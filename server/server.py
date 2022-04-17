from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/result',methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    print(output)
    name = output["name"]
    return render_template('index.html', name = name)

if __name__ == "__main__":
    app.run(debug=True)

# #!/usr/bin/env python3
# print("REARAFEAFEAW")
# import random_forest
# print("))))))))")
# def file_clean():
#     columns_dropped = open("code/output/columns_dropped.csv", "w+")
#     columns_dropped.truncate()
#     columns_dropped.close()
#     apply_to_ui = open("code/output/apply_to_ui.csv", "w+")
#     apply_to_ui.truncate()
#     apply_to_ui.close()

# file_clean()
# rf = random_forest.RandomForest("code/uploads/weight_to_test.csv","code/output/result.csv", "blnIsThreatening",0.85,0.01,[])
# rf.start()
