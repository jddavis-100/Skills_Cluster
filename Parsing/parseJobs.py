#from pattern.en import parse

#s = 'The mobile web is more important than mobile apps.'
#s = parse(s, relations=True, lemmata=True)
#print s


import pprint

from os import listdir

import sqlite3 as lite


#skillKeywords = ["AJAX", "AMQP", "Android", "ApacheMQ", "Artifactory", "ASP.NET", "Bootstrap", "C++", "C#", "CSS", "Crystal Reports", "Delphi", "Django", "Eclipse", "Flash", "GIS", "Git", "Hadoop", "Hibernate", "HTML", "HTML5", "J2EE", "Java", "Javascript", "JBOSS", "JCE", "JDBC", "Jenkins", "JMS", "JNDI", "JPA", "JQuery", "JSON", "JUnit", "LAMP", "Maven", "Memcached", "MongoDB", "MVC", "MySQL", ".NET", "Nose", "NUnit", "Oracle", "Perl", "Photoshop", "PHP", "PostGIS", "Python", "RabbitMQ", "REST", "Ruby", "Ruby on Rails", "Selenium", "Silverlight", "SOAP", "Sparx", "Sphinx", "Spring", "SQL", "SQL Server", "Struts", "Subversion", "SVN", "VB.NET", "Visio", "Visual Studio", "WCF", "Web Services", "WPF", "XML", "xUnit"]


skillKeywords = ["AJAX", "AMQP", "Android", "ApacheMQ", "Artifactory", "ASP.NET", "Bootstrap",
		 "C++", "C#", "CSS", "Crystal Reports", "Delphi", "Django", "Eclipse", "Flash",
		 "GIS", "Git", "Hadoop", "Hibernate", "HTML", "HTML5", "J2EE", "Java", "Javascript",
		 "JBOSS", "JCE", "JDBC", "Jenkins", "JMS", "JNDI", "JPA", "JQuery", "JSON", "JUnit",
		 "LAMP", "Maven", "Memcached", "MongoDB", "MVC", "MySQL", ".NET", "Nose", "NUnit",
		 "Oracle", "Perl", "Photoshop", "PHP", "PostGIS", "Python", "RabbitMQ", "REST", "Ruby",
		 "Ruby on Rails", "Selenium", "Silverlight", "SOAP", "Sparx", "Sphinx", "Spring",
		 "SQL", "SQL Server", "Struts", "Subversion", "SVN", "VB.NET", "Visio", "Visual Studio",
		 "WCF", "Web Services", "WPF", "XML", "xUnit"]



#jobFile = open("c:\\temp\\EvernoteSkillClustersData\\0026c338-e8a0-475f-b9a6-aa595109e71d.html", "r")



skillsDictionary = {}

for jobFileName in listdir("c:\\temp\\EvernoteSkillClustersData"):
    jobFile = open("c:\\temp\\EvernoteSkillClustersData\\"+jobFileName, "r")
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
		
		

	

pp = pprint.PrettyPrinter(depth=6)

#pp.pprint(skillsDictionary)

#with open('skillsDictionary.txt', 'wt') as out:
 #   pprint(skillsDictionary, stream=out)





con = lite.connect('skillClusters')
    
cur = con.cursor()    
cur.execute('SELECT SQLITE_VERSION()')
    
data = cur.fetchone()
    
print "SQLite version: %s" % data                
    
with con:
    
    cur = con.cursor()    
    for skillKeyword in skillsDictionary:
	secondarySkillHash = skillsDictionary[skillKeyword]
	for secondarySkillKeyword in secondarySkillHash:
	    secondarySkillCount = secondarySkillHash[secondarySkillKeyword]
	    insertString = "INSERT INTO skillspair (primary_term, secondary_term, number_of_times) VALUES('" + skillKeyword + "','" + secondarySkillKeyword + "','" + str(secondarySkillCount) + "')"
	    print insertString
	    cur.execute(insertString)
