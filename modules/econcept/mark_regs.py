#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException
import struct_utils as Sutil

#标记需要正则匹配的模块
class MarkRegs():
	def __init__(self,net_data,key):
		self.net_data = net_data;
		self.key = key;

	def load_data(self,dfile): pass;

	def encode(self,struct):
		try:
			if not struct.has_key(self.key): struct[self.key] = list();
			self._mark_regs(struct);
			Sutil._link_split_words(struct,self.key);
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_regs(self,struct):
		data = self.net_data.get_data_key(self.key);
		if data is None: return None;

		for key in data.keys():
			item = data[key];
			for it in item:
				if not it.has_key('stype'):
					it['stype'] = key
				self._mark_reg_from_list(struct,it);

	def _mark_reg_from_list(self,struct,item):
		if not item.has_key('stype'):
			item['stype'] = key
		comp = re.compile(item['reg']);
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
			elif len(it) > 0:
				tdic = dict();
				tdic['str'] = it;
				if item.has_key('type'):
					tdic['type'] = item['type'];
				else:
					tdic['type'] = self.key;
				tdic['stype'] = item['stype'];
				struct[self.key].append(tdic);
