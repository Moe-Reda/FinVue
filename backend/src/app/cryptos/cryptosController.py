from flask import Blueprint, jsonify, request
from .cryptosUseCase import Cryptos

cryptos_blueprint = Blueprint('cryptos', __name__)

cryptos_use_case = Cryptos()


@cryptos_blueprint.route('/get_crypto_time_series/<string:crypto>/<int:days>',
                         methods=['GET'])
def getCryptoTimeSeries(crypto, days):
    result = cryptos_use_case.getCryptoTimeSeries(crypto, days)
    return jsonify(timeSeries=result[0]), result[1]


@cryptos_blueprint.route('/get_crypto_portfolio_time_series/<string:username'
                         '>/<int:days>',
                         methods=['GET'])
def getPortfolioTimeSeries(username, days):
    result = cryptos_use_case.getPortfolioTimeSeries(username, days)
    return jsonify(timeSeries=result[0]), result[1]


@cryptos_blueprint.route('/get_all_cryptos/<string:username>', methods=['GET'])
def getAllCryptos(username):
    result = cryptos_use_case.fetchAllCryptos(username)
    return jsonify(cryptos=result[0]), result[1]


@cryptos_blueprint.route('/add_crypto', methods=['POST'])
def add_crypto():
    data = request.json
    username = data['username']
    tick = data['tick'] + "-USD"
    order = data['order']
    quantity = data['quantity']
    msg = cryptos_use_case.addCrypto(tick, username, quantity, order)
    return jsonify(msg[0]), msg[1]
