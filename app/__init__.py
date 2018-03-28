from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_cors import CORS
 
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://evalua:evalua@localhost:5432/evalua'
db = SQLAlchemy(app)
 
from app.catalog.views import catalog
app.register_blueprint(catalog)

from app.admin.master.interest import bpInterest
app.register_blueprint(bpInterest)

from app.admin.master.table_columns_and_length import bpTableColumnLength
app.register_blueprint(bpTableColumnLength)

from app.admin.master.admin import bpAdmin
app.register_blueprint(bpAdmin)

from app.admin.master.admin_history import bpAdminHistory
app.register_blueprint(bpAdminHistory)
 
db.create_all()
