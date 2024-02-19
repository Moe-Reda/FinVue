from .transactionRepository import TransactionRepository


class CreateTransaction:
    transactionRepository = TransactionRepository()

    def createTransaction(self, username, amount, category):
        try:
            user_id_result = self.transactionRepository.getUserId(username)
            if user_id_result is None:
                return {'message': 'Username not found'}, 404
            user_id = user_id_result[0]
        except Exception as e:
            return {'error': str(e)}, 500
        try:
            self.transactionRepository.createTransaction(user_id, amount, category)
            return {'message': 'Transaction created successfully'}, 201
        except Exception as e:
            return {'error': str(e)}, 500
