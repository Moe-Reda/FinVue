from flask import Blueprint, jsonify, request
from .billsUseCases import CreateBill, FetchBill

bills_blueprint = Blueprint('bills', __name__)

create_bill_use_case = CreateBill()
fetch_bill_use_case = FetchBill()

@bills_blueprint.route('/create_bill', methods=['POST'])
def create_bill():
    data = request.json
    userid= data['user']
    bill_name = data['name']
    bill_amount = data['amount']
    bill_date = data['dueDate']
    recurring = data['recurring']
    frequency = data['frequency']
    msg = create_bill_use_case.createsBill(userid, bill_name, bill_amount, bill_date, recurring, frequency)
    return jsonify(msg[0]), msg[1]

    
@bills_blueprint.route('/fetch_bills/<string:username>',
                         methods=['GET'])
def fetch_bills(username):
    result = fetch_bill_use_case.fetchBill(username)
    return jsonify(result[0]), result[1]