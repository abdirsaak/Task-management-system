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




# fetch all (all rows)

# fetchone (one row)


class Admin:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
    

    # ... register admin:
    def register_admin(self,admin_name, admin_email, admin_password):
        sql  =  'INSERT INTO admins(admin_name,admin_email,admin_password)  VALUES (%s,%s,%s)'

        try:
            self.cursor.execute(sql, (admin_name, admin_email, admin_password))
            self.connection.commit()
            return 'si sax ayad u diiwan gelisay admin'

        except Exception as e:
            print(f'eror while registering admin')
            return False
        

    # .... display admins



    def display_admins(self):
        sql = 'SELECT * FROM admins'

        try:
            self.cursor.execute(sql)

            get_admins  =  self.cursor.fetchall()


            if get_admins:
                print(f'all admins db: {get_admins}')
                return get_admins
            else:
                print('mala soo helin admins')
                return False


        except Exception as e:
            print(f'eror while display admins')


    def get_admin_profile(self, admin_email):
        if not admin_email:
            print('Admin email is not provided.')
            return []

        sql = 'SELECT admin_name, admin_email, admin_password FROM admins WHERE admin_email = %s'

        try:
            self.cursor.execute(sql, (admin_email,))
            get_admins = self.cursor.fetchall()

            if get_admins:
                print(f'All admin profiles: {get_admins}')
                return get_admins
            else:
                print('No admin profile found for the given email.')
                return []
        except Exception as e:
            print(f'Error while displaying admin profile: {e}')
            return []




            
    def update_admin_profile(self, admin_name,admin_email,admin_password,admin_session_email):
        sql = """UPDATE admins SET admin_name = %s,
          admin_email = %s,
         admin_password = %s
         WHERE admin_email = %s
         """
        

        try:
            self.cursor.execute(sql, ( admin_name,admin_email,admin_password, admin_session_email))

            self.connection.commit()
            print('waa la badaly')
            return True


        except Exception as e:
            print(f'error while updating admin profile: {e}')
            return False

        

    # def get_admin_profile(self, admin_email):
    #     print(f'admin aemail: {admin_email}')
    #     sql = 'SELECT admin_name,admin_email, admin_password FROM admins WHERE admin_email = %s'

    #     try:
    #         self.cursor.execute(sql, (admin_email))

    #         get_profile_info  = self.cursor.fetchall()
    #         print(f'admin profile value: {get_profile_info}')

    #         if get_profile_info:
    #             return get_profile_info
    #         else:
    #             return []

    #     except Exception as e:
    #         print(f'error while getting admin profile')


    # .... delete admin

    def  delete_admin(self, admin_id):
        sql = 'DELETE FROM admins WHERE id = %s'

        try:
            self.cursor.execute(sql, (admin_id,))
            self.connection.commit()

            return 'si sax ayad u delete gareyey'


        except Exception as e:
            print(f'error while delete admin: {e}')
            return False




    # .... update admins


    def update_admins(self,admin_name,admin_email,admin_password,admin_id):
        sql = 'UPDATE admins SET admin_name = %s, admin_email = %s,admin_password = %s WHERE id = %s'

        try:
            self.cursor.execute(sql, (admin_name,admin_email,admin_password,admin_id))
            self.connection.commit()

            return 'si sax ayad u update gareysy'


        except Exception as e:
            print(f'error while update admin: {e}')
            return False
    # login
    
    
    def login(self, email, password):
        sql = ' SELECT admin_email, admin_password FROM admins WHERE admin_email = %s '

        try:
            self.cursor.execute(sql, ( email,))
            make_login = self.cursor.fetchall()


            get_encrpted_password= make_login[0][1]
            if get_encrpted_password:
                print(f'encrpt password database: {get_encrpted_password}')
                print(f'user password : {password}')

                # .. ecnptry to decrpt

                encrpt_password_dectrypass =  bycrpt.check_password_hash(get_encrpted_password, password)
                print(f'value of encrpt_password_dectrypass: {encrpt_password_dectrypass}')

                if encrpt_password_dectrypass:
                    print('login success')
                    return make_login
                else:
                    print('login denied')
                    return False



           

        except Exception as e:
            print(f'error while login')
            return False
        
        
    def emp_login(self, email, password):
        sql = ' SELECT emp_email, emp_password FROM employee WHERE emp_email = %s '

        try:
            self.cursor.execute(sql, ( email,))
            make_login = self.cursor.fetchall()


            get_encrpted_password= make_login[0][1]
            if get_encrpted_password:
                print(f'encrpt password database: {get_encrpted_password}')
                print(f'user password : {password}')

                # .. ecnptry to decrpt

                encrpt_password_dectrypass =  bycrpt.check_password_hash(get_encrpted_password, password)
                print(f'value of encrpt_password_dectrypass: {encrpt_password_dectrypass}')

                if encrpt_password_dectrypass:
                    print('login success')
                    return make_login
                else:
                    print('login denied')
                    return False



           

        except Exception as e:
            print(f'error while login')
            return False
    

    def get_emp_name(self, emp_email):
        sql = "SELECT emp_name FROM employee WHERE emp_email = %s"


        try:
            self.cursor.execute(sql, (emp_email,))
            get_emp_name = self.cursor.fetchone()

            if get_emp_name:

                return get_emp_name
            
            else:
                return []
            

        except Exception as e:
            print(f'error while get_emp_name: {e}')

            return False


       # ........... register employee
        
    def register_employee(self,emp_name, emp_email, emp_password,emp_number,emp_address,emp_img):
        sql  =  'INSERT INTO employee(emp_name, emp_email, emp_password,emp_number,emp_address,emp_img)  VALUES (%s,%s,%s,%s,%s,%s)'

        try:
            print(f'all values DB : {emp_name}{emp_email}{emp_address}')
            print(f'all values DB : {emp_number}{emp_address}{emp_img}')
            self.cursor.execute(sql, (emp_name, emp_email, emp_password,emp_number,emp_address,emp_img))
            self.connection.commit()
            return True

        except Exception as e:
            print(f'eror while registering employee: {e}')
            return False
        

    
    def display_employee(self):
        sql = 'SELECT * FROM employee'

        try:
            self.cursor.execute(sql)

            get_employees  =  self.cursor.fetchall()


            if get_employees:
                # print(f'all employee db: {get_employees}')
                return get_employees
            else:
                return []

          


        except Exception as e:
            print(f'eror while display empoyee')

    # def get_employee_names(self):


        sql = 'SELECT emp_name FROM employee'

        try:
            self.cursor.execute(sql)
            get_emp_names = self.cursor.fetchall()

            print(f'all employee names db: {get_emp_names}')
            if get_emp_names:
                return get_emp_names
            else:
                return []

        except Exception as e:
            print(f'error get employee names db: {e}')
            return False

    def get_employee_names(self):
        sql = 'SELECT id, emp_name FROM employee'
        try:
        
            self.cursor.execute(sql)
            get_emp_names = self.cursor.fetchall()
            print(f'all employee names from the database: {get_emp_names}')
            if get_emp_names:
                return get_emp_names
            else:
                return '[]'
        except Exception as e:
            print(f'Error fetching employee names from the database: {e}')
            return []
    



  
    def update_employee(self, emp_name,emp_email,emp_password,emp_number,emp_address,emp_img, emp_id):
        sql = "UPDATE employee SET emp_name = %s,emp_email = %s,emp_password = %s,emp_number = %s,emp_address = %s, emp_img = %s WHERE id = %s"

        try:
            self.cursor.execute(sql, (emp_name,emp_email,emp_password,emp_number,emp_address,emp_img, emp_id))

            self.connection.commit()
            print('db si sax ayad u update gareysy EMployee')

            return True

        except Exception as e:
            print(f'erro update Emp DB: {e}')

            return False

    def delete_employee(self, emp_id):
        sql = "DELETE FROM employee WHERE id   =%s"
        try:
            self.cursor.execute(sql,(emp_id,) )
            self.connection.commit()

            print('si sax ayad u tirty employee db')
            return True

        except Exception as e:
            print(f'error delete employee db: {e}')
            return False
    
    def get_employe_profile(self, em_email):
        if not em_email:
            print('employee email is not provided.')
            return []

        sql = 'SELECT emp_name, emp_email,emp_number,emp_address,emp_img FROM employee WHERE emp_email = %s'

        try:
            self.cursor.execute(sql, (em_email,))
            get_employee = self.cursor.fetchall()

            if get_employee:
                print(f'All employee profiles: {get_employee}')
                return get_employee
            else:
                print('No employe profile found for the given email.')
                return []
        except Exception as e:
            print(f'Error while displaying employee profile: {e}')
            return []
    

   



