"""The Endpoints to manage the BOOK_REQUESTS"""
import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint
import requests

REQUEST_API = Blueprint('request_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API



@REQUEST_API.route('/request', methods=['POST'])
def create_record():
    """Create a book request record
    @param email: post : the requesters email address
    @param title: post : the title of the book requested
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if not data.get('email'):
        abort(400)
    if not data.get('title'):
        abort(400)

    new_uuid = str(uuid.uuid4())
    book_request = {
        'title': data['title'],
        'email': data['email'],
        'timestamp': datetime.now().timestamp()
    }
    BOOK_REQUESTS[new_uuid] = book_request
    # HTTP 201 Created
    return jsonify({"id": new_uuid}), 201





@REQUEST_API.route('/recommend/startups/<int:investor_id>', methods=['PUT'])
def investor_recommendations(investor_id):
    """Get startups that match an investor by adding investor params
    @param name: Name of the investor
    @param fundingType: Choose if the type is Pre-Serie A, Serie A,...
    @param: location: Location of the investor
    @param: description: Brieve Description of the investor
    @param: fullDescription: Full description of the investor
    @return: 200: starttups
    @raise 400: misunderstood request
    """

    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if not data.get('name'):
        abort(400)
    if not data.get('fundingType'):
        abort(400)
    if not data.get('location'):
        abort(400)
    if not data.get('description'):
        abort(400)
    if not data.get('fullDescription'):
        abort(400)

    investor_request = {
        'name': data['name'],
        'fundingType': data['fundingType'],
        'location': data['location'],
        'description': data['description'],
        'fullDescription': data['fullDescription'],
    }
    BASE = "http://127.0.0.1:5000/"
    reponse2 = requests.put(BASE + "recommend/startups/1", investor_request)
    print(reponse2.json())
    # server.Recommend.put(investor_id=investor_id), 200
    return jsonify(reponse2)