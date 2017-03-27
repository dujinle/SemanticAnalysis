#!/usr/bin/python
#-*- coding:utf-8 -*-
import common,sys
from myexception import MyException

class SceneBase():
	def __init__(self):
		self.data = None;

	def load_data(self,dfile):
		try:
			if dfile is None: return;
			self.data = common.read_json(dfile);
		except Exception as e:
			raise MyException(sys.exc_info());

	def _fetch_func(self,struct,tt = 'stype'):
		reg = '';
		for istr in struct['inlist']:
			if not struct.has_key(istr): continue;
			item = struct[istr];
			if item.has_key('parent'):
				reg = reg + item['parent'][tt];
			reg = reg + item[tt];
			if item.has_key('child'):
				reg = reg + item['child'][tt];

		for model in self.data['models']:
			comp = re.compile(model['reg']);
			match = comp.search(reg);
			if not match is None: return model['func'];
		return None;
