from distutils.log import debug
from fileinput import filename
from flask import *
from datetime import datetime
import os
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the uploads folder if it does not already exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/success',methods = ['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(filepath)
        return render_template("acknowledgement.html", name = f.filename)
    
@app.route('/uploads')
def list_uploads():
    files_info = []
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    for filename in files:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        size = os.path.getsize(filepath)
        mtime = os.path.getmtime(filepath)
        modified_date = datetime.fromtimestamp(mtime)

        files_info.append({
            'name': filename,
            'size': size,
            'modified_date': modified_date
        })
    return render_template('uploads.html', files = files_info)

@app.route('/uploads/<filename>')
def display_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(filepath, as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True)
