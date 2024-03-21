import pymysql


class CryptosRepository:
    mysql_host = '184.148.137.52'
    mysql_user = 'ProjectFinance'
    mysql_password = 'Finance@2003'
    mysql_db = 'finvue'

    # Connect to MySQL
    db = None
    cursor = None

    def getUserId(self, username):
        self.db = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                                  password=self.mysql_password,
                                  db=self.mysql_db)
        self.cursor = self.db.cursor()
        user_id_query = "SELECT id FROM users WHERE username = %s LIMIT 1"
        self.cursor.execute(user_id_query, (username,))
        user_id_result = self.cursor.fetchone()
        return user_id_result

    def fetchAll(self, userid):
        self.db = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                                  password=self.mysql_password,
                                  db=self.mysql_db)
        self.cursor = self.db.cursor()
        fetch_all_query = "SELECT tick FROM cryptos WHERE user_id = %s"
        self.cursor.execute(fetch_all_query, (userid,))
        cryptos = self.cursor.fetchall()
        return cryptos

    def addCrypto(self, tick, user_id, quantity, order):
        self.db = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                                  password=self.mysql_password,
                                  db=self.mysql_db)
        self.cursor = self.db.cursor()
        try:
            query = "INSERT INTO cryptos (tick, user_id, quantity, price) " \
                    "VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE quantity " \
                    "= quantity + %s, price = price + %s "
            self.cursor.execute(query, (
                tick, user_id, quantity, order, quantity, order))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def getCryptoQuantity(self, user_id, crypto):
        self.db = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                                  password=self.mysql_password,
                                  db=self.mysql_db)
        self.cursor = self.db.cursor()
        quantity_query = "SELECT quantity FROM cryptos WHERE user_id = %s AND " \
                         "tick = %sLIMIT 1 "
        self.cursor.execute(quantity_query, (user_id, crypto))
        quantity = self.cursor.fetchone()
        return quantity
