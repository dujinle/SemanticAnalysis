#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
import common,config
from mytag_encode import MyTagEncode
from myexception import MyException

class MytagMager:
	def __init__(self):
		self.tag_objs = list();

		# mark tag objs #
		self.tag_objs.append(MyTagEncode());

	def init(self,dtype):
		try:
			step = 1;
			fdirs = config.dfiles[dtype];
			for obj in self.tag_objs:
				obj.init(fdirs[str(step)]);
				step = step + 1;
		except Exception as e: raise e;

	def encode(self,struct):
		try:
			for obj in self.tag_objs:
				obj.encode(struct);
		except Exception as e:
			raise e;
