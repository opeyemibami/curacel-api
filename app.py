from flask import Flask, request, flash, redirect,jsonify
from werkzeug.utils import secure_filename
import os
from ml import get_prediction

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# uploaded images are stored in 'images' folder
UPLOAD_FOLDER = './images'

ALLOWED_EXTENSIONS = set(['png', 'jpg'])
 
# Setting a environment variable
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return ('Api is functional')

@app.route('/', methods=['POST'])
def upload_file():
    print('Uploading')
    if request.method == 'POST':
     
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filename)
    
            pred,confidence_level = get_prediction(filename)
            resp = jsonify({'predicted class' : str(pred), 'model confidence level':str(confidence_level)})

            
            
            # Delete the file
            os.remove(filename)
        return resp

# The app will run in debug mode
if __name__ == '__main__':
    app.run(debug=True)