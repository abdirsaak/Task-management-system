from app import app

from flask import Flask, render_template, request, redirect, url_for,session,flash
from app.DB_Configration import MyConfiguration
from app.Models.admin_db.admin_db import  Database

from app.Models.admin_db.admin_db import Tasks
from app.Models.admin_db.Dashboard_db import Dashboard

from app.Models.admin_db.admin_db import  Admin
from werkzeug.utils import secure_filename
import os
import uuid
from flask_bcrypt import Bcrypt

import smtplib
from email.mime.text import MIMEText


bycript = Bcrypt()

STATIC_FOLDER = os.path.abspath('app/static')
UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'emp_images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app.config["SECRET_KEY"] = "abdi@12"

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Helper Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



my_configuration = MyConfiguration()
mysql_connect = Database(
    host=my_configuration.DB_HOSTNAME,
    port=3306,
    user=my_configuration.DB_USERNAME,
    password=my_configuration.DB_PASSWORD,
    database=my_configuration.DB_NAME
)
mysql_connect.make_connection()



# Create a Todo instance and use the connection
admin_object = Admin(mysql_connect.connection)


task_ob = Tasks(mysql_connect.connection)

dashboard_ob  =Dashboard(mysql_connect.connection)




@app.route('/', methods = ['GET', 'POST'])
def login():
    if session.get('admin_email'):
        return redirect(url_for('dashbaord'))
    elif session.get('emp_email'):
        return redirect(url_for('employee_dashbaord'))
    else:

        if request.method == 'POST':
            # ... inan helo email iyo password, chechbox admin
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role')
            print(f'value of role: {role}')

            if role == 'admin':
                # ka raadi table-ka admins
                make_login = admin_object.login(email,password)

            
                if make_login:
                    print(f'value of make_login: {make_login}')
                    session['admin_email']  = email
                    return redirect(url_for('dashbaord'))

                else:
                    flash('email or password incorrect')
                    return redirect(url_for('login'))

            else:
                
                #  ka raadi table ka employee
                make_employee_login = admin_object.emp_login(email,password)

                if make_employee_login:
                    session['emp_email'] = email
                    return redirect(url_for('employee_dashbaord'))
                else:
                    return redirect(url_for('login'))

            

        else:

            return render_template('./admin/login.html')
  
    return render_template('./admin/login.html')











@app.route('/login/dashboard')
def dashbaord():
    if session.get('admin_email'):
        total_emp  = dashboard_ob.get_total_employee()
        total_open_tasks = dashboard_ob.get_total_open_tasks()
        total_pending_tasks  = dashboard_ob.get_total_pending_tasks()
        total_complete_tasks  = dashboard_ob.get_total_complete_tasks()
        total_todo = dashboard_ob.get_total_todos()
        total_issue = dashboard_ob.get_total_issue()
        total_features = dashboard_ob.get_total_features()

        get_top_10_tasks = dashboard_ob.get_top_10_tasks()
        get_top_10_todo = dashboard_ob.get_top_10_todos()


       
        return render_template('./admin/dashboard.html',
                        total_employee = total_emp, total_open_task =  total_open_tasks,
                        total_pending_task  = total_pending_tasks, complete_tasks = total_complete_tasks,
                        total_todos = total_todo, total_issues = total_issue, total_feature =total_features,
                         top_10_tasks =  get_top_10_tasks,
                         top_10_todos = get_top_10_todo)
    else:
        return redirect(url_for('login'))

