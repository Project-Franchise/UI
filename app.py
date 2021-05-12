from flask import Flask, render_template, request, flash, redirect, url_for
from error_handlers import page_not_found, internal_server_error, bad_request_error
import requests


app = Flask(__name__)

app.register_error_handler(400, bad_request_error)
app.register_error_handler(404, page_not_found)
app.register_error_handler(500, internal_server_error)

def city(id):
    return requests.get("http://127.0.0.1:5000/city", params={"id": id}).json()


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
    path_to_domria = "https://dom.ria.com/uk/"
    states = requests.get("http://127.0.0.1:5000/states")
    realty_types = requests.get("http://127.0.0.1:5000/realty_types")
    operation_types = requests.get("http://127.0.0.1:5000/operation_types").json()
    response = request.args
    request_to_client_service = {
        'price': {},
        'square': {},
        'floor': {},
        'floors_number': {},
        'page_ads_number': 10,
        'page': 1
    }
    for key, value in response.items():
        if value != '':
            if 'ge' in key or 'le' in key:
                try:
                    request_to_client_service[key.split('-')[0]][key.split('-')[1]] = int(value)
                except ValueError or KeyError:
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
    data_for_user = []
    for items in response_from_server:
        print(items)
        data_for_user.append(
            {
                'City': city(items[0]['city_id'])[0]['name'],
                'Floor': items[1]['floor'],
                'Square': items[1]['square'],
                'Price': items[1]['price'],
                "href": f'{path_to_domria}{items[1]["original_url"]}' if items[0]['service_id'] == 1 else '#'
            }
        )
    return render_template("index.html", states=states.json(), realty_types=realty_types.json(), list=data_for_user, count=len(response_from_server))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
