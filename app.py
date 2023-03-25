from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)


# page
@app.route('/')
def home_page():
   return render_template('index.html')

@app.route('/list')
def list_page():
   return render_template('list.html')

@app.route('/upload')
def upload_page():
   return render_template('upload.html')



# s3 connection
# import boto3
# def s3_connection():
   


# file uploading
@app.route('/file_upload', methods=['POST'])
def upload_image():
   if request.method == "POST":
      if request.files['file'].filename == '':
          flash('파일이 없습니다. 파일을 제출하세요!') 
          # 파일이 없으면 flash 전달. (현재 창에서 flash 메시지 출력.) 
          return redirect(url_for('upload'))
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return '파일이 저장되었습니다'
   else:
      return render_template('upload.html')
   
   
   
   
   
	
if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)
   app.secret_key = 'super secret key'
   app.config['SESSION_TYPE'] = 'filesystem'
