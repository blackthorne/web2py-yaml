#!/usr/bin/env python
# encoding: utf-8
# Web2py YAML Model Translator

import yaml,sys,#headers

########################################################################
class Table:
	"""represents a table that may be part of a Model"""
	#----------------------------------------------------------------------
	def __init__(self, name, fields={}, constraints={}):
		"""Constructor"""
		self.name, self.fields, self.constraints = name, fields, constraints
		
	def gen_code(self, dbname):
		code = "%s.define_table(\'%s\'\n" % (dbname, self.name)
		for i,field in enumerate(self.fields):
			code += "SQLField(\'%s\', \'%s\')" % (field, self.fields[field])
			if i +1 != len(self.fields):
				code += ','
			code += '\n'
		code += ')'
		return code 
	

def main():
	a = Table('asd')
	
if __name__ == '__main__':
	main()
