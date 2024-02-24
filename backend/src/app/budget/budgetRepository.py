# from database import Database
import pymysql
import datetime


class BudgetRepository:
    mysql_host = '184.148.137.52'
    mysql_user = 'ProjectFinance'
    mysql_password = 'Finance@2003'
    mysql_db = 'finvue'

    # Connect to MySQL
    db = None
    cursor = None


    def createOrUpdateBudget(self, user_id, category, allowance, date):
        # Check if a budget already exists for the month, if so, update it, otherwise create a new one
        try:
            self.db = None
            self.cursor = None
            self.db = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                                 password=self.mysql_password,
                                 db=self.mysql_db)
            self.cursor = self.db.cursor()
            query = """
            INSERT INTO budget (user_id, category, allowance, date)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE allowance = VALUES(allowance)
            """
            self.cursor.execute(query, (user_id, category, allowance, date))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            if self.db:
                self.db.close()
            


    def getSpentByCategory(self, user_id, category, start_date, end_date):
        try:
            self.db = None
            self.cursor = None
            self.db = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                                 password=self.mysql_password,
                                 db=self.mysql_db)
            self.cursor = self.db.cursor()
            query = """
            SELECT SUM(amount) FROM transactions
            WHERE user_id = %s AND category = %s AND created_at >= %s AND created_at < %s
            """
            self.cursor.execute(query, (user_id, category, start_date, end_date))
            spent = self.cursor.fetchone()[0] or 0.0
            return spent
        except Exception as e:
            raise e


    def fetchBudgets(self, user_id, month_year):
        try:
            self.db = None
            self.cursor = None
            self.db = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                                 password=self.mysql_password,
                                 db=self.mysql_db)
            self.cursor = self.db.cursor()
            start_date = datetime.datetime(month_year.year, month_year.month, 1)
            if month_year.month == 12:
                end_date = datetime.datetime(month_year.year + 1, 1, 1)
            else:
                end_date = datetime.datetime(month_year.year, month_year.month + 1, 1)

            query = "SELECT category, allowance FROM budget WHERE user_id = %s AND date = %s"
            self.cursor.execute(query, (user_id, start_date))
            budgets = self.cursor.fetchall()

            budget_data = []
            for category, allowance in budgets:
                spent = self.getSpentByCategory(user_id, category, start_date, end_date)
                budget_data.append({
                    'category': category,
                    'allowance': float(allowance),
                    'spent': spent
                })
            return budget_data
        except Exception as e:
            raise e
        finally:
            if self.db:
                self.db.close()

    def getUserId(self, username):
        self.db = None
        self.cursor = None
        self.db = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                             password=self.mysql_password,
                             db=self.mysql_db)
        self.cursor = self.db.cursor()
        user_id_query = "SELECT id FROM users WHERE username = %s LIMIT 1"
        self.cursor.execute(user_id_query, (username,))
        user_id_result = self.cursor.fetchone()
        if self.db:
            self.db.close()
        return user_id_result






