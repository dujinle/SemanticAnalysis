#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common
from myexception import MyException
import struct_utils as Sutil
#标记对象名词以及链接的网络
class MarkObjs():
	def __init__(self,net_data,key):
		self.net_data = net_data;
		self.key = key;

	def load_data(self,dfile): pass;

	def encode(self,struct):
		try:
			if not struct.has_key(self.key): struct[self.key] = list();
			self._mark_objs_inlist(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_objs_inlist(self,struct):
		try:
			data = self.net_data.get_data_key(self.key);
			if data is None: return None;

			for tstr in struct['inlist']:
				tdic = self._fetch_str(tstr,data);
				if tdic is None: continue;
				mtdic = tdic['dict'][tstr];
#				common.print_dic(mtdic);
				myd = dict(mtdic['_prop']);
				myd['stype'] = myd['stype'].replace('_','');
				myd['str'] = tstr;
				myd['track'] = tdic['track'];
				struct[self.key].append(myd);
		except Exception as e:
			raise MyException(sys.exc_info());

	def _fetch_str(self,strs,dicts):
		if not isinstance(dicts,dict): return None;

		myob = dict();
		myob['dict'] = dicts;
		myob['track'] = list();
		mlist = list();
		mlist.append(myob);
		while True:
			if len(mlist) == 0: break;
			tdic = mlist.pop();
			if not isinstance(tdic['dict'],dict): continue;
			if tdic['dict'].has_key(strs): return tdic;
			for key in tdic['dict'].keys():
				tob = dict();
				tob['dict'] = tdic['dict'][key];
				tob['track'] = list();
				tob['track'].extend(tdic['track']);
				tob['track'].append(key);
				mlist.append(tob);
		return None;
