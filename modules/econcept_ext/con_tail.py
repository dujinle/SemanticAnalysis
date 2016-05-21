#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
import common,config
from net_data import NetData
from myexception import MyException

class ConTail():
	def __init__(self):
		self.net_data = NetData();

	def init(self,dtype): pass;

	def encode(self,struct):
		try:
			ndata = self.net_data.data;
			if not struct.has_key('stc'): struct['stc'] = dict();
			if not struct.has_key('stc_same'): struct['stc_same'] = list();

			self._fetch_ckey(struct,'time_stc','TIME');
			self._fetch_ckey(struct,'SomeNums',None);
			self._fetch_ckey(struct,'SomeUnits',None);

			for key in ndata.keys():
				if not struct.has_key(key): continue;
				self.fetch_cept(struct,struct[key]);
				del struct[key];

		except Exception as e:
			raise MyException(sys.exc_info());

	def fetch_cept(self,struct,cepts):
		stc = struct['stc'];
		for ib in cepts:
			istr = ib['str'];
			if stc.has_key(istr) and stc[istr]['type'] <> ib['type']:
				struct['stc_same'].append(dict(ib));
				continue;
			stc[istr] = dict(ib);

	def _fetch_ckey(self,struct,ckey,ctype):
		if not struct.has_key(ckey): return None;
		stc = struct['stc'];
		for inter in struct[ckey]:
			istr = inter['str'].replace('_','');
			if not ctype is None:
				inter['stype'] = ctype;
				inter['type'] = ctype;
			inter['str'] = istr;
			if stc.has_key(istr) and stc[istr]['type'] <> inter['type']:
				struct['stc_same'].append(dict(inter));
				continue;
			stc[istr] = dict(inter);
		del struct[ckey];
