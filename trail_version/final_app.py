import os
from urllib import response
from flask import Flask, flash, request, redirect, url_for,Request,jsonify
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

UPLOAD_FOLDER = 'api_uploaded_files/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
import requests
@app.route('/upload_text/', methods=['GET', 'POST'])
def upload_text():
    if request.method == 'POST':
        # check if the post request has the file part
        # file = request.files['file']
        text = request.form
        print(text)
    if request.method == 'GET':
        text = request.form
        print(text)
        
    return jsonify(dict(text=text))
    
from flask import send_from_directory

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

data = []
@app.route('/get-files/<name>')
def get_files(name):
    # data = download_file(name)
    data = [dict(file=name)]
    # with open(os.path.join(app.config['UPLOAD_FOLDER'], name), "rb") as fp:
    #     fp.read(request.data)
    import PyPDF2

    # creating a pdf file object
    pdfFileObj = open(app.config["UPLOAD_FOLDER"]+data[0]["file"],'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    print(pdfReader.numPages)


    # response = jsonify(data)
    # print(response)

    import textract
    text = textract.process(app.config["UPLOAD_FOLDER"]+data[0]["file"], method='pdfminer').decode('utf8')
    print(text)
    return jsonify(dict(text=text))

    # import PyPDF2

    # # creating a pdf file object
    # pdfFileObj = open(file,'rb')

    # # creating a pdf reader object
    # pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# file = download_file()
# print(file)




app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)

if __name__=="__main__":
    app.run(debug=True,port=8000)