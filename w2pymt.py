#!/usr/bin/env python
# encoding: utf-8
# Web2py YAML Model Translator

import yaml,sys #headers

########################################################################
class Table:
	"""represents a table that may be part of a Model"""
	#----------------------------------------------------------------------
	def __init__(self, name, fields={}, constraints=[]):
		"""Constructor"""
		self.name, self.fields, self.constraints = name, fields, constraints
		
	def gen_code(self, dbname):
		code = "%s.define_table(\'%s\'\n" % (dbname, self.name)
		for i,field in enumerate(self.fields):
			if field == 'constraints':
				self.constraints.append(self.fields[field])
			else:
				code += "\tSQLField(\'%s\', \'%s\')" % (field, self.fields[field]) # TODO: fix requires/default bug 
				if i +1 != len(self.fields):
					code += ','
				code += '\n'
		code += ')\n'
		return code 
	
########################################################################
class Model:
	"""defines a Model to be translated"""

	#----------------------------------------------------------------------
	def __init__(self, yaml_filename):
		"""Constructor"""
		self.conf, self.tables = self.load_yaml_file(yaml_filename), []
		for table in self.conf:
			if table != 'db':
				self.tables.append(Table(table, self.conf[table]))
		for table in self.tables:                         # remove ?
			del self.conf[table.name]
		for key,default in [('dbms','sqlite'),('username',''),('password',''),('hostname','localhost'),('parameters',''), ('options',[])]:
			self.set_default(key,default)
		for table in self.tables:
			print table.gen_code(self.conf['db']['name'])
		
	def set_default(self, conf_key, default_value):
		if not self.conf['db'].has_key(conf_key):
			self.conf['db'][conf_key] = default_value
			
	def load_yaml_file(self, filename):
		file = open(filename)
		dataMap = yaml.load(file)
		file.close()
		return dataMap
		
def main():
	print 'Loading model...'
	model = Model('models/yaml/test.yml')
	
if __name__ == '__main__':
	main()
