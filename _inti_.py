from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

app = Flask(__name__)
admin=Admin(app)
admin.add_view(ModelView(User, db.session))

app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models

