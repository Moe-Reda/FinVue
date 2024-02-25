from flask import Blueprint, jsonify, request
from .stocksUseCase import Stocks

stocks_blueprint = Blueprint('stocks', __name__)

stocks_use_case = Stocks()


@stocks_blueprint.route('/get_time_series/<string:stock>/<int:days>', methods=['GET'])
def getStockTimeSeries(stock, days):
    result = stocks_use_case.getStockTimeSeries(stock, days)
    return jsonify(timeSeries=result[0]), result[1]


@stocks_blueprint.route('/get_portfolio_time_series/<string:username>/<int:days>',
                        methods=['GET'])
def getPortfolioTimeSeries(username, days):
    result = stocks_use_case.getPortfolioTimeSeries(username, days)
    return jsonify(timeSeries=result[0]), result[1]


@stocks_blueprint.route('/get_all_stocks/<string:username>', methods=['GET'])
def getAllStocks(username):
    result = stocks_use_case.fetchAllStocks(username)
    return jsonify(stocks=result[0]), result[1]

@stocks_blueprint.route('/add_stock', methods=['POST'])
def add_stock():
    data = request.json
    username = data['username']
    tick = data['tick']
    order = data['order']
    quantity = data['quantity']
    msg = stocks_use_case.addStock(tick, username, quantity, order)
    return jsonify(msg[0]), msg[1]
