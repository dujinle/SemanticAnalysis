#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common
from myexception import MyException
import struct_utils as Sutil
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
			if not struct.has_key('Units'): struct['Units'] = list();
			self._mark_unit(struct);
			self._deal_unit(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_unit(self,struct):
		for unit in self.data.keys():
			if struct['text'].find(unit) <> -1:
				tdic = dict();
				tdic['stype'] = 'UNIT';
				tdic['str'] = unit;
				struct['Units'].append(tdic);
		Sutil._sort_by_apper(struct,'Units');

	#把相邻的单位词合并成一个单位词
	def _deal_unit(self,struct):
		Sutil._merge_cont_tag(struct,'Units',self.data);

