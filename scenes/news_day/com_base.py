#!/usr/bin/python
#-*- coding:utf-8 -*-
import common,os,sys,re,json
from myexception import MyException

class ComBase():
	def __init__(self):
		self.data = None;

	def init(self): pass;

	def load_data(self,dfile):
		try:
			if dfile is None: return;
			self.data = common.read_json(dfile);
		except Exception as e:
			raise MyException(sys.exc_info());

	def _fetch_func(self,struct):
		if not struct.has_key('stc'): return 'None';
		if not struct.has_key('stseg'): return 'None';

		segs = struct.get('stseg');
		stcs = struct.get('stc');
		reg = '';
		for istr in segs:
			if not stcs.has_key(istr): continue;
			item = stcs.get(istr);
			if item.has_key('stype'):
				reg = reg + item['stype'];

		for model in self.data['models']:
			comp = re.compile(model['reg']);
			match = comp.search(reg);
			if not match is None: return model['func'];
		return None;
