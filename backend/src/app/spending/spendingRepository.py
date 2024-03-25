from datetime import datetime

import pymysql


class SpendingRepository:
    mysql_host = '184.148.137.52'
    mysql_user = 'ProjectFinance'
    mysql_password = 'Finance@2003'
    mysql_db = 'finvue'

    # Connect to MySQL
    db = None
    cursor = None

    def fetchSpendings(self, user_id):
        self.db = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                                  password=self.mysql_password,
                                  db=self.mysql_db)
        self.cursor = self.db.cursor()
        spendings_query = "SELECT DATE(created_at) AS date, SUM(amount) AS " \
                          "amount FROM transactions WHERE user_id = %s GROUP " \
                          "BY DATE(created_at) ORDER BY DATE(created_at);"
        self.cursor.execute(spendings_query, (user_id,))
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
