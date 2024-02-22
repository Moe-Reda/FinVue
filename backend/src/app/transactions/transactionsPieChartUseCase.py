from .transactionRepository import TransactionRepository

class TransactionsPieChart:
     transactionRepository = TransactionRepository()
     def transactionsPieChart(self, username):
        try:
            user_id_result = self.transactionRepository.getUserId(username)
            if user_id_result is None:
                return {'message': 'Username not found'}, 404
            user_id = user_id_result[0]
        except Exception as e:
            return {'error': str(e)}, 500
        
        try:
            cats_and_totals = self.transactionRepository.transactionsPieChart(user_id)

            if not cats_and_totals:
                return {'message': 'No transactions found for the user'}, 404

            categories_list = [{'category': category, 'total': total} for
                                 category, total in cats_and_totals]

            return categories_list, 200
        except Exception as e:
            return {'error': str(e)}, 500