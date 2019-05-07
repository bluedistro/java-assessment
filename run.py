import pandas as pd
from flask import Flask, jsonify, request
import json
import numpy as np

app = Flask(__name__)

def read_results():
    # read excel file
    xls_file = pd.ExcelFile('java_assessment.xlsx')
    # drop the header from the file and use declared ones
    headers = ['ID', 'Names', 'QUIZ_1', 'QUIZ_3_Programming', 'QUIZ_3_Written', 'QUIZ_2_GUI', 'QUIZ_2_GUI_IMPLEMENTATION']
    data = xls_file.parse('Sheet3', names=headers)
    # drop  the quiz three comments and quiz five results for now
    return data


@app.route("/java/<int:id_number>")
def view_results(id_number):
    data = read_results()
    print(data)
    try:
        # cast id numbers to int
        data["ID"] = data["ID"].astype(int)
        results = data.loc[data["ID"] == id_number]
        results = (results.to_dict(orient="records"))[0]
        info = ({"ASSESSMENT": results,
                 "NOTICE": "Quiz 1 - 16 marks. Quiz 2 - 20 marks each. Quiz 3 Written - 14. Quiz 3 Programming - 15"})
        return jsonify(info)
    except Exception as e:
        return jsonify({"Error": "Unknown Error during processing.."})

@app.route("/java")
def view_results_name():
    data = read_results()
    name = request.args.get('name', None)
    if name is None:
        abort(404)
    else:
        try:
            print(name)
            data['ID'] = data['ID'].astype(int)
            name_to_lower = data['Name'].str.lower()
            location = np.where(name_to_lower.str.contains(name.lower()))[0][0]
            results = data.iloc[[location]]
            info = ({"ASSESSMENT": results,
                     "NOTICE": "Quiz 1 - 10 marks. Quiz 2 - 10. Quiz 3 - 13. "
                                            "Quiz 4 - 9. Quiz 5 Programming - 10. Quiz 5 Written - 20"})
            return jsonify(info)
        except Exception as e:
            return jsonify({"status": "failure",
                            "Error": "Name does not match any name in the database"})

if __name__ == "__main__":
    app.run()
