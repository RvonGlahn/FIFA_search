import flask
from flask import jsonify
from flask_cors import CORS
from resources.search_players import SearchPlayers

app = flask.Flask(__name__)
CORS(app)

fifa_search = SearchPlayers()


@app.route('/api/attribute_list', methods=['GET'])
def attribute_list():
    return jsonify(fifa_search.get_attributes_json())


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


app.run()