class Tasks:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
    


    # ....Creating new task

    def create_task(self, task_name, task_status, task_priority,task_description):
        sql = "INSERT INTO tasks( task_name, task_status, task_priority,task_description) VALUE (%s,%s,%s,%s)"


        try:
            # .... execute
            self.cursor.execute(sql, (task_name, task_status, task_priority,task_description))
            self.connection.commit()

            return True

        except Exception as e:
            print(f'error while creating new task DB: {e}')
            return False
        
    def display_task(self):
        sql = 'SELECT * FROM tasks'

        try:
            self.cursor.execute(sql)

            get_all_task  = self.cursor.fetchall()
            print(f'all value task admin: {get_all_task}')
            if get_all_task:
                return get_all_task

            else:
                return []


        except Exception as error:
            print(f'error aya jiro displaying tasks: {error}')

            return False      
        
    

    def update_task(self,task_name, task_status, task_priority,task_description, task_id):

        sql   = "UPDATE tasks SET task_name = %s, task_status = %s, task_priority = %s, task_description = %s WHERE id  = %s"
        

        try:
            self.cursor.execute(sql, (task_name, task_status, task_priority,task_description, task_id))
            self.connection.commit()

            return True

        except Exception as e:
            print(f'error updating task DB: {e}')
            return False

    def delete_task(self, task_id):

        sql = 'DELETE FROM tasks WHERE id = %s'

        try:
            self.cursor.execute(sql, (task_id,))
            self.connection.commit()

            return True

        except Exception as e:
            print(f'error deleting task : {e}')
            return False
        
    

    def assing_task(self, task_id, emp_name):
        sql = "INSERT INTO todo(task_id,emp_name) values (%s, %s)"

        try:
            self.cursor.execute(sql, (task_id, emp_name))
            self.connection.commit()
            return True
        

        except Exception as e:
            print(f'error assign task db: {e}')
            return False
        
    def get_todos(self):
        sql = """
                 SELECT todo.task_id, tasks.task_name,
                    tasks.task_status,
                     tasks.task_priority ,todo.emp_name
                    from tasks
                     join  todo 
                      on tasks.id = todo.task_id;
    """
        try:
            self.cursor.execute(sql)
            all_todos = self.cursor.fetchall()

            if all_todos:
                return all_todos
            else:
                return []

        except Exception as e:
            print(f'error get todos: {e}')
            return False      


    def get_emp_todo(self, emp_name):
        sql = """

                SELECT todo.task_id, tasks.task_name,
                    tasks.task_status,
                     tasks.task_priority ,todo.emp_name
                    from tasks
                     join  todo 
                      on tasks.id = todo.task_id WHERE todo.emp_name = %s;
        """

        try:
            self.cursor.execute(sql, (emp_name))

            get_emp_todos =  self.cursor.fetchall()


            if get_emp_todos:

                return get_emp_todos
            else:
                return []

            pass

        except Exception as e:
            print(f'error get_emp_todo: {e}')

            return False
    
       
    def cancel_todo(self, id):
        print(f'value of todo id db: {id}')

        sql = 'DELETE FROM todo WHERE task_id  = %s'

        try: 
            self.cursor.execute(sql, (id,))
            self.connection.commit()

            return True
        

        except Exception as e:
            print(f'error cancel todo db: {e}')
            return False

    def make_complete_todo(self, task_id, task_status):
        sql  =  "UPDATE tasks SET task_status = %s WHERE id = %s "

        try:
            self.cursor.execute(sql, (task_status,task_id))
            self.connection.commit()
            return True
        except Exception as e:
            print(f'error while make complete task: {e}')
            return False
        



