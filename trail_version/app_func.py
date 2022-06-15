from flask import Flask, jsonify, request
from flask_restful import Resource, Api

import io
import json
import os
import re
import shutil  # For copying files and for file handling.
import time
import pandas as pd
from flask import (Flask, redirect, render_template, request,jsonify,
                   send_from_directory, url_for,flash)
from pdfminer.converter import (HTMLConverter, PDFPageAggregator,
                                TextConverter, XMLConverter)
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from werkzeug.utils import secure_filename

from doc_codes.doc_sum_test import Prediction
from doc_codes.doc_sum_train import Doc_summ

# creating the flask app
app = Flask(__name__)
# creating an API object
api = Api(app)

app.config['UPLOAD_FOLDER'] = './UPLOAD_FOLDER/'

global BatchList
global TextList
global BatchCount
global TextCount
global Log
BatchList = []
TextList = []
BatchCount = 0
TextCount = 0
Log = {}

class DocSummary(Resource):
    # @app.route('/')
    def get(self):
        # return render_template('Page.html')
        
        Console = "None"
        ProgressBarValue = 0

        if 'UPLOAD_FOLDER' in os.listdir('./'):
        
            for fileName in os.listdir(app.config['UPLOAD_FOLDER']):
                shutil.rmtree(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
                
            os.rmdir(app.config['UPLOAD_FOLDER'])
            
        os.mkdir(app.config['UPLOAD_FOLDER'])

        return render_template('Page.html', BatchList = BatchList, Console = Console, ProgressBarValue = ProgressBarValue)

    @app.route('/RunPage', methods = ['GET', 'POST'])
    def RunPage():
        global BatchList
        global TextList
        global TextCount
        global BatchCount
        global Log
        
        errors = []
        results = {}

        summarized_result=None
        SelectedItem = request.form.get("Selection")

        def getLocalTime():
            LocalTime = time.localtime()
            return "{}/{}/{} {}:{}:{}".format(LocalTime.tm_mday, LocalTime.tm_mon, LocalTime.tm_year, LocalTime.tm_hour, LocalTime.tm_min, LocalTime.tm_sec)
        
        def getLogTime():
            LocalTime = time.localtime()
            return "{}{}{}_{}{}{}".format(LocalTime.tm_mday, LocalTime.tm_mon, LocalTime.tm_year, LocalTime.tm_hour, LocalTime.tm_min, LocalTime.tm_sec)
        
        if request.method=='POST':
            try:
                text = request.form['SummarizeBlock']

                summary_length = request.form['summarizer_length']
            except:
                errors.append("Unable to get text/Summary length")
                return render_template('Page.html',errors=errors)
            
            try:
                Pred = Prediction(text,summary_length)
                Text_Extract = Pred.summary()
                boolSelectCode = True
                # result = {
                #     "output": Text_Extract,
                #     }
                # result = {str(key): value for key, value in result.items()}
                # print(result)
                # summarized_result = result['output']
                summarized_result = Text_Extract

            except:
                errors.append("Requested summary length is greater than given text length ")

        return render_template('Page.html',summarized_result=summarized_result, errors=errors)

