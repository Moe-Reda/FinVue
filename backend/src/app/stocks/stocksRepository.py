import pymysql


class StocksRepository:
    mysql_host = '184.148.137.52'
    mysql_user = 'ProjectFinance'
    mysql_password = 'Finance@2003'
    mysql_db = 'finvue'

    # Connect to MySQL
    db = pymysql.connect(host=mysql_host, user=mysql_user,
                         password=mysql_password,
                         db=mysql_db)
    cursor = db.cursor()

    def getUserId(self, username):
        user_id_query = "SELECT id FROM users WHERE username = %s LIMIT 1"
        self.cursor.execute(user_id_query, (username,))
        user_id_result = self.cursor.fetchone()
        return user_id_result

    def fetchAll(self, userid):
        fetch_all_query = "SELECT tick FROM stocks WHERE user_id = %s"
        self.cursor.execute(fetch_all_query, (userid,))
        stocks = self.cursor.fetchall()
        return stocks

    def addStock(self, tick, user_id, quantity, order):
        try:
            query = "INSERT INTO stocks (tick, user_id, quantity, torder) " \
                    "VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE quantity "\
                    "= quantity + %s, torder = torder + %s "
            self.cursor.execute(query, (
                tick, user_id, quantity, order, quantity, order))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def getStockQuantity(self, user_id, stock):
        quantity_query = "SELECT quantity FROM stocks WHERE user_id = %s AND " \
                         "tick = %sLIMIT 1 "
        self.cursor.execute(quantity_query, (user_id, stock))
        quantity = self.cursor.fetchone()
        return quantity
