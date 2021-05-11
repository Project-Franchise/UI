from flask import Flask, render_template, request, flash, redirect, url_for
from error_handlers import page_not_found, internal_server_error, bad_request_error
import requests


app = Flask(__name__)

app.register_error_handler(400, bad_request_error)
app.register_error_handler(404, page_not_found)
app.register_error_handler(500, internal_server_error)


@app.route('/')
def main_page():
    """
    Main Home page route
    """
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


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
