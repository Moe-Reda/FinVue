from flask import Blueprint, jsonify, request
from .savingsUseCases import CreateSavings

savings_blueprint = Blueprint('savings', __name__)

create_savings_use_case = CreateSavings()

# fetch_budget_use_case = FetchBudget()
# update_budget_use_case = UpdateBudget()


@savings_blueprint.route('/make_savings', methods=['POST'])
def create_savings():
    data = request.json
    initial_savings = float(data['initial_savings'])
    monthly_added_savings = float(data['monthly_added_savings'])
    predicted_interest_rate = float(data['predicted_interest_rate'])
    time_period = float(data['months'])
    result = create_savings_use_case.createSavings(initial_savings, monthly_added_savings, predicted_interest_rate,
                                              time_period)
    return jsonify(result[0]), result[1]

