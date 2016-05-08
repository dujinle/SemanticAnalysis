#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,re,common
from myexception import MyException
import struct_utils as Sutil

#mark the locality prep words
class MarkLocalPrep():
	def __init__(self):
		self.data = dict();

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception:
			raise MyException(sys.exc_info());

	def encode(self,struct):
		try:
			if not struct.has_key('LocalPrep'): struct['LocalPrep'] = list();
			self._mark_lprep_tag(struct);
			self._reset_inlist(struct);
		except Exception as e:
			raise MyException(sys.exc_info());

	def _mark_lprep_tag(self,struct):
		for tag in struct['inlist']:
			tdic = self._mark_words(tag);
			if not tdic is None:
				struct['LocalPrep'].append(tdic);

	def _reset_inlist(self,struct):
		Sutil._merge_cont_tag(struct,'LocalPrep');
		tid = 0;
		for item in struct['LocalPrep']:
			tid = Sutil._merge_some_words(struct,item['str'],tid);

	def _mark_words(self,tstr):
		for key in self.data.keys():
			item = self.data[key];
			if tstr in item['reg']:
				tdic = dict();
				tdic['type'] = 'LocalPrep';
				tdic['stype'] = key;
				tdic['str'] = tstr;
				return tdic;
		return None;

