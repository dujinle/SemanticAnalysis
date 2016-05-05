#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common
from myexception import MyException

class MarkUnit():
	def __init__(self):
		self.data = dict();

	def load_data(self,dfile):
		try:
			self.data = common.readfile(dfile);
		except Exception:
			raise MyException(sys.exc_info());

	def encode(self,struct):
		try:
			if not struct.has_key('unit_list'): struct['unit_list'] = list();
			self._mark_unit(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_unit(self,struct):
		for key in self.data.keys():
			if struct['text'].find(key) <> -1:
				tdic = dict();
				tdic['stype'] = 'UNIT';
				tdic['str'] = key;
				struct['unit_list'].append(tdic);
