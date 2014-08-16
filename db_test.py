import os
import os.path as op
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from wtforms import validators

from flask.ext import admin
from flask.ext.admin.contrib import sqla
from flask.ext.admin.contrib.sqla import filters


# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['DATABASE_FILE'] = 'skillsCluster.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class SkillPair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primary_term = db.Column(db.String(140))
    secondary_term = db.Column(db.String(140))
    number_of_times = db.Column(db.Integer)

    def __unicode__(self):
        return self.id


# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'



# Customized Post model admin
class SkillAdmin(sqla.ModelView):
    # Visible columns in the list view
    column_exclude_list = ['text']

    # List of columns that can be sorted. For 'user' column, use User.username as
    # a column.
    column_sortable_list = ('primary_term')

    column_filters = ('primary_term')

    def __init__(self, session):
        # Just call parent class with predefined model.
        super(SkillAdmin, self).__init__(SkillPair, session)


# Create admin
admin = admin.Admin(app, 'Simple Models')

# Add views
admin.add_view(SkillAdmin(db.session))



if __name__ == '__main__':
    # Build a sample db on the fly, if one does not exist yet.
    app_dir = op.realpath(os.path.dirname(__file__))
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
#    if not os.path.exists(database_path):
#        build_sample_db()

    # Start app
    app.run(debug=True)
