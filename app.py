from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET_NAME, LOCATION, aws_db
import boto3
from flask import Flask, render_template, request, flash, redirect, url_for
# from werkzeug.utils import secure_filename
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


# file uploading
@app.route('/file_upload', methods=['POST'])
def upload_image():
    try:
        # 1. get file
        if request.files['file'].filename == '':
            flash('파일이 없습니다')
            return redirect(url_for('upload'))
        file = request.files['file']
        # f.save(secure_filename(f.filename))

        # 2. 모델 적용

        # 3. mysql 적용
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

        # 4. s3 연동
        s3 = s3_connection()
        s3.put_object(
            Bucket=BUCKET_NAME,
            Body=file,
            Key=file.filename,
            ContentType=file.content_type
        )
        return render_template('index.html')
    except Exception as e:
        print(e)



# 결과 도출
@app.route('/list_result', methods=['POST'])
def image_list():
   search_word = request.form['search-word']
   print(search_word)
   conn = mysql.connect()
   cursor = conn.cursor()
   sql = "SELECT * FROM pictures WHERE caption_result=%s OR ocr_result=%s";
   cursor.execute(sql, (search_word, search_word))
   
   rows = cursor.fetchall()
   result_list = []
   for e in rows:
      print(e)
      result_list.append(e[1])
   print(result_list)
   conn.commit()
   conn.close()
   
   image_s3_url = [ f"https://{BUCKET_NAME}.s3.{LOCATION}.amazonaws.com/{filename}" for filename in result_list]  
   return render_template('list.html', data = image_s3_url)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5003, debug=True)
