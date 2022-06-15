from flask import Flask
import PyPDF2
import pandas as pd
import xlrd
UPLOAD_FOLDER = 'uploads/'

from flask import Flask, request, abort, jsonify, send_from_directory
# from app import app
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

import os
import urllib.request
# from app import app
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','xlsx','csv'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		resp = jsonify({'message' : 'File successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
		resp.status_code = 400
		return resp

def read_pdf(file):
	# creating a pdf file object
	pdfFileObj = open(file,'rb').endecode("utf-8")
	
	# creating a pdf reader object
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	
	# printing number of pages in pdf file
	print(pdfReader.numPages)
	
	# creating a page object
	pageObj = pdfReader.getPage(0)
	
	# extracting text from page
	# print(pageObj.extractText())

	return pageObj

def read_csv(file):
	import pickle
	if file.split(".")[-1] == ".xlsx":

		# with open(file, 'wb') as output:
		# 	pickle.dump(file, output)
		# with open(file, 'rb') as input:
		# 	data = pickle.load(input)
		
		wb = xlrd.open_workbook(file)
		sheet = wb.sheet_by_index(0)
 
		# For row 0 and column 0
		sheet.cell_value(0, 0)
		
		# Extracting number of columns
		# print(sheet.ncols)
		return sheet.ncols
	else:
		df = pd.read_csv(file,encoding='latin-1')
		return df

@app.route("/get-files/<name>")
def get_file(name):
    """Download a file."""
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
	
@app.route('/result_response',methods = ["GET"])
def read_file(file_path=app.config["UPLOAD_FOLDER"]):
	# files = os.listdir(file_path)
	if not os.listdir(file_path):
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	else:
		for i in os.listdir(file_path):
			if i.split(".")[-1] == ".pdf":
				pageobj = read_pdf(file_path+"/"+i)
			else:
				df = read_csv(file_path+"/"+f"{i}")
				# print(len(df))
		result = {
			"pdf_output": pageobj.extractText(),
			"csv_output" : len(df)
		}
		result = {str(key): value for key, value in result.items()}
		
		extracted_text_result = result['pdf_output']
		extracted_csv_result = result['csv_output']
	
	return jsonify(dict({"response":str(extracted_text_result)}))
		
if __name__ == "__main__":
    app.run(debug=True,port=5001)