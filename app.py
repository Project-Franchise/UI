from flask import Flask, render_template, request, jsonify
from error_handlers import page_not_found, internal_server_error, bad_request_error
import requests
from constants import SERVICES


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


@app.route("/cities/<int:state_id>")
def get_cities_by_sattes(state_id):
    """
    Returns html - dropdown of cities in state with state_id
    """
    cities = requests.get(f"http://127.0.0.1:5000/cities?state_id={state_id}")
    return jsonify({"data": render_template("cities_dropdown.html", cities=cities.json())})


@app.route('/result', methods=["POST"])
def result():
    response = request.get_json()
    response["page"] = 1
    response["page_ads_number"] = 10
    response_from_server = requests.post("http://127.0.0.1:5000/realty", json=response).json()
    data_for_user = []
    for items in response_from_server:
        details = items["realty_details"]
        data_for_user.append(
            {
                "City": items["city"]["name"] if items["city"] else "Uknown",
                "State": items["state"]["name"],
                "Floor": details["floor"],
                "Square": details["square"],
                "Price": details["price"],
                "href": details["original_url"]
            }
        )
    return jsonify({"data": render_template("results.html", list=data_for_user, count=len(response_from_server))})


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
