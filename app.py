from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/')
def main_page():
    states = requests.get("http://127.0.0.1:5000/states")
    realty_types = requests.get("http://127.0.0.1:5000/realty_types")
    return render_template("index.html", states=states.json(), realty_types=realty_types.json())


@app.route('/result')
def result():
    operation_types = requests.get("http://127.0.0.1:5000/operation_types")
    operation_types_list = operation_types.json()
    response = request.args
    print(response)
    return "HELLO"

app.run(host='127.0.0.1', port=8000)
