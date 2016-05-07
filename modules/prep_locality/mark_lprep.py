#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,re,common
from myexception import MyException

#mark the locality prep words
class MarkLPrep():
	def __init__(self):
		self.data = dict();

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception:
			raise MyException(sys.exc_info());

	def encode(self,struct):
		try:
			if not struct.has_key('lprep'): struct['lprep'] = list();
			self._mark_tmood_tag(struct);
		except Exception as e:
			raise MyException(sys.exc_info());

	def _mark_tmood_tag(self,struct):
		for tag in struct['inlist']:
			tdic = self._mark_words(tag);
			if not tdic is None:
				struct['lprep'].append(tdic);

	def _mark_words(self,tstr):
		for key in self.data.keys():
			item = self.data[key];
			if tstr in item['reg']:
				tdic = dict();
				tdic['type'] = 'LPREP';
				tdic['stype'] = key;
				tdic['str'] = tstr;
				return tdic;
		return None;

