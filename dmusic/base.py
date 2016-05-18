#!/usr/bin/python
#-*- coding:utf-8 -*-
import common,os,json
from myexception import MyException
class Base:
	def __init__(self):
		self.data = None;

	def init(self):
		pass;

	def load_data(self,dfile):
		try:
			if dfile is None: return;
			self.data = common.readfile(dfile);
		except Exception as e:
			raise e;
