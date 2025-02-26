from app import app
from flask import Flask, render_template, redirect, request,session,url_for,flash

from app.Models.admin_db.admin_db import Features
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
feature_ob = Features(mysql_connect.connection)


@app.route('/login/feature', methods = ['GET', 'POST'])
def feature():
    if session.get('admin_email'):

        if 'create_feature' in request.form:
            feature_name = request.form.get('feature_name')
            feature_desc = request.form.get('feature_desc')

           

            create_feature = feature_ob.create_feature(feature_name,feature_desc)

            if create_feature:
                flash('Feature created Success')
                print('succefuly created')
                return redirect(url_for('feature'))
            else:
                print('error aya dhacay')
                return redirect(url_for('feature'))
            
        elif 'update_feature' in request.form:
            feature_id = request.form.get('feature_id')
            feature_name = request.form.get('feature_name')
            feature_desc = request.form.get('feature_desc')


            update_feature = feature_ob.update_feature(feature_name,feature_desc,feature_id)
            if update_feature:
                flash('Updated Feature success')
                print('updated success')
                return redirect(url_for('feature'))
            else:
                print('updated error')
                return redirect(url_for('feature'))
        elif 'delete_feature' in request.form:
            feature_id = request.form.get('feature_id')

            delete_feature = feature_ob.delete_feature(feature_id)

            if delete_feature:
                flash('Deted feature success')
                print('deleted success')
                return redirect(url_for('feature'))
            else:
                print('delete feature error')
                return redirect(url_for('feature'))


        
            
        get_all_features = feature_ob.display_features()

        
        return render_template('./admin/features.html', get_features = get_all_features)
    else:
        return redirect(url_for('login'))
