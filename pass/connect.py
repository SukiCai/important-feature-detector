import random_forest
import pandas as pd
import time
import os
import csv
from flask import Flask, render_template, url_for, request
import subprocess

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


@app.route('/ask', methods=['POST'])
def ask():
    subprocess.call(["php","code/pass/contact-form-process.php"],stdout=subprocess.PIPE)
    # path = r"code/pass/contact-form-process.php"
    # assert os.path.isfile(path)
    # with open(path, "r") as f:
    #     subprocess.call(path)
    # pass
    return render_template('project.html')


@app.route('/result',methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    name = output['name']
    accuracy = float(output['accuracy'])
    clean() 
    rf = random_forest.RandomForest("code/uploads/analyze_target.csv","code/output/result.csv", name, accuracy,0.01,[])
    rf.start()
    rf.visualize()
    return render_template('feature_ranking.html')

if __name__=="__main__":
    app.run(debug=True)