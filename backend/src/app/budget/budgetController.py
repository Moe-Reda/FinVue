from flask import Blueprint, jsonify, request
from .budgetUseCases import CreateBudget, FetchBudget, UpdateBudget

budgets_blueprint = Blueprint('budgets', __name__)

create_budget_use_case = CreateBudget()
fetch_budget_use_case = FetchBudget()
update_budget_use_case = UpdateBudget()


@budgets_blueprint.route('/create_budget', methods=['POST'])
def create_budget():
    data = request.json
    username = data['username']
    category = data['category']
    allowance = data['allowance']
    month_year = data['month_year']
    msg = create_budget_use_case.createBudget(username, category, allowance,
                                              month_year)
    return jsonify(msg[0]), msg[1]


@budgets_blueprint.route('/update_budget', methods=['POST'])
def update_budget():
    data = request.json
    username = data['username']
    category = data['category']
    amount = data['amount']  # Amount to be added to 'spent'
    month_year = data['month_year']
    msg = update_budget_use_case.updateBudget(username, category, amount,
                                              month_year)
    return jsonify(msg[0]), msg[1]


@budgets_blueprint.route('/fetch_budget/<string:username>/<string:month_year>',
                         methods=['GET'])
def fetch_budget(username, month_year):
    result = fetch_budget_use_case.fetchBudget(username, month_year)
    return jsonify(budgets=result[0]), result[1]
