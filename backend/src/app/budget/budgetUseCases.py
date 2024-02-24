from .budgetRepository import BudgetRepository
from datetime import datetime

class CreateBudget:
    budgetRepository = BudgetRepository()

    def createBudget(self, username, category, allowance, month_year):
        try:
            user_id_result = self.budgetRepository.getUserId(username)
            if user_id_result is None:
                return {'message': 'Username not found'}, 404
            user_id = user_id_result[0]
            date = datetime.strptime(month_year, "%Y-%m")
            self.budgetRepository.createOrUpdateBudget(user_id, category, allowance, date)
            return {'message': 'Budget created successfully'}, 201
        except Exception as e:
            return {'error': str(e)}, 500


class UpdateBudget:
    budgetRepository = BudgetRepository()

    def updateBudget(self, username, category, amount, month_year):
        try:
            user_id_result = self.budgetRepository.getUserId(username)
            if user_id_result is None:
                return {'message': 'Username not found'}, 404
            user_id = user_id_result[0]
            date = datetime.strptime(month_year, "%Y-%m")  # Assuming month_year is in 'YYYY-MM' format
            self.budgetRepository.createOrUpdateBudget(user_id, category, amount, date)
            return {'message': 'Budget updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500


class FetchBudget:
    budgetRepository = BudgetRepository()

    def fetchBudget(self, username, month_year):
        try:
            user_id_result = self.budgetRepository.getUserId(username)
            if user_id_result is None:
                return {'message': 'Username not found'}, 404
            user_id = user_id_result[0]
            date = datetime.strptime(month_year, "%Y-%m")

            budgets = self.budgetRepository.fetchBudgets(user_id, date)
            if not budgets:
                return {'message': 'No budget found for the user'}, 404

            total_allowance = 0
            total_spent = 0
            budget_data = []

            for budget in budgets:
                total_allowance += budget['allowance']
                total_spent += budget['spent']
                percentage_spent = (budget['spent'] / budget['allowance']) * 100 if budget['allowance'] > 0 else 0
                budget_data.append({
                    'category': budget['category'],
                    'allowance': budget['allowance'],
                    'spent': budget['spent'],
                    'remaining': budget['allowance'] - budget['spent'],
                    'percentage_spent': percentage_spent
                })
            overall_percentage_spent = (total_spent / total_allowance) * 100 if total_allowance > 0 else 0
            overall_budget = {
                'total_allowance': total_allowance,
                'total_spent': total_spent,
                'overall_remaining': total_allowance - total_spent,
                'overall_percentage_spent': overall_percentage_spent
            }

            return {'budgets': budget_data, 'overall_budget': overall_budget}, 200

        except Exception as e:
            return {'error': str(e)}, 500
