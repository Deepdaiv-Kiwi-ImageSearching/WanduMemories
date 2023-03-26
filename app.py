from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET_NAME, aws_db
import boto3
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from flaskext.mysql import MySQL 

app = Flask(__name__)

# mysql
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = aws_db["user"]
app.config['MYSQL_DATABASE_PASSWORD'] = aws_db["password"]
app.config['MYSQL_DATABASE_DB'] = aws_db["database"]
app.config['MYSQL_DATABASE_HOST'] = aws_db["host"]
mysql.init_app(app)



# s3 connection
def s3_connection():
   try:
      s3 = boto3.client(
            "s3",
            region_name="ap-northeast-2",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
         )
   except Exception as e:
      print(e)
   else:
      print("s3 bucket connected!")
      return s3


# get pages
@app.route('/')
def home_page():
   return render_template('index.html')

@app.route('/list')
def list_page():
   return render_template('list.html')

@app.route('/upload')
def upload_page():
   return render_template('upload.html')






# 파일 업로드
@app.route('/file_upload', methods=['POST'])
def upload_image():
   try:
      
      if request.method == "POST":
         if request.files['file'].filename == '':
            flash('파일이 없습니다') 
            return redirect(url_for('upload'))
         # 파일 업로드
         file = request.files['file']
         # f.save(secure_filename(f.filename))
         
         
         # mysql 적용
         conn = mysql.connect()
         cursor = conn.cursor()
         insert_stmt = (
            "INSERT INTO pictures (filename, ocr_result, caption_result) "
            "VALUES (%s, %s, %s)"
         )
         data = (file.filename, "dddd", "안녕")
         cursor.execute(insert_stmt, data)
         conn.commit()
         conn.close()

         
         # s3 연동
         s3 = s3_connection()
         s3.put_object(
            Bucket = BUCKET_NAME,
            Body = file,
            Key = file.filename,
            ContentType = file.content_type
         )
         
         return render_template('index.html')
      else:
         return render_template('upload.html')
   except Exception as e:
      print(e)
   

# 결과 도출
# @app.route('/list_result', methods=['GET'])
# def image_list():
   

   
   
   
   
	
if __name__ == '__main__':  
   app.run('0.0.0.0',port=5001,debug=True)

