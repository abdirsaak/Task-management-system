from flask import Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = "abdi@12"


# .....meshan waxaan kusoo import gareyneynaa wixii views quseeya.
from .Views.admin import admin
from .Views.employee import employee
from .Views.admin import task
from .Views.admin import features
from .Views.admin import issue
# ...meshan waxaan kusoo import gareyneynaa wixii models quseeya.


from .Models.admin_db import admin_db
from .Models.admin_db import employee_db
from .Models.admin_db import issue_db
from .Models.admin_db import Dashboard_db