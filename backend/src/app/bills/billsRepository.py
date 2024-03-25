# from database import Database
import pymysql
import datetime


class BillsRepository:
    mysql_host = '184.148.137.52'
    mysql_user = 'ProjectFinance'
    mysql_password = 'Finance@2003'
    mysql_db = 'finvue'

    # Connect to MySQL
    db = None
    cursor = None


    def createorupdateBill(self, user_id, bill_name, bill_amount, due_date, recurring, frequency):
        # Check if a budget already exists for the month, if so, update it, otherwise create a new one
        try:
            self.db = None
            self.cursor = None
            self.db = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                                 password=self.mysql_password,
                                 db=self.mysql_db)
            self.cursor = self.db.cursor()
            query = """
            INSERT INTO bills (user_id, bill_name, bill_amount, due_date, recurring, frequency)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            bill_name = VALUES(bill_name), 
            bill_amount = VALUES(bill_amount), 
            due_date = VALUES(due_date), 
            recurring = VALUES(recurring), 
            frequency = VALUES(frequency);
            """
            self.cursor.execute(query, (user_id, bill_name, bill_amount, due_date, recurring, frequency))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            if self.db:
                self.db.close()
                
    def fetchBills(self, user_id):
        try:
            self.db = None
            self.cursor = None
            self.db = pymysql.connect(host=self.mysql_host, user=self.mysql_user,
                                 password=self.mysql_password,
                                 db=self.mysql_db)
            self.cursor = self.db.cursor()
            query = "SELECT bill_name, bill_amount, due_date, recurring, frequency FROM bills WHERE user_id = %s"
            self.cursor.execute(query, (user_id))
            bills_array = self.cursor.fetchall()
            return bills_array
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