@app.route('/login/admin', methods = ['GET', 'POST'])
def register_admin():
    if session.get('admin_email'):
        if request.method == 'POST':
            if 'create_admin' in request.form:
                admin_name = request.form.get('admin_name')
                admin_email = request.form.get('admin_email')
                admin_pass = request.form.get('admin_pass')

                print(f'admin name: {admin_name}')
                print(f'admin name: {admin_email}')
                print(f'admin name: {admin_pass}')


                password_to_endcode = bycript.generate_password_hash(admin_pass).decode('utf-8')

                # /.. model amam fucnton register database
                admin_register  = admin_object.register_admin(admin_name,admin_email,password_to_endcode)

                print(f'registered success views: {admin_register}')
                return redirect(url_for('register_admin'))

            # ........... waa meesha laga update gareyn lahaa Admin

            elif 'update_id' in request.form:
                admin_name  =  request.form.get('admin_name')
                admin_email  =  request.form.get('admin_email')
                admin_pass  =  request.form.get('admin_pass')
                update_id  =  request.form.get('update_id')

                update_admin = admin_object.update_admins(admin_name,admin_email,admin_pass,update_id)

                print(f'updated admins success views: {update_admin}')
                return redirect(url_for('register_admin'))
                
                # waa meesha admin-ka laga tiri lahaa.
            elif 'delete_id' in request.form:
                admin_id   =  request.form.get('delete_id')

                delete_admin = admin_object.delete_admin(admin_id)

                print(f'si sax aya loo tiry: {delete_admin}')
                return redirect(url_for('register_admin'))
    else:
        return redirect(url_for('login'))
            
       




        # ... display all admins

    all_admins = admin_object.display_admins()


       
        

    return render_template('./admin/admins.html', admins = all_admins)

    
# ....... send emails
def send_email(emp_name,to, password):
    # Send an email with the password to the school
    msg = MIMEText(f'Your password is: {password} , booqo www.alqasimischool.com')
    print(f"passworka gmail: inside send_email() {password}")
    print(f"passworka gmail: inside send_email() {emp_name}")
    msg['Subject'] = 'Employee Registeration'
    msg['From'] = 'rasaaq883@gmail.com'
    msg['To'] = to

    # Connect to the external SMTP server
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()

    s.login('rasaaq883@gmail.com', 'gwxo swba qtxk qdzg')
    s.send_message(msg)
    s.quit()


