# -*- coding: utf-8 -*-

active_options = []

def is_set(property):
	if 'all-nodesc' in active_options:
		return property != 'description'
	return 'all' in active_options or property in active_options

def gen_template(dbname, db_line_def, options):
	global active_options
	active_options = options
	template = "# -*- coding: utf-8 -*- \n\n"
      
	if is_set('description'):
		template +="""
#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################
"""
      
	if is_set('gae'):
		template += """if request.env.web2py_runtime_gae:            # if running on Google App Engine
	%s = DAL('gae')                           # connect to Google BigTable
	session.connect(request, response, db=%s) # and store sessions and tickets there
	### or use the following lines to store sessions in Memcache
	# from gluon.contrib.memdb import MEMDB
	# from google.appengine.api.memcache import Client
	# session.connect(request, response, db=MEMDB(Client())
else:                                         # else use a normal relational database
	%s       # if not, use SQLite or other DB

""" % (dbname, dbname, db_line_def.strip())
	else:
		template += db_line_def
            
	if is_set('session'):
		template += """
## if no need for session
# session.forget()
"""
      
	if is_set('description'):
		template += """
#########################################################################
## Here is sample code if you need for 
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## comment/uncomment as needed
"""
	template +="from gluon.tools import *"
      
	if is_set('auth'):
		template += """
auth=Auth(globals(),%s)                      # authentication/authorization
auth.settings.hmac_key='<your secret key>'
auth.define_tables()                         # creates all needed tables
""" % dbname
      
	if is_set('crud'):
		template += "crud=Crud(globals(),%s)                      # for CRUD helpers using auth\n" % dbname
      
	if is_set('services'):
		template += "service=Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc\n"
      
	if is_set('auth-crud'):
		template +="# crud.settings.auth=auth                      # enforces authorization on crud\n"
      
	if is_set('mail'):
		template += """
# mail=Mail()                                  # mailer
# mail.settings.server='smtp.gmail.com:587'    # your SMTP server
# mail.settings.sender='you@gmail.com'         # your email
# mail.settings.login='username:password'      # your credentials or None
"""
      
	if is_set('auth'):
		template += """
# auth.settings.mailer=mail                    # for user email verification
# auth.settings.registration_requires_verification = True
# auth.settings.registration_requires_approval = True
# auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
# auth.settings.reset_password_requires_verification = True
# auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'
## more options discussed in gluon/tools.py
#########################################################################
"""

	if is_set('description'):
		template += """
#########################################################################
## Define your tables below, for example
##
## >>> %s.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(%s.mytable.myfield=='value').select(%s.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
      """ % (dbname, dbname, dbname) 
	return template + '\n'