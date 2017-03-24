#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
import common
from fetch_nunit import FetchNunit
from myexception import MyException
abspath = os.path.dirname(__file__);

class FnunitMager:
	def __init__(self):
		self.tag_objs = list();
		self.dfile = [
			os.path.join(abspath,'tdata','fetch_nunit.json')
		];
		# mark tag objs #
		self.tag_objs.append(FetchNunit());

	def init(self,dtype = None):
		try:
			for i,obj in enumerate(self.tag_objs):
				obj.load_data(self.dfile[i]);
		except Exception as e: raise e;

	def encode(self,struct):
		try:
			for obj in self.tag_objs:
				obj.encode(struct);
		except Exception as e:
			raise MyException(sys.exc_info());
