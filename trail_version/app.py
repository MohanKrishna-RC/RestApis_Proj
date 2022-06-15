import os

from flask import Flask, request, abort, jsonify, send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'api_uploaded_files/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@app.route("/get-files/<name>")
def get_file(name):
    """Download a file."""
    return send_from_directory(app.config["UPLOAD_FOLDER"], name,as_attachment=True)
    # print(file)
    # requests.get = 
    # import PyPDF2
 
    # # creating a pdf file object
    # pdfFileObj = open(file,'rb')

    # # creating a pdf reader object
    # pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # # printing number of pages in pdf file
    # print(pdfReader.numPages)

    # # creating a page object
    # pageObj = pdfReader.getPage(0)

    # # extracting text from page
    # print(pageObj.extractText())


@app.route("/files/<filename>", methods=["POST"])
def post_file(filename):
    """Upload a file."""

    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories allowed")

    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "wb") as fp:
        fp.write(request.data)

    # Return 201 CREATED
    return "", 201

app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True)

if __name__ == "__main__":
    app.run(debug=True, port=8000)