# from database import Database
import pymysql


class TransactionRepository:
    mysql_host = '184.148.137.52'
    mysql_user = 'ProjectFinance'
    mysql_password = 'Finance@2003'
    mysql_db = 'finvue'

    # Connect to MySQL
    db = None
    cursor = None

    def createTransaction(self, user_id, amount, category):
        self.db = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                                  password=self.mysql_password,
                                  db=self.mysql_db)
        self.cursor = self.db.cursor()
        try:
            query = "INSERT INTO transactions (amount, user_id, category) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (amount, user_id, category))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def fetchTransactions(self, user_id):
        self.db = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                                  password=self.mysql_password,
                                  db=self.mysql_db)
        self.cursor = self.db.cursor()
        transactions_query = "SELECT category, amount FROM transactions WHERE user_id = %s"
        self.cursor.execute(transactions_query, (user_id,))
        transactions = self.cursor.fetchall()
        return transactions

    def getUserId(self, username):
        self.db = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                                  password=self.mysql_password,
                                  db=self.mysql_db)
        self.cursor = self.db.cursor()
        user_id_query = "SELECT id FROM users WHERE username = %s LIMIT 1"
        self.cursor.execute(user_id_query, (username,))
        user_id_result = self.cursor.fetchone()
        return user_id_result

    def transactionsPieChart(self, user_id):
        self.db = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                             password=self.mysql_password,
                             db=self.mysql_db)
        self.cursor = self.db.cursor()
        transactions_query = "SELECT category, amount FROM transactions WHERE user_id = %s"
        self.cursor.execute(transactions_query, (user_id,))
        transactions = self.cursor.fetchall()
        # transactions is in format [ ("category1", amount1), ("category2", amount2)]
        #Get every unique category with their total amounts
        list_cats_amounts = {}
        for item in transactions:
            category = item[0]
            amount = item[1]
            if category not in list_cats_amounts:
                list_cats_amounts[category] = amount
            else:
                list_cats_amounts[category] += amount
        # add everything in a list of tups [('category1', total1),('category2', total2)]
        list_of_tups = []
        for category in list_cats_amounts:
            first = category
            second = list_cats_amounts[category]
            res = (first, second)
            list_of_tups.append(res)
        return list_of_tups

