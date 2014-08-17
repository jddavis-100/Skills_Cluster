from __future__ import division

__author__ = 'Christine'

from decimal import *

import os
import os.path as op
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from wtforms import validators

from flask.ext import admin
from flask.ext.admin.contrib import sqla
from flask.ext.admin.contrib.sqla import filters, ModelView

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

import pprint
import sqlite3 as lite

from os import listdir

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['DATABASE_FILE'] = 'C:\\Users\\elze\\Documents\\MyProjects\\Python\\EvernoteSkillClusters\\skillsClustertest.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class SkillPostCounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_term = db.Column(db.String(140))
    number_of_postings = db.Column(db.Float)

    def __unicode__(self):
        return self.skill_term

class SkillPair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primary_term = db.Column(db.String(140))
    secondary_term = db.Column(db.String(140))
    number_of_times = db.Column(db.Integer)
    #Rel = relationship(SkillPostCounter, primaryjoin=primary_term == SkillPostCounter.skill_term)

    #num_postings = relationship(SkillPostCounter, primaryjoin=primary_term == SkillPostCounter.skill_term)


    ratio = db.column_property(
        #db.select([Decimal(number_of_times) / Decimal(SkillPostCounter.number_of_postings)]).\
	#db.select([SkillPostCounter.number_of_postings / number_of_times]).\
	db.select([number_of_times / SkillPostCounter.number_of_postings]).\
            where(SkillPostCounter.skill_term==primary_term).\
            correlate_except(SkillPostCounter)
    )

    def __unicode__(self):
        return self.primary_term



class SkillView(ModelView):
    #column_select_related_list = ('primary_term', 'secondary_term', 'ratio')

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
#admin.add_view(PercentagesView(db.session))

def build_db():

    db.drop_all()
    db.create_all()

    skillKeywords = ["AJAX", "AMQP", "Android", "Angular", "Ant", "ApacheMQ", "Artifactory", "ASP.NET", "Backbone", "Bootstrap",
                     "C++", "C#", "Cassandra", "Chef", "CSS", "Crystal Reports", "Delphi", "DevOps", "Django",
		     "Eclipse", "Ember", "Entity Framework", "Flash", "Flask", "FoxPro", "IIS",
		     "GIS", "Git", "Hadoop", "Handlebars", "Hibernate", "HTML", "HTML5", "J2EE", "Java", "Javascript",
                     "JBOSS", "JCE", "JDBC", "Jenkins", "JMS", "JNDI", "JPA", "JQuery", "JSON", "JUnit", 
                     "LAMP", "Lua", "Linux", "Maven", "Memcached", "MongoDB", "MVC", "MySQL", ".NET",
		     "NHibernate", "Node", "Nose", "NoSQL", "NUnit",
                     "Oracle", "Perl", "Photoshop", "PHP", "PostGIS", "Postgres", "Python", "Puppet", "RabbitMQ", "REST", "Ruby",
                     "Ruby on Rails", "Selenium", "Silverlight", "SOAP", "Sparx", "Sphinx", "Spring",
                     "SQL", "SQL Server", "Struts", "Subversion", "SVN", "UNIX",
		     "VB.NET", "Visio", "Visual Basic", "Visual Studio",
                     "WCF", "Web Services", "WPF", "XML", "xUnit"]



    skillsDictionary = {}

    skillsPostCountsDict = {}

    for jobFileName in listdir("c:\\temp\\EvernoteSkillClustersData"):
        jobFile = open("c:\\temp\\EvernoteSkillClustersData\\" + jobFileName, "r")
        jobDescription = jobFile.read().lower()
        for skillKeywordRaw in skillKeywords:
            skillKeyword = skillKeywordRaw.lower()
            ind = jobDescription.find(skillKeyword)
            if ind != -1:
                if skillKeyword in skillsDictionary:
                    secondarySkillDict = skillsDictionary[skillKeyword]
		    skillsPostCountsDict[skillKeyword] = skillsPostCountsDict[skillKeyword] + 1
                else:
                    secondarySkillDict = {}
		    skillsPostCountsDict[skillKeyword] = 1

                for secondarySkillKeywordRaw in skillKeywords:
                    secondarySkillKeyword = secondarySkillKeywordRaw.lower()
		    if (skillKeyword != secondarySkillKeyword):
			indSec = jobDescription.find(secondarySkillKeyword)
			if indSec != -1:
			    if secondarySkillKeyword in secondarySkillDict:
				secondarySkillDict[secondarySkillKeyword] = secondarySkillDict[secondarySkillKeyword] + 1
			    else:
				secondarySkillDict[secondarySkillKeyword] = 1
		skillsDictionary[skillKeyword] = secondarySkillDict

    for skillKeyword in skillsPostCountsDict:
	skillPostCounter = SkillPostCounter()
	skillPostCounter.skill_term = skillKeyword
	skillPostCounter.number_of_postings = skillsPostCountsDict[skillKeyword]
	db.session.add(skillPostCounter)

    for skillKeyword in skillsDictionary:
        secondarySkillHash = skillsDictionary[skillKeyword]
        for secondarySkillKeyword in secondarySkillHash:
            secondarySkillCount = secondarySkillHash[secondarySkillKeyword]
            skillpair = SkillPair()
            skillpair.primary_term = skillKeyword
            skillpair.secondary_term = secondarySkillKeyword
            skillpair.number_of_times = secondarySkillCount
            db.session.add(skillpair)


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
