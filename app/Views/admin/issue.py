from app import app
from flask import Flask, render_template, redirect, request,session,url_for, flash

from app.Models.admin_db.issue_db import Issue

from app.Models.admin_db.admin_db import Database
from app.DB_Configration import MyConfiguration




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
issue_ob = Issue(mysql_connect.connection)


@app.route('/login/issue', methods = ['GET', 'POST'])
def issue():
    if session.get('admin_email'):

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
                flash('Issue Created success')
                print('create success issue')

                return redirect(url_for('issue'))
            else:

                print('error aya dhacy issue')
                return redirect(url_for('issue'))
        elif 'update_issue' in request.form:
            issue_id = request.form.get('issue_id')
            issue_name = request.form.get('issue_name')
            issue_desc = request.form.get('issue_desc')
            issue_priority = request.form.get('issue_priority')
            customer_name = request.form.get('customer_name')
            

            update_issue = issue_ob.update_issue(issue_name,issue_desc,issue_priority,customer_name,issue_id)


            if update_issue:
                flash('Issue Updated success')
                print('updated success')
                return redirect(url_for('issue'))
            else:
                print('updated failed')
                return redirect(url_for('issue'))
        elif 'delete_issue' in request.form:
            issue_id = request.form.get('issue_id')

            print(f'issue id delete : {issue_id}')

            delete_issue = issue_ob.delete_issue(issue_id)
            if delete_issue:
                flash('Deleted issue success')
                print('deleted success')
                return redirect(url_for('issue'))
            else:
                print('delete failiere')
                return redirect(url_for('issue'))



        get_all_issue = issue_ob.display_issue()


        return render_template('./admin/issue.html', get_issues = get_all_issue)
    else:
        return redirect(url_for('login'))
        