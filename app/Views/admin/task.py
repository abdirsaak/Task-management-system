from app import app
from flask import Flask, render_template, redirect, request,session,url_for, flash


from app.Models.admin_db.admin_db import Tasks
from app.Models.admin_db.admin_db import Database
from app.DB_Configration import MyConfiguration
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
task_ob = Tasks(mysql_connect.connection)
admin_object = Admin(mysql_connect.connection)



# @app.route('/login/task', methods = ['GET', 'POST'])
# def task():
#     if session.get('admin_email'):
#         get_empl_names = admin_object.get_employee_names()
#         if 'create_task' in request.form:
#             # sameey new task
#             task_name = request.form.get('task_name')
#             task_status = request.form.get('task_status')
#             task_priority = request.form.get('task_priority')
#             task_description = request.form.get('task_description')

#             print(f"task Name: {task_name}, task_status: {task_status}, task_priorit: {task_priority}, task_description: {task_description}")

#             create_task = task_ob.create_task(task_name,task_status,task_priority,task_description)


#             if create_task:
#                 print('new task created success Views:')
                
#                 return redirect(url_for('task'))
            
#             else:
#                 print('error while creating new task views: ')
#                 return redirect(url_for('task'))
#         elif 'update_task' in request.form:

#             task_name = request.form.get('task_name')
#             task_status = request.form.get('task_status')
#             task_priority = request.form.get('task_priority')
#             task_description = request.form.get('task_description')

#             task_id  =request.form.get('task_id')

#             update_task = task_ob.update_task(task_name,task_status,task_priority,task_description,task_id)
#             if update_task:
#                 print('si sucess task')
#                 return redirect(url_for('task'))
#             else:
#                 print('errro aya jiro update task viwes')
#                 return redirect(url_for('task'))
#         elif 'delete_task' in request.form:
#             task_id = request.form.get('task_id')

#             delete_task = task_ob.delete_task(task_id)

#             if delete_task:
#                 print('deleted task success')
#                 return redirect(url_for('task'))
#             else:
#                 print('error delete task viwes')
#                 return redirect(url_for('task'))
#         elif 'assing_task' in request.form:
#             task_id = request.form.get('task_id')
#             emp_name = request.form.get('emp_name')
#             print(f'task_id assing: {task_id}')
#             print(f'emp name assing: {emp_name}')

#             assing_to = task_ob.assing_task(task_id, emp_name)

#             if assing_to:
#                 print('assigned to success')
#                 return redirect(url_for('task'))
#             else:
#                 print('error happned wheile assigning to')
#             return redirect(url_for('task'))
#         else:
#         # soo bandhig all tasks ka
#             all_tasks = task_ob.display_task()
        
#             print(f'value of employee in task: {get_empl_names}')

#             return render_template('./admin/task.html', get_tasks = all_tasks, employee_list = get_empl_names)
#     else:
#         return redirect(url_for('login'))




@app.route('/login/task', methods=['GET', 'POST'])
def task():
    if session.get('admin_email'):
        # Fetch fresh employee names every time the route is accessed
        get_empl_names = admin_object.get_employee_names()

        if request.method == 'POST':
            if 'create_task' in request.form:
                # Create new task
                task_name = request.form.get('task_name')
                task_status = request.form.get('task_status')
                task_priority = request.form.get('task_priority')
                task_description = request.form.get('task_description')

                print(f"Task Name: {task_name}, Status: {task_status}, Priority: {task_priority}, Description: {task_description}")

                create_task = task_ob.create_task(task_name, task_status, task_priority, task_description)

                if create_task:
                    flash('Task created Successfuly')
                    print('New task created successfully')
                else:
                    print('Error while creating new task')

                return redirect(url_for('task'))

            elif 'update_task' in request.form:
                # Update existing task
                task_name = request.form.get('task_name')
                task_status = request.form.get('task_status')
                task_priority = request.form.get('task_priority')
                task_description = request.form.get('task_description')
                task_id = request.form.get('task_id')

                update_task = task_ob.update_task(task_name, task_status, task_priority, task_description, task_id)
                
                if update_task:
                    flash('updated Task Success')
                    print('Task updated successfully')
                else:
                    print('Error while updating task')

                return redirect(url_for('task'))

            elif 'delete_task' in request.form:
                # Delete a task
                task_id = request.form.get('task_id')

                delete_task = task_ob.delete_task(task_id)

                if delete_task:
                    flash('Task Deleted Success')
                    print('Task deleted successfully')
                else:
                    print('Error while deleting task')

                return redirect(url_for('task'))

            elif 'assing_task' in request.form:
                # Assign task to employee
                task_id = request.form.get('task_id')
                emp_name = request.form.get('emp_name')

                print(f"Task ID to assign: {task_id}, Employee name: {emp_name}")

                assign_to = task_ob.assing_task(task_id, emp_name)

                if assign_to:
                    flash(f'Task assigned to {emp_name} ')
                    print('Task assigned successfully')
                else:
                    print('Error while assigning task')

                return redirect(url_for('task'))

        # Fetch and display all tasks
        all_tasks = task_ob.display_task()

        # Ensure employee names are fetched fresh for display
        get_empl_names = admin_object.get_employee_names()
        print(f"Employee List Passed to Template: {get_empl_names}")

        return render_template('./admin/task.html', get_tasks=all_tasks, employee_list=get_empl_names)

    else:
        return redirect(url_for('login'))
