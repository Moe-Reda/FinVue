from flask import Blueprint, jsonify, request
from .createTransactionsUseCase import CreateTransaction
from .fetchTransactionsUseCase import FetchTransactions
from .transactionsPieChartUseCase import TransactionsPieChart


transactions_blueprint = Blueprint('transactions', __name__)

create_transaction_use_case = CreateTransaction()
fetch_transactions_use_case = FetchTransactions()
transactions_pie_chart_use_case = TransactionsPieChart()


@transactions_blueprint.route('/create_transaction', methods=['POST'])
def create_transaction():
    data = request.json
    username = data['username']
    # need to get user_id from database by searching database with username
    amount = data['amount']
    category = data.get('category',
                        'Uncategorized')  # Default category to 'Uncategorized' if not provided
    msg = create_transaction_use_case.createTransaction(username, amount, category)
    return jsonify(msg[0]), msg[1]


@transactions_blueprint.route('/fetch_transactions/<string:username>',
                              methods=['GET'])
def fetch_transactions(username):
    result = fetch_transactions_use_case.fetchTransactions(username)
    return jsonify(transactions=result[0]), result[1]


@transactions_blueprint.route('/piechart/<string:username>',
                              methods=['GET'])
def transactions_pie_chart(username):
    result = transactions_pie_chart_use_case.transactionsPieChart(username)
    return jsonify(totals=result[0]), result[1]
