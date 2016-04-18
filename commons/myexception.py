#!/usr/bin/python
#-*- coding:utf-8 -*-
import json
CODENUM = 0;
class MyException(Exception):

	def __init__(self,value):
		self.value = value;

	def __str__(self):
		vtype = type(self.value);
		res = self.value;
		global CODENUM;
		CODENUM = CODENUM + 1;
		if vtype == dict or vtype == list:
			res = json.dumps(self.value,indent = 2,ensure_ascii = False);
		return repr('CodeError[' + str(CODENUM) + ']:' + res);
