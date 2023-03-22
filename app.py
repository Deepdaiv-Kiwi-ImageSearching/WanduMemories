from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def home_page():
   return render_template('index.html')

@app.route('/upload')
def upload_page():
   return render_template('upload.html')

# 파일 업로드
# @app.route('/file', methods=['POST'])
# def file_upload():
# 	file = request.files['file']
    	
#    filename = secure_filename(file.filename)
#    os.makedirs(image_path, exists_ok=True)
#    file.save(os.path.join(image_path, filename)
      
#    return

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)
