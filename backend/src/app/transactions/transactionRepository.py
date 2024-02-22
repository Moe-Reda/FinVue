# from database import Database
import pymysql


class TransactionRepository:
    mysql_host = '184.148.137.52'
    mysql_user = 'ProjectFinance'
    mysql_password = 'Finance@2003'
    mysql_db = 'finvue'

    # Connect to MySQL
    db = pymysql.connect(host=mysql_host, user=mysql_user,
                         password=mysql_password,
                         db=mysql_db)
    cursor = db.cursor()

    def createTransaction(self, user_id, amount, category):
        try:
            query = "INSERT INTO transactions (amount, user_id, category) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (amount, user_id, category))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def fetchTransactions(self, user_id):
        transactions_query = "SELECT category, amount FROM transactions WHERE user_id = %s"
        self.cursor.execute(transactions_query, (user_id,))
        transactions = self.cursor.fetchall()
        return transactions

    def getUserId(self, username):
        user_id_query = "SELECT id FROM users WHERE username = %s LIMIT 1"
        self.cursor.execute(user_id_query, (username,))
        user_id_result = self.cursor.fetchone()
        return user_id_result
