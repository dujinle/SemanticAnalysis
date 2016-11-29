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
			if not struct.has_key('Nunit'): struct['Nunit'] = list();
			self._calc_num_unit(struct);
			self._reset_inlist(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _calc_num_unit(self,struct):
		nlist = struct['Nums'];
		ulist = struct['Units'];
		nid = uid = 0;
		while True:
			if nid >= len(nlist): break;
			num = nlist[nid];
			uid = 0;
			while True:
				if uid >= len(ulist): break;
				unit = ulist[uid];
				ustr = num['str'] + unit['str'];
				if struct['text'].find(ustr) <> -1:
					tdic = dict();
					tdic['type'] = 'Nunit';
					tdic['stype'] = num['type'] + unit['type'];
					tdic['str'] = ustr;
					tdic['stc'] = [num,unit];
					struct['Nunit'].append(tdic);
					del ulist[uid],nlist[nid];
					nid = nid - 1;
					break;
				else:
					uid = uid + 1;
			nid = nid + 1;

	def _reset_inlist(self,struct):
		tid = 0;
		for item in struct['Nunit']:
			tstr = item['str']
			tid = Sutil._merge_some_words(struct,tstr,tid);
