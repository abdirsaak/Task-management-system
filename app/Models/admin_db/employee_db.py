from app import app
import mysql.connector
from app.DB_Configration import MyConfiguration


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





class Dashboard:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    
    # .......... total todos by employee

    def get_total_todo_emp(self, empl_name):

        sql = "select  count(*) from todo WHERE emp_name = %s"

        try:
            self.cursor.execute(sql, (empl_name))
            get_total_emp_todo = self.cursor.fetchone()


            if get_total_emp_todo:
                print(f'get_total_emp_todo: {get_total_emp_todo}')
                return get_total_emp_todo
            
            else:
                return []
    


        except Exception as e:
            print(f'erro geting get_total_todo_emp: {e}')
            return False