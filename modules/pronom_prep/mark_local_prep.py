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
		for key in self.data.keys():
			item = self.data[key];
			reg_str = '';
			for istr in item['reg']:
				reg_str = reg_str + '(' + istr + ')|'
			if reg_str[-1] == '|': reg_str = reg_str[0:-1];
			com = re.compile(reg_str);
			match = com.search(struct['text']);
			if match is None: continue;
			tdic = dict();
			tdic['type'] = 'LocalPrep';
			tdic['stype'] = key;
			tdic['str'] = match.group(0);
			struct['LocalPrep'].append(tdic);
		Sutil._sort_by_apper(struct,'LocalPrep');

	def _reset_inlist(self,struct):
		Sutil._merge_cont_tag(struct,'LocalPrep');
		tid = 0;
		for item in struct['LocalPrep']:
			tid = Sutil._merge_some_words(struct,item['str'],tid);
