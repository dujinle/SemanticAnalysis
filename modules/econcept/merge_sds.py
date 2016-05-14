#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
import struct_utils as Sutil
from myexception import MyException

class MergeSbDoSth():
	def __init__(self,net_data):
		self.net_data = net_data;
		self.filter = u'(的)*';

	def load_data(self,dfile): pass;

	def encode(self,struct):
		try:
			if not struct.has_key('Sds'): struct['Sds'] = list();
			self._fetch_sds(struct);
			self._reset_inlist(struct,'Sds');
		except Exception:
			raise MyException(sys.exc_info());

	#寻找sb do sth结构,进行组合
	def _fetch_sds(self,struct):
		pid = tid = uid = 0;
		while True:
			if pid >= len(struct['Objs']): break;
			pit = struct['Objs'][pid];
			tid = 0;
			while True:
				if tid >= len(struct['Verbs']): break;
				vit = struct['Verbs'][tid];
				if pit['stype'] == 'SB':
					if self._merge_ov(struct,pit,vit) == True:
						del struct['Objs'][pid];
						del struct['Verbs'][tid];
						pid = pid - 1;
						break;
				elif  pit['stype'] == 'STH' or  pit['stype'] == 'SP':
					if self._merge_ov(struct,vit,pit) == True:
						del struct['Objs'][pid];
						del struct['Verbs'][tid];
						pid = pid - 1;
						break;
				tid = tid + 1;
			pid = pid + 1;

		pid = tid = 0;
		while True:
			if pid >= len(struct['Objs']): break;
			pit = struct['Objs'][pid];
			tid = 0;
			while True:
				if tid >= len(struct['Sds']): break;
				sit = struct['Sds'][tid];
				if self._merge_ov(struct,sit,pit) == True:
					del struct['Objs'][pid];
					del struct['Sds'][tid];
					pid = pid - 1;
					break;
				elif self._merge_ov(struct,pit,sit) == True:
					del struct['Objs'][pid];
					del struct['Sds'][tid];
					pid = pid - 1;
					break;
				tid = tid + 1;
			pid = pid + 1;

	def _reset_inlist(self,struct,key):
		tid = 0;
		for item in struct[key]:
			if item.has_key('stc'):
				tid = Sutil._merge_some_words(struct,item['str'],tid);

	def _merge_ov(self,struct,cit,nit):
		pstr = cit['str'] + nit['str'];
		if struct['text'].find(pstr) <> -1:
			tdic = dict();
			tdic['str'] = pstr;
			tdic['stc'] = [cit,nit];
			tdic['stype'] = cit['stype'] + nit['stype'];
			struct['Sds'].append(tdic);
			return True;
		return False;

