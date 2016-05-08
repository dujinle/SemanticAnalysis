#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,re,common
from myexception import MyException
import struct_utils as Sutil
class CalcNumUnit():
	def __init__(self):
		self.data = dict();

	def load_data(self,dfile):
		try:
			if dfile is None: return None;
			self.data = common.read_json(dfile);
		except Exception:
			raise MyException(sys.exc_info());

	def encode(self,struct):
		try:
			if not struct.has_key('nunit'): struct['nunit'] = list();
			self._calc_num_unit(struct);
			self._reset_inlist(struct);
			if len(struct['unit_list']) == 0: del struct['unit_list'];
			if len(struct['num_list']) == 0: del struct['num_list'];
		except Exception:
			raise MyException(sys.exc_info());

	def _calc_num_unit(self,struct):
		nlist = struct['num_list'];
		ulist = struct['unit_list'];
		nid = uid = pid = 0;
		while True:
			if nid >= len(nlist): break;
			num = nlist[nid];
			while True:
				if uid >= len(ulist): break;
				unit = ulist[uid];
				ustr = num['str'] + unit['str'];
				if struct['text'].find(ustr) <> -1:
					tdic = dict();
					tdic['type'] = 'NUNIT';
					tdic['str'] = ustr;
					tdic['stc'] = list();
					tdic['stc'].append(num);
					tdic['stc'].append(unit);
					struct['nunit'].append(tdic);
					del ulist[uid],nlist[nid];
					nid = nid - 1;
					break;
				else:
					uid = uid + 1;
			nid = nid + 1;

	def _reset_inlist(self,struct):
		tid = 0;
		for item in struct['nunit']:
			tstr = item['str']
			tid = Sutil._merge_some_words(struct,tstr,tid);
