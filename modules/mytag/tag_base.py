#!/usr/bin/python
#-*- coding:utf-8 -*-
import common,os,sys
from myexception import MyException

class TagBase:
	def __init__(self):
		self.data = None;

	def init(self): pass;

	def load_data(self,dfile):
		try:
			if dfile is None: return;
			self.data = common.read_json(dfile);
		except Exception as e:
			raise MyException(sys.exc_info());
