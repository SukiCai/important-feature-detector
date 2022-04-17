import random_forest
import pandas as pd
from flask import Flask, render_template, url_for, request

def clean():
    columns_dropped = open("code/output/columns_dropped.csv", "w+")
    columns_dropped.truncate()
    columns_dropped.close()
    apply_to_ui = open("code/output/apply_to_ui.csv", "w+")
    apply_to_ui.truncate()
    apply_to_ui.close()
    print("Cleaned Up")


# clean()
# rf = random_forest.RandomForest("code/uploads/analyze_target.csv","code/output/result.csv", "blnIsThreatening",0.92,0.01,[])
# rf.start()

app = Flask(__name__)
@app.route('/')
@app.route('/home')
def home():
    return render_template("project.html")

@app.route('/result',methods=['POST', 'GET'])
def result():
    clean()
    rf = random_forest.RandomForest("code/uploads/analyze_target.csv","code/output/result.csv", "blnIsThreatening",0.92,0.01,[])
    rf.start()
    output = pd.read_csv("code/output/features_ranking.csv").to_json()
    print(output)
    name = output
    return render_template('project.html', name = name)

if __name__ == "__main__":
    app.run(debug=True)