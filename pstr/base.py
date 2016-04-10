#!/usr/bin/python
#-*- coding:utf-8 -*-
import common
class Base:
	def __init__(self):
		pass;

	def init(self):
		self.__init__();

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception as e:
			raise e;

	def check_input(self,struct):
		if not struct.has_key('inlist'):
			raise Exception('the struct has not contain the key [inlist]');
