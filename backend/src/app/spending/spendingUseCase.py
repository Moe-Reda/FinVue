from .spendingRepository import SpendingRepository


class SpendingUseCase:
    spendingRepository = SpendingRepository()

    def fetchSpendings(self, username):
        try:
            user_id_result = self.spendingRepository.getUserId(username)
            if user_id_result is None:
                return {'message': 'Username not found'}, 404
            user_id = user_id_result[0]
        except Exception as e:
            return {'error': str(e)}, 500

        try:
            spendings = self.spendingRepository.fetchSpendings(user_id)

            if not spendings:
                return {'message': 'No transactions found for the user'}, 404

            spendings_dic = {'day':[], 'amount':[]}

            for day, amount in spendings:
                spendings_dic['day'].append(day.strftime('%Y-%m-%d'))
                spendings_dic['amount'].append(amount)


            return spendings_dic, 200
        except Exception as e:
            return {'error': str(e)}, 500
