from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, BUCKET_NAME
import boto3
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)


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


@app.route('/file_upload', methods=['POST'])
def upload_image():
   if request.method == "POST":
      if request.files['file'].filename == '':
          flash('파일이 없습니다') 
          return redirect(url_for('upload'))
      # 파일 업로드
      f = request.files['file']
      # f.save(secure_filename(f.filename))
      
      # 모델 적용
      

      
      # s3 연동
      s3 = s3_connection()
      s3.put_object(
         Bucket = BUCKET_NAME,
         Body = f,
         Key = f.filename,
         ContentType = f.content_type
      )
      return render_template('index.html')
   else:
      return render_template('upload.html')
   

# 모델 불러오기

   
   
   
   
	
if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)

