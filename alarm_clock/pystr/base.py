#!/usr/bin/python
#-*- coding:utf-8 -*-
import common
import os
import json
from myexception import MyException
from handler import RequestHandler

class Base(RequestHandler):
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
			if dfile is None: return;
			self.data = common.read_json(dfile);
		except Exception as e:
			raise MyException(format(e));

	def deal_data(self,fname,action,data):
		_class = str(self.__class__);
		idx = _class.find(fname);
		spidx = _class.find('.');
		if spidx != -1 and fname != _class[spidx + 1:]:
			return common.PASS;
		func = self.action[action];
		ret = func(data);
		return ret;

	def check_input(self,struct):
		if not struct.has_key('inlist'):
			raise MyException('the struct has not contain the key [inlist]');

	def write_file(self,dfile):
		try:
			if dfile is None: return None;
			os.rename(dfile,dfile + '.1');
			data = json.dumps(self.data,indent = 2,ensure_ascii = False);
			fd = open(dfile,'w');
			fd.write(data);
			fd.close();
		except Exception as e:
			raise MyException(format(e));

	def _add(self,data): pass;
	def _del(self,data): pass;
	def baseget(self,data): return self.data;
	def _send_msg(self,msg): self.gen_result(0,'succ',msg);
