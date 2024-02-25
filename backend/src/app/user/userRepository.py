#from database import Database
import pymysql


class UserRepository:
    mysql_host = '184.148.137.52'
    mysql_user = 'ProjectFinance'
    mysql_password = 'Finance@2003'
    mysql_db = 'finvue'

    # Connect to MySQL
    db = None
    cursor = None

    def getUserData(self, username, password):
        self.db = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                                  password=self.mysql_password,
                                  db=self.mysql_db)
        self.cursor = self.db.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        data = self.cursor.fetchone()
        return data

    def registerUser(self, email, username, password):
        self.db = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                                  password=self.mysql_password,
                                  db=self.mysql_db)
        self.cursor = self.db.cursor()
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (username, email, password))
        self.db.commit()

    def getUserId(self, username):
        self.db = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                                  password=self.mysql_password,
                                  db=self.mysql_db)
        self.cursor = self.db.cursor()
        user_id_query = "SELECT id FROM users WHERE username = %s LIMIT 1"
        self.cursor.execute(user_id_query, (username,))
        user_id_result = self.cursor.fetchone()
        return user_id_result
