from flask import Flask, render_template, request, flash, redirect, url_for
import requests

app = Flask(__name__)


@app.route('/')
def main_page():
    states = requests.get("http://127.0.0.1:5000/states")
    realty_types = requests.get("http://127.0.0.1:5000/realty_types")
    return render_template("index.html", states=states.json(), realty_types=realty_types.json(), list={})


@app.route('/result')
def result():
    operation_types = requests.get("http://127.0.0.1:5000/operation_types").json()
    response = request.args
    request_to_client_service = {'price': {}, 'page_ads_number': 10, 'page': 1}
    for key, value in response.items():
        if value != '':
            if key == 'from' or key == 'to':
                try:
                    request_to_client_service['price'][key] = int(value)
                except ValueError:
                    return redirect(url_for('main_page'))
            elif key == 'operation_type_id':
                for operations in operation_types:
                    if operations['name'] == value:
                        request_to_client_service[key] = operations['id']
                        break
            elif "latest" in key and key == "latest":
                try:
                    request_to_client_service[key] = bool(value)
                except ValueError:
                    return redirect(url_for('main_page'))
            else:
                try:
                    request_to_client_service[key] = int(value)
                except ValueError:
                    return redirect(url_for('main_page'))
    response_from_server = requests.post("http://127.0.0.1:5000/realty", json=request_to_client_service).json()
    print(response_from_server)
    return render_template('results.html', list=response_from_server['response'])

app.run(host='127.0.0.1', port=8000)
