#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
import struct_utils as Sutil
from myexception import MyException

class MergeObjs():
	def __init__(self,net_data):
		self.net_data = net_data;
		self.filter = u'(的)*';

	def load_data(self,dfile): pass;

	def encode(self,struct):
		try:
			self._fetch_sub_objs(struct,'Objs','SB');
			self._reset_inlist(struct,'Objs');
		except Exception:
			raise MyException(sys.exc_info());

	#连续的对象必然存在从属关系 把他们合并在一起
	def _fetch_sub_objs(self,struct,key,stype):
		tid = pid = 0;
		while True:
			if tid >= len(struct[key]): break;
			cur = struct[key][tid];
			if cur['stype'] <> stype:
				tid = tid + 1;
				continue;
			pid = tid + 1;
			while True:
				if pid >= len(struct[key]): break;
				nitm = struct[key][pid];
				if nitm['stype'] <> stype:
					pid = pid + 1;
					continue;
				comp = re.compile(cur['str'] + self.filter + nitm['str']);
				match = comp.search(struct['text']);
				if not match is None:
					tdic = dict(cur);
					tdic['str'] = match.group(0);
					if tdic.has_key('stc'):
						tdic['stc'].append(nitm);
					else:
						tdic['stc'] = [cur,nitm];
					struct[key][tid] = tdic;
					del struct[key][pid];
					continue;
				pid = pid + 1;
			tid = tid + 1;

	def _reset_inlist(self,struct,key):
		tid = 0;
		for item in struct[key]:
			if item.has_key('stc'):
				tid = Sutil._merge_some_words(struct,item['str'],tid);