class Features:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
    

    # ... creating a new feture
    def create_feature(self, feature_name,feature_desc):

        sql = "INSERT INTO features(feature_name,feature_desc) values (%s,%s)"

        try:
            self.cursor.execute(sql, (feature_name,feature_desc))

            self.connection.commit()
            return True
        

        except Exception as e:
            print(f'error while creating features')
            return False
        
    

    # // display features

    def display_features(self):
        sql = "SELECT * FROM features"
        try:

            self.cursor.execute(sql)

            get_all_features = self.cursor.fetchall()


            if get_all_features:
                return get_all_features
            else:
                return []

            


        except Exception as e:
            print(f'error display featrues: {e}')

            return False        

    # ........update features
    def update_feature(self, feature_name,feature_desc, feature_id):
        sql = "UPDATE features SET feature_name = %s, feature_desc = %s WHERE id = %s"

        try:
            self.cursor.execute(sql,(feature_name,feature_desc, feature_id))
            self.connection.commit()

            return True


        except Exception as e:
            print(f'errror while updating featrues: {e}')
            return False
    def delete_feature(self, feature_id):

        sql = "DELETE FROM features WHERE id  = %s"

        try:
            self.cursor.execute(sql, (feature_id,))
            self.connection.commit()

            return True
            

        except Exception as e:
            print(f'error deleteing feature')

            return False








  

    

   
    

    