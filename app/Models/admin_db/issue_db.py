from app import app
import mysql.connector
from app.DB_Configration import MyConfiguration

from flask_bcrypt import Bcrypt


bycrpt = Bcrypt()


class Database:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def make_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            self.cursor = self.connection.cursor()
            print('si sax ayad ugu xirantay database-ka')
        except Exception as e:
            print('error ayaa jiro maku xirmin database-ka')
            print(e)

    def my_cursor(self):
        return self.cursor
    



class Issue:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    # ... create issue
    def create_issue(self,issue_name, issue_desc, issue_priority,customer_name):

        sql = "INSERT INTO issue (issu_name,issue_desc,issue_priority,customer_name) values (%s, %s, %s,%s)"

        try:

            self.cursor.execute(sql, (issue_name, issue_desc, issue_priority,customer_name))
            self.connection.commit()

            return True


        except Exception as e:
            print(f'error while creating issue')

            return False



    # dsiplay issue

    def display_issue(self):

        sql = "SELECT * FROM issue"


        try:

            self.cursor.execute(sql)

            get_all_issue = self.cursor.fetchall()


            if get_all_issue:
                return get_all_issue
            
            else:
                return []

        except Exception as e:
            print(f'error displying issue db: {e}')

            return False


    # update issue

    def update_issue(self, issue_name, issue_desc, issue_priorty, customer_name, issue_id):
        sql = "UPDATE issue SET issu_name = %s, issue_desc = %s,issue_priority  =%s,customer_name = %s WHERE id = %s"


        try:

            self.cursor.execute(sql, (issue_name, issue_desc, issue_priorty, customer_name, issue_id))
            self.connection.commit()

            return True
    

        except Exception as e:
            print(f'error update issue: {e}')

            return False

    

    def delete_issue(self, issue_id):
        sql = "DELETE FROM issue WHERE id  = %s"

        try:
            self.cursor.execute(sql, (issue_id,))

            self.connection.commit()

            return True


        except Exception as e:
            print(f'error while deleting isssue')





    # delete issue