@app.route('/login/employee', methods= ['GET', 'POST'])
def employee():
    if session.get('admin_email'):
        if request.method == 'POST':
           try:
                
                if 'create_emp' in request.form:

                    emp_name = request.form.get('emp_name')
                    emp_email = request.form.get('emp_email')
                    emp_pass = request.form.get('emp_pass')
                    emp_num = request.form.get('emp_num')
                    emp_address = request.form.get('emp_address')
                    emp_img = request.files['emp_img']

                    emp_password_to_encrpyt = bycript.generate_password_hash(emp_pass)

                    print(f'all values : {emp_name}{emp_email}{emp_pass}')
                    print(f'all values : {emp_num}{emp_address}{emp_img}')
                    # .... chech gareey all user input vlaues
                     # ...inan xaqiijino inuu yahay secure
                    if allowed_file(emp_img.filename):
                        filename1 = secure_filename(emp_img.filename)
                        extension1 = filename1.rsplit('.', 1)[1].lower()
                    
                 
                        unique_filename1 = f"{uuid.uuid4().hex}.{extension1}"
                        print(f'unique_filename1: {unique_filename1}')
                    
                        image_1_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename1)
                        

                        emp_img.save(image_1_path)
                    

                        register_emp = admin_object.register_employee(emp_name,emp_email,emp_password_to_encrpyt,emp_num,emp_address,unique_filename1)
                        print(f'value of register_emp: {register_emp}')
                        if register_emp:
                            flash('Employee created success')
                            # send_email(emp_name,emp_email,emp_pass)
                            print('registered employee views success')
                            return redirect(url_for('employee'))
                        else:
                            flash('Error Employee createting')
                            print('errro aya dhacy employee register viwes: ')
                            return redirect(url_for('employee'))
                elif 'update_emp' in request.form:
                    emp_name = request.form.get('emp_name')
                    emp_email = request.form.get('emp_email')
                    emp_pass = request.form.get('emp_pass')
                    emp_num = request.form.get('emp_num')
                    emp_address = request.form.get('emp_address')
                    emp_img = request.files['emp_img']

                    emp_id = request.form.get('emp_id')
                    emp_password_to_encrpyt = bycript.generate_password_hash(emp_pass)
                    

                    print(f'all values update : {emp_name}{emp_email}{emp_pass}')
                    print(f'all values update : {emp_num}{emp_address}{emp_img} {emp_id}')
                    # .... chech gareey all user input vlaues
                     # ...inan xaqiijino inuu yahay secure
                    if allowed_file(emp_img.filename):
                        filename1 = secure_filename(emp_img.filename)
                        extension1 = filename1.rsplit('.', 1)[1].lower()
                    
                 
                        unique_filename1 = f"{uuid.uuid4().hex}.{extension1}"
                        print(f'unique_filename1: {unique_filename1}')
                    
                        image_1_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename1)
                        

                        emp_img.save(image_1_path)

                        make_update = admin_object.update_employee(emp_name,emp_email,emp_pass,emp_num,emp_address,unique_filename1,emp_id)

                        if make_update:
                            flash('updated employee success')
                            print('si sax ayad u uodate gareysy employee views')
                            return redirect(url_for('employee'))
                        else:
                            flash('Error updating employee ')
                            return redirect(url_for('employee'))

                    
                elif 'delete_btn' in request.form:

                    emp_id = request.form.get('emp_id')
                    print(f'vlaue of emp_id delete: {emp_id}')
                    make_delete = admin_object.delete_employee(emp_id)

                    if make_delete:
                        flash('Deleted Employee success')
                        return redirect(url_for('employee'))
                    else:
                        flash('Error while Deleting Employee')
                        return redirect(url_for('employee'))
                    


           
           except Exception as e:
               print(f'errorregister employee viwes: {e}')
               return redirect(url_for('employee'))
        

        display_all_employee = admin_object.display_employee() 
        return render_template('./admin/employee.html',get_emp = display_all_employee)
    else:
        return redirect(url_for('login'))
        

@app.route('/login/todo', methods = ['GET', 'POST'])
def todo():
    if session.get('admin_email'):
        if "cancel_todo" in request.form: 
            todo_id = request.form.get('todo_id')
            print(f'value of todo id: {todo_id}')

            cancel_todo = task_ob.cancel_todo(todo_id)
            if cancel_todo:
                flash('Todo Canceled Success')
                print('success canceled todo')
                return redirect(url_for('todo'))
            else:
                print('error canceled todo')
                return redirect(url_for('todo'))
            

        get_todos = task_ob.get_todos()
        print(f'all todos values: {get_todos}')
        return render_template('./admin/todo.html', all_todos = get_todos)
    else:
        return redirect(url_for('login'))


# .............. what employee can have 








@app.route('/login/profile', methods = ['GET', 'POST'])
def profile():
    if session.get('admin_email'):
        admin_email = session.get('admin_email')
        print(f'session admin email is {admin_email}')

        
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')


            print(f'all profile values: {name}, {email}, {password}')
            password_to_hash = bycript.generate_password_hash(password)

            make_update_profile  =admin_object.update_admin_profile(name, email, password_to_hash,admin_email)

            if make_update_profile:
                session['admin_email']  = email
                flash('si sax ayad u update gareysy')
                return redirect(url_for('profile'))
            else:
                flash('error ayaa jiro')
                return redirect(url_for('profile'))                
        else:
            get_admin_profile = admin_object.get_admin_profile(admin_email)
            print(f'value of admin profile: {get_admin_profile}')

            return render_template('./admin/profile.html', admin_profile =get_admin_profile )
  


 
    else: 
        return redirect(url_for('login'))
    

@app.route('/login/logout')
def logout():
    if session.get('admin_email'):
        session.pop('admin_email', None)

        return redirect(url_for('login'))
    else: 
        return redirect(url_for('login'))




