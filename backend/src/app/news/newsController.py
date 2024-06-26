import requests
from flask import Blueprint, jsonify


news_blueprint = Blueprint('news', __name__)

@news_blueprint.route('/get_news/<string:query>', methods=['GET'])
def get_external_api_data(query):
    params = {
        'apikey': 'pub_40713b5222424acf2f6ad9e7cb358ad0bafd5',
        'q': query,
        'language': 'en'
    }
    response = requests.get('https://newsdata.io/api/1/news', params=params)
    data = response.json()
    return jsonify(data)