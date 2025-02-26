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


    # ....... get total employee
    def get_total_employee(self):
        sql = "SELECT COUNT(*) AS Total_emp FROM employee;"
        try:
            self.cursor.execute(sql)

            total_employee = self.cursor.fetchone()

            if total_employee:
                print(f'value of total employee: {total_employee}')
                return total_employee
            else:
                return []

        except Exception as e:
            print(f'error total employee: {e}')
            return False
        

    # ....... get total open task
    def get_total_open_tasks(self):
        sql = "SELECT COUNT(*) AS Tota_open_task FROM tasks WHERE task_status= 'open' "
        try:
            self.cursor.execute(sql)

            total_epen_tasks = self.cursor.fetchone()

            if total_epen_tasks:
                print(f'value of total open tasks: {total_epen_tasks}')
                return total_epen_tasks
            else:
                return []

        except Exception as e:
            print(f'error total total_epen_tasks: {e}')
            return False

    # ....... get total pending task
    def get_total_pending_tasks(self):
        sql = "SELECT COUNT(*) AS Total_pending_task FROM tasks WHERE task_status= 'pending' "
        try:
            self.cursor.execute(sql)

            total_pending_tasks = self.cursor.fetchone()

            if total_pending_tasks:
                print(f'value of total total_pending_tasks: {total_pending_tasks}')
                return total_pending_tasks
            else:
                return []

        except Exception as e:
            print(f'error total total_pending_tasks: {e}')
            return False
        
        # ................ get total complete tasks
    def get_total_complete_tasks(self):
        sql = "SELECT COUNT(*) AS Total_complete_task FROM tasks WHERE task_status= 'completed' "
        try:
            self.cursor.execute(sql)

            total_complete_tasks = self.cursor.fetchone()

            if total_complete_tasks:
                print(f'value of total total_complete_tasks: {total_complete_tasks}')
                return total_complete_tasks
            else:
                return []

        except Exception as e:
            print(f'error total total_complete_tasks: {e}')
            return False
        
# .................. get total todos
    def get_total_todos(self):
        sql = "SELECT COUNT(*) AS Total_todos FROM todo "
        try:
            self.cursor.execute(sql)

            total_todo = self.cursor.fetchone()

            if total_todo:
                print(f'value of  total_todo: {total_todo}')
                return total_todo
            else:
                return []

        except Exception as e:
            print(f'error  total_todo: {e}')
            return False
# .................. get total issue
    def get_total_issue(self):
        sql = "SELECT COUNT(*) AS total_issue FROM issue "
        try:
            self.cursor.execute(sql)

            total_issue = self.cursor.fetchone()

            if total_issue:
                print(f'value of  total_issue: {total_issue}')
                return total_issue
            else:
                return []

        except Exception as e:
            print(f'error  total_issue: {e}')
            return False
# .................. get total features
    def get_total_features(self):
        sql = "SELECT COUNT(*) AS total_features FROM features "
        try:
            self.cursor.execute(sql)

            total_features = self.cursor.fetchone()

            if total_features:
                print(f'value of  total_features: {total_features}')
                return total_features
            else:
                return []

        except Exception as e:
            print(f'error  total_features: {e}')
            return False
        
    # ............. get top 10 tasks

    def get_top_10_tasks(self):



        sql = "select * from tasks order by created_date desc  limit 10;"

        try: 
            self.cursor.execute(sql)

            get_top_10_tasks = self.cursor.fetchall()

            if get_top_10_tasks:
                print(f'value of top 10 tasks: {get_top_10_tasks}')
                return get_top_10_tasks
            
            else:
                return []

        except Exception as e:
            print(f'error top 10 tasks: {e}')

            return False
        
    def get_top_10_todos(self):



        sql = """   
            SELECT todo.emp_name,
            tasks.task_name,
            tasks.task_status,
            tasks.task_priority   from   todo 
            inner join tasks 
            on todo.task_id = tasks.id 
            order by todo.created_date 
            desc  limit 10;
        """

        try: 
            self.cursor.execute(sql)

            get_top_10_todo = self.cursor.fetchall()

            if get_top_10_todo:
                print(f'value of top 10 todo: {get_top_10_todo}')
                return get_top_10_todo
            
            else:
                return []

        except Exception as e:
            print(f'error top 10 todo: {e}')

            return False
  