from .billsRepository import BillsRepository
from datetime import datetime

class CreateBill:
    billsRepository = BillsRepository()
    def createsBill(self, user_id, bill_name, bill_amount, due_date, recurring, frequency):
        try:
            user_id_result = self.billsRepository.getUserId(user_id)
            if user_id_result is None:
                return {'message': 'Username not found'}, 404
            user_id_final = user_id_result[0]
            self.billsRepository.createorupdateBill(user_id_final, bill_name, bill_amount, due_date, recurring, frequency)
            return {'message': 'Bill created successfully'}, 201
        except Exception as e:
            return {'error': str(e)}, 500
        
        
class FetchBill:
    billsRepository = BillsRepository()

    def fetchBill(self, username):
        try:
            user_id_result = self.billsRepository.getUserId(username)
            if user_id_result is None:
                return {'message': 'Username not found'}, 404
            user_id = user_id_result[0]
            bills = self.billsRepository.fetchBills(user_id)
            if not bills:
                return {'message': 'No bills found for the user'}, 404
            
            bills_dict_list = [
                {
                    'name': bill[0],
                    'amount': bill[1],
                    'dueDate': bill[2].strftime('%Y-%m-%d %H:%M:%S'),
                    'recurring': bill[3],
                    'frequency': bill[4]
                } for bill in bills
            ]
            
            return {'bills': bills_dict_list}, 200

        except Exception as e:
            return {'error': str(e)}, 500