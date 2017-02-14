#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException
import struct_utils as Sutil

#标记代词
class MarkPronoun():
	def __init__(self,net_data,key):
		self.net_data = net_data;
		self.key = key;

	def load_data(self,dfile): pass;

	def encode(self,struct):
		try:
			if not struct.has_key(self.key): struct[self.key] = list();
			if not struct.has_key('inlist'):
				self._mark_objs(struct);
			else:
				self._mark_objs_inlist(struct);
			Sutil._link_split_words(struct,self.key);
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_objs(self,struct):
		data = self.net_data.get_data_key(self.key);
		if data is None: return None;

		for key in data.keys():
			item = data[key];
			pstr = '';
			for istr in item['reg']:
				pstr = pstr + '(' + istr + ')|';
			if pstr[-1] == '|': pstr = pstr[0:-1];
			comp = re.compile(pstr);
			match = comp.findall(struct['text']);
			for it in match:
				if isinstance(it,tuple) == True:
					for isr in it:
						if len(isr) == 0: continue;
						tdic = dict();
						tdic['str'] = isr;
						if item.has_key('type'):
							tdic['type'] = item['type'];
						else:
							tdic['type'] = self.key;
						tdic['stype'] = item['stype'];
						struct[self.key].append(tdic);
				else:
					tdic = dict();
					tdic['str'] = it;
					if item.has_key('type'):
						tdic['type'] = item['type'];
					else:
						tdic['type'] = self.key;
					tdic['stype'] = item['stype'];
					struct[self.key].append(tdic);

	def _mark_objs_inlist(self,struct):
		data = self.net_data.get_data_key(self.key);
		if data is None: return None;

		for key in data.keys():
			item = data[key];
			for istr in item['reg']:
				if istr in struct['inlist']:
					tdic = dict();
					tdic['str'] = istr;
					if item.has_key('type'):
						tdic['type'] = item['type'];
					else:
						tdic['type'] = self.key;
					tdic['stype'] = item['stype'];
					struct[self.key].append(tdic);
