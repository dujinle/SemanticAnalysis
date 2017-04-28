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

			for key in ndata.keys():
				if not struct.has_key(key): continue;
				self.fetch_cept(struct['stc'],struct[key]);
				del struct[key];
			self._fetch_ckey(struct,'intervals','TIME');
			self._fetch_ckey(struct,'SomeNums',None);
			self._fetch_ckey(struct,'SomeUnits',None);

		except Exception as e:
			raise MyException(sys.exc_info());

	def fetch_cept(self,stc,cepts):
		for ib in cepts:
			istr = ib['str'];
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
			stc[istr] = dict(inter);
		del struct[ckey];
