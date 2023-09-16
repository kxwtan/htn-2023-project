import time
from flask import Flask, jsonify, request, Response
import pandas as pd
app = Flask(__name__)

@app.route('/get_latest_et_data', methods=['GET'])
def get_latest_et_data():
    df = pd.read_csv('data.csv', header=None, names=["col1", "x", "y", "z", "vergence"])

    return json_data_list

app.run()
