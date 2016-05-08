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
			if not struct.has_key('unit_list'): struct['unit_list'] = list();
			self._mark_unit(struct);
			self._deal_unit(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_unit(self,struct):
		for istr in struct['inlist']:
			if self.data.has_key(istr):
				tdic = dict();
				tdic['stype'] = 'UNIT';
				tdic['str'] = istr;
				struct['unit_list'].append(tdic);
		Sutil._sort_by_apper(struct,'unit_list');

	#把相邻的单位词合并成一个单位词
	def _deal_unit(self,struct):
		Sutil._merge_cont_tag(struct,'unit_list',self.data);

