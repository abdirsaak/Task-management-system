from app import app

from flask import Flask, render_template, request, redirect, url_for,session,flash
from app.DB_Configration import MyConfiguration
from app.Models.admin_db.admin_db import  Database
from app.Models.admin_db.issue_db import Issue
from app.Models.admin_db.admin_db import Features
from app.Models.admin_db.admin_db import Tasks
from app.Models.admin_db.employee_db import Dashboard

from app.Models.admin_db.admin_db import  Admin


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
empl_dashbaord = Dashboard(mysql_connect.connection)
# Create a Todo instance and use the connection
feature_ob = Features(mysql_connect.connection)
issue_ob = Issue(mysql_connect.connection)

# ............. employee dashbaord

@app.route('/login/employee/dashboard')
def employee_dashbaord():
    if session.get('emp_email'):
        emp_email = session.get("emp_email")
        get_emp_name = admin_object.get_emp_name(emp_email)

        get_total_todo_emp = empl_dashbaord.get_total_todo_emp(get_emp_name)

        print(f'total todo employee: {get_total_todo_emp}')

        return render_template('./employee/emplo_dashbaord.html', total_todo = get_total_todo_emp)
    else:
        return redirect(url_for('login'))





@app.route('/login/employee/todo', methods = ['GET', 'POST'])
def employee_todo():
     if session.get('emp_email'):
        emp_email = session.get('emp_email')
# .......... waan soo helnay emp name
        get_emp_name = admin_object.get_emp_name(emp_email)
        # ........... 

        get_all_emp_todos = task_ob.get_emp_todo(get_emp_name)
        
        if 'make_complete_task' in request.form:
            task_id = request.form.get('task_id')
            task_status = request.form.get('task_status')
            print(f'task_complete id : {task_id}')
            print(f'task_status id : {task_status}')

            make_complete_task = task_ob.make_complete_todo(task_id,task_status)

            if make_complete_task:
                print(f'maked status completed')
                # return redirect(url_for('employee_todo'))
                return render_template('./employee/emplo_todo.html', emp_todos = get_all_emp_todos)
            else:
                print('érror aya jiro')
                # return redirect(url_for('employee_todo'))
                return render_template('./employee/emplo_todo.html', emp_todos = get_all_emp_todos)


        if get_all_emp_todos:
            print(f'value of emp_todo: {get_all_emp_todos}')
            return render_template('./employee/emplo_todo.html', emp_todos = get_all_emp_todos)
        else:
            print('error aya jiro get emp_todos ')
            # return redirect(url_for('employee_todo'))
            return render_template('./employee/emplo_todo.html', emp_todos = get_all_emp_todos)

        # print(f'value of emp_name from employe todo : {get_emp_name}')
        # return render_template('./employee/emplo_todo.html')
     else:
        return redirect(url_for('login'))





# @app.route('/login/employee/feature')
# def employee_feature():
#     if session.get('emp_email'):
#          return render_template('./employee/emplo_feature.html')
#     else:
#         return redirect(url_for('login'))




# @app.route('/login/employee/issue')
# def employee_issue():
#     if session.get('emp_email'):
        
#         return render_template('./employee/emplo_issue.html')
#     else:
#         return redirect(url_for('login'))
    



@app.route('/login/employee/issue', methods = ['GET', 'POST'])
def employee_issue():
    if session.get('emp_email'):

        if 'create_issue' in request.form:
            issue_name = request.form.get('issue_name')
            issue_desc = request.form.get('issue_desc')
            issue_priority = request.form.get('issue_priority')
            customer_name = request.form.get('customer_name')

            print(f'issue name: {issue_name}')
            print(f'issue desc: {issue_desc}')
            print(f'issue priori: {issue_priority}')
            print(f'csutomer name: {customer_name}')
            create_issue = issue_ob.create_issue(issue_name,issue_desc ,issue_priority,customer_name)

            if create_issue:
                print('create success issue')

                return redirect(url_for('employee_issue'))
            else:

                print('error aya dhacy issue')
                return redirect(url_for('employee_issue'))
        elif 'update_issue' in request.form:
            issue_id = request.form.get('issue_id')
            issue_name = request.form.get('issue_name')
            issue_desc = request.form.get('issue_desc')
            issue_priority = request.form.get('issue_priority')
            customer_name = request.form.get('customer_name')
            

            update_issue = issue_ob.update_issue(issue_name,issue_desc,issue_priority,customer_name,issue_id)


            if update_issue:

                print('updated success')
                return redirect(url_for('employee_issue'))
            else:
                print('updated failed')
                return redirect(url_for('employee_issue'))
        elif 'delete_issue' in request.form:
            issue_id = request.form.get('issue_id')

            print(f'issue id delete : {issue_id}')

            delete_issue = issue_ob.delete_issue(issue_id)
            if delete_issue:
                print('deleted success')
                return redirect(url_for('employee_issue'))
            else:
                print('delete failiere')
                return redirect(url_for('employee_issue'))



        get_all_issue = issue_ob.display_issue()


        return render_template('./employee/emplo_issue.html', get_issues = get_all_issue)
    else:
        return redirect(url_for('login'))
        
    



@app.route('/login/employee/feature', methods = ['GET', 'POST'])
def employee_feature():
    if session.get('emp_email'):

        if 'create_feature' in request.form:
            feature_name = request.form.get('feature_name')
            feature_desc = request.form.get('feature_desc')

           

            create_feature = feature_ob.create_feature(feature_name,feature_desc)

            if create_feature:
                print('succefuly created')
                return redirect(url_for('employee_feature'))
            else:
                print('error aya dhacay')
                return redirect(url_for('employee_feature'))
            
        elif 'update_feature' in request.form:
            feature_id = request.form.get('feature_id')
            feature_name = request.form.get('feature_name')
            feature_desc = request.form.get('feature_desc')


            update_feature = feature_ob.update_feature(feature_name,feature_desc,feature_id)
            if update_feature:
                print('updated success')
                return redirect(url_for('employee_feature'))
            else:
                print('updated error')
                return redirect(url_for('employee_feature'))
        elif 'delete_feature' in request.form:
            feature_id = request.form.get('feature_id')

            delete_feature = feature_ob.delete_feature(feature_id)

            if delete_feature:
                print('deleted success')
                return redirect(url_for('employee_feature'))
            else:
                print('delete feature error')
                return redirect(url_for('employee_feature'))


        
            
        get_all_features = feature_ob.display_features()

        
        return render_template('./employee/emplo_feature.html', get_features = get_all_features)

    else:
        return redirect(url_for('login'))



@app.route('/login/employee/profile')
def employee_profile():
    if session.get('emp_email'):

        # ........ get all employees
        employee_email   = session.get('emp_email')

        get_empl_profile = admin_object.get_employe_profile(employee_email)


        return render_template('./employee/emplo_profile.html', emo_profile = get_empl_profile)
    else:
        return redirect(url_for('login'))


@app.route('/login/employee/profile/logout')
def employee_logout():
    if session.get('emp_email'):
        session.pop('emp_email', None)

        return redirect(url_for('login'))
    else: 
        return redirect(url_for('login'))


