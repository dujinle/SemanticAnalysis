#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
import common
from myexception import MyException
from wsvd_words import WsvdWords

class WsvdMager:
	def __init__(self):
		self.tag_objs = list();
		# mark tag objs #
		self.tag_objs.append(WsvdWords());

	def init(self,dtype = None): pass;

	def encode(self,struct):
		try:
			for obj in self.tag_objs:
				obj.encode(struct);
		except Exception as e:
			raise MyException(sys.exc_info());
