from flask import Blueprint, jsonify, request
from .CurrencyUseCase import ExchangeCurrency

currency_blueprint = Blueprint('currency', __name__)

exchange_currency_use_case = ExchangeCurrency()


@currency_blueprint.route('/exchange_currency', methods=['POST'])
def exchange_currency():
    data = request.json
    source = data['source_currency']
    target = data['target_currency']
    amount = data['amount']
    result = exchange_currency_use_case.exchangeCurrency(source, target, amount)
    return jsonify(result[0]), result[1]
