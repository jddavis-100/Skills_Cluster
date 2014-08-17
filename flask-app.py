__author__ = 'Christine'

import os
import os.path as op
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from wtforms import validators

from flask.ext import admin
from flask.ext.admin.contrib import sqla
from flask.ext.admin.contrib.sqla import filters, ModelView

import pprint
import sqlite3 as lite

from os import listdir

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['DATABASE_FILE'] = 'skillsClustertest.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class SkillPair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primary_term = db.Column(db.String(140))
    secondary_term = db.Column(db.String(140))
    number_of_times = db.Column(db.Integer)

    def __unicode__(self):
        return self.primary_term

class SkillView(ModelView):
    column_searchable_list = ("primary_term",)
    column_filters = ('primary_term',)

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(SkillView, self).__init__(SkillPair, session, **kwargs)

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


# Create admin
admin = admin.Admin(app, 'SkillCluster')

# Add views
admin.add_view(SkillView(db.session))


def build_db():

    db.drop_all()
    db.create_all()

    skillKeywords = ["AJAX", "AMQP", "Android", "ApacheMQ", "Artifactory", "ASP.NET", "Bootstrap",
                     "C++", "C#", "CSS", "Crystal Reports", "Delphi", "Django", "Eclipse", "Flash",
                     "GIS", "Git", "Hadoop", "Hibernate", "HTML", "HTML5", "J2EE", "Java", "Javascript",
                     "JBOSS", "JCE", "JDBC", "Jenkins", "JMS", "JNDI", "JPA", "JQuery", "JSON", "JUnit",
                     "LAMP", "Maven", "Memcached", "MongoDB", "MVC", "MySQL", ".NET", "Nose", "NUnit",
                     "Oracle", "Perl", "Photoshop", "PHP", "PostGIS", "Python", "RabbitMQ", "REST", "Ruby",
                     "Ruby on Rails", "Selenium", "Silverlight", "SOAP", "Sparx", "Sphinx", "Spring",
                     "SQL", "SQL Server", "Struts", "Subversion", "SVN", "VB.NET", "Visio", "Visual Studio",
                     "WCF", "Web Services", "WPF", "XML", "xUnit"]



    skillsDictionary = {}

    for jobFileName in listdir("/Users/Christine/Desktop/EvernoteSkillClustersData"):
        jobFile = open("/Users/Christine/Desktop/EvernoteSkillClustersData/" + jobFileName, "r")
        jobDescription = jobFile.read().lower()
        for skillKeywordRaw in skillKeywords:
            skillKeyword = skillKeywordRaw.lower()
            ind = jobDescription.find(skillKeyword)
            if ind != -1:
                if skillKeyword in skillsDictionary:
                    secondarySkillDict = skillsDictionary[skillKeyword]
                else:
                    secondarySkillDict = {}

                for secondarySkillKeywordRaw in skillKeywords:
                    secondarySkillKeyword = secondarySkillKeywordRaw.lower()
                    indSec = jobDescription.find(secondarySkillKeyword)
                    if indSec != -1:
                        if secondarySkillKeyword in secondarySkillDict:
                            secondarySkillDict[secondarySkillKeyword] = secondarySkillDict[secondarySkillKeyword] + 1
                        else:
                            secondarySkillDict[secondarySkillKeyword] = 1
                skillsDictionary[skillKeyword] = secondarySkillDict

    for skillKeyword in skillsDictionary:
        secondarySkillHash = skillsDictionary[skillKeyword]
        for secondarySkillKeyword in secondarySkillHash:
            secondarySkillCount = secondarySkillHash[secondarySkillKeyword]
            skillpair = SkillPair()
            skillpair.primary_term = skillKeyword
            skillpair.secondary_term = secondarySkillKeyword
            skillpair.number_of_times = secondarySkillCount
            db.session.add(skillpair)
            #insertString = "INSERT INTO skillspair (primary_term, secondary_term, number_of_times) VALUES('" + skillKeyword + "','" + secondarySkillKeyword + "','" + str(
            #    secondarySkillCount) + "')"
            #print insertString
            #cur.execute(insertString)

    db.session.commit()
    return

if __name__ == '__main__':
    # Build a sample db on the fly, if one does not exist yet.
    app_dir = op.realpath(os.path.dirname(__file__))
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_db()

    # Start app
    app.run(debug=True)