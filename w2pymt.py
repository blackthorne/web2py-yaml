#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Web2py YAML Model Translator

import yaml,sys,headers

########################################################################
class Table:
	"""represents a table that may be part of a Model"""
	#----------------------------------------------------------------------
	def __init__(self, name, fields={}, constraints={}):
		"""Constructor"""
		self.name, self.fields, self.constraints = name, fields, constraints
		
	def gen_constraints(self, dbname):
		code = ''
		for field in self.fields:
			if self.fields[field].__class__() == {}:
				for key in self.fields[field]:
					if key != 'type':
						code += "%s.%s.%s.%s=%s\n" % (dbname, self.name, field, key, self.fields[field][key])
		return code
	
	def gen_code(self, dbname):
		code = "%s.define_table(\'%s\'\n" % (dbname, self.name)
		for i,field in enumerate(self.fields):
			if self.fields[field] .__class__() == {}:
				code += "\tSQLField(\'%s\', \'%s\')" % (field, self.fields[field]['type'])
			elif ',' in self.fields[field]:
				commaindex=self.fields[field].find(',')
				code += "\tSQLField(\'%s\', \'%s\',%s)" % (field, self.fields[field][:commaindex], self.fields[field][commaindex+1:])
			else:
				code += "\tSQLField(\'%s\', \'%s\')" % (field, self.fields[field]) 
			if i +1 != len(self.fields):
				code += ','
			code += '\n'
		code += ')\n'
		constraints = self.gen_constraints(dbname)
		if constraints != '':
			code += constraints + '\n'
		return code 
	
########################################################################
class Model:
	"""defines a Model to be translated"""
	def gen_db_def(self):
		if self.conf['db']['parameters'] == '':
			return "%s = DAL(\'%s\')\n" % (self.conf['db']['name'], self.conf['db']['dbline'])
		else:
			return "%s = DAL(\'%s\', %s)\n" % (self.conf['db']['name'], self.conf['db']['dbline'], self.conf['db']['parameters'])
	
	def gen_tables(self, dataMap, tables = {}):
		for table in dataMap:
			if table != 'db':
				tables[table] = Table(table, dataMap[table])
				for field in dataMap[table].keys():
					if field == 'constraints':
						tables[table].constraints = dataMap[table]['constraints']
						del tables[table].fields[field]
		return tables
	
	def gen_conf(self, dataMap):
		for table in self.tables:                         # not really needed
			del dataMap[table]                       #
		for key,default in self.defaults:
			if not dataMap['db'].has_key(key):
				dataMap['db'][key] = default
		if dataMap['db']['dbline'] == '':
			if dataMap['db']['dbms'] == 'sqlite':
				dataMap['db']['dbline'] = "sqlite://" + dataMap['db']['dbfile'] 
			else:
				dataMap['db']['dbline'] = "%s://%s:%s@%s/%s" % (dataMap['db']['dbms'], dataMap['db']['username'], dataMap['db']['password'], dataMap['db']['hostname'], dataMap['db']['name'])		
		options = dataMap['db']['options']                                    #
		dataMap['db']['options'] = []
		if ',' in options:#
			for option in options.split(','):                                            # not really needed
				dataMap['db']['options'].append(option.strip())      #
		else:
			dataMap['db']['options'] = [options]
		return dataMap
	
	#----------------------------------------------------------------------
	def __init__(self, 
	             yaml_filename, 
	             defaults = [('dbms','sqlite'),('username',''),('password',''),('hostname','localhost'),('parameters',''), ('options',['all']), ('dbline',''), ('dbfile', 'storage.sqlite')]):
		"""Constructor"""
		dataMap = self.load_yaml_file(yaml_filename)                                 # 
		self.defaults, self.tables = defaults, self.gen_tables(dataMap)        # these lines order should be respected
		self.conf = self.gen_conf(dataMap)                                                      #
			
	def load_yaml_file(self, filename):
		file = open(filename)
		dataMap = yaml.load(file)
		file.close()
		return dataMap

	def gen_code(self):
		code = headers.gen_template(self.conf['db']['name'], self.gen_db_def(), self.conf['db']['options'])
		for table in self.tables:
			code += self.tables[table].gen_code(self.conf['db']['name'])
		return code
	
	def __str__(self):
		return self.gen_code()

def usage():
	print 'ERROR: missing or wrongly defined parameters'
	print 'usage:'
	print '\t' + sys.argv[0] + " <yaml_model> <db_output_file>\n"
	exit()
	
def main():
	if len(sys.argv) == 3:
		print 'Loading model...'
		model = Model(sys.argv[1])
		file = open(sys.argv[2],'w')
		print 'Generating code to output file...'
		file.write(model.gen_code())
		file.close()
		print 'done'
	else:
		usage()
if __name__ == '__main__':
	main()
