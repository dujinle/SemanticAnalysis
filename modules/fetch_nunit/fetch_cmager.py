#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
import common,config
from fetch_nunit import FetchNunit
from myexception import MyException

class PDealMager:
	def __init__(self):
		self.tag_objs = list();

		# mark tag objs #
		self.tag_objs.append(FetchNunit());

	def init(self,dtype):
		try:
			step = 1;
			dfiles = config.dfiles[dtype];
			for obj in self.tag_objs:
				obj.load_data(dfiles[str(step)]);
				step = step + 1;
		except Exception as e: raise e;

	def encode(self,struct):
		try:
			for obj in self.tag_objs:
				obj.encode(struct);
		except Exception as e:
			raise MyException(sys.exc_info());
