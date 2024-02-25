from .transactionRepository import TransactionRepository


class FetchTransactions:
    transactionRepository = TransactionRepository()

    def fetchTransactions(self, username):
        try:
            user_id_result = self.transactionRepository.getUserId(username)
            if user_id_result is None:
                return {'message': 'Username not found'}, 404
            user_id = user_id_result[0]
        except Exception as e:
            raise e
            return {'error': str(e)}, 500

        try:
            transactions = self.transactionRepository.fetchTransactions(user_id)

            if not transactions:
                return {'message': 'No transactions found for the user'}, 404

            transactions_list = [{'category': category, 'amount': amount} for
                                 category, amount in transactions]

            return transactions_list, 200
        except Exception as e:
            raise e
            return {'error': str(e)}, 500
