import random_forest
import pandas as pd
import time
import os
import csv
from flask import Flask, render_template, url_for, request

def clean():
    columns_dropped = open("code/output/columns_dropped.csv", "w+")
    columns_dropped.truncate()
    columns_dropped.close()
    apply_to_ui = open("code/output/apply_to_ui.csv", "w+")
    apply_to_ui.truncate()
    apply_to_ui.close()
    print("Cleaned Up")


from flask import Flask,render_template
UPLOAD_FOLDER = 'code/output'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
app=Flask(__name__,template_folder='templates',static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/project/")
def project():
    return render_template('project.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('project.html', message = "No file part")
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return render_template('project.html', message = "No file selected")
        if allowed_file(file.filename) == False:
            return render_template('project.html', message = "Only csv file accepted")
        if file:
            filename = "analyze_target.csv"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('project.html')

@app.route('/result',methods=['POST', 'GET'])
def result():
    clean() 
    rf = random_forest.RandomForest("code/uploads/analyze_target.csv","code/output/result.csv", "blnIsThreatening",0.92,0.01,[])
    rf.start()
    rf.visualize()
    name = "suki"
    return render_template('feature_ranking.html', name = name)

if __name__=="__main__":
    app.run(debug=True)