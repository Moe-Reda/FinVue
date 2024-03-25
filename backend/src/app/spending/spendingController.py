from flask import Blueprint, jsonify, request
from .spendingUseCase import SpendingUseCase

spendings_blueprint = Blueprint('spendings', __name__)

spending_use_case = SpendingUseCase()

@spendings_blueprint.route('/spendings/<string:username>', methods=['GET'])
def fetch_spendings(username):
    result = spending_use_case.fetchSpendings(username)
    return jsonify(spendings=result[0]), result[1]
