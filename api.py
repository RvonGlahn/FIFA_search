import flask
from flask import jsonify, request
from flask_cors import CORS
from resources.search_players import SearchPlayers
import json
import os
from dotenv import load_dotenv

# from werkzeug.contrib.fixers import ProxyFix

# load env variables
load_dotenv()

app = flask.Flask(__name__)
CORS(app)


# Use the fixer if Proxy causes issues
# app.wsgi_app = ProxyFix(app.wsgi_app)

fifa_search = SearchPlayers()


@app.route("/api", methods=["GET"])
def api_route():
    return (
        "<h2>FIFA API</h2>"
        "<p>Use API routes:</p>"
        "<p>/search</p>"
        "<p>/suggest</p>"
        "<p>/attributes</p>",
        200,
    )


@app.route("/api/suggest/<string:part>", methods=["GET"])
def suggest_name(part):
    return jsonify(fifa_search.get_suggestion(part))


@app.route("/api/search", methods=["POST"])
def search_players():
    return jsonify(fifa_search.get_players(json.loads(request.data)))


@app.route("/api/attributes", methods=["GET"])
def attribute_list():
    return fifa_search.get_attributes_json()


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == "__main__":
    print(os.environ["FLASK_RUN_HOST"])
    app.run(host=os.environ["FLASK_RUN_HOST"], port=os.environ["FLASK_RUN_PORT"])
