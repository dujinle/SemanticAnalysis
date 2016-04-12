#!/usr/bin/python
#-*- coding:utf-8 -*-
import common
class Base:
	def __init__(self):
		self.data = None;
		self.action = dict();
		self.action['add'] = self._add;
		self.action['del'] = self._del;
		self.action['get'] = self.baseget;

	def init(self):
		pass;

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception as e:
			raise e;

	def deal_data(self,fname,action,data):
		_class = str(self.__class__);
		if _class.find(fname) == -1:
			return common.PASS;
		if len(fname) == 1 and _class.find(fname + '1') <> -1:
			return common.PASS;

		func = self.action[action];
		ret = func(data);
		return ret;

	def check_input(self,struct):
		if not struct.has_key('inlist'):
			raise Exception('the struct has not contain the key [inlist]');

	def _add(self,data): pass;
	def _del(self,data): pass;
	def baseget(self,data): return self.data;
