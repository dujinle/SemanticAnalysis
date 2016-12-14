#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException
import struct_utils as Sutil
import hanzi2num as Han2Dig

class MarkNum():
	def __init__(self,net_data,key):
		self.net_data = net_data;
		self.key = key;

	def encode(self,struct):
		try:
			if not struct.has_key(self.key): struct[self.key] = list();
			self._mark_num(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_num(self,struct):
		words = struct['text'];
		match = self._match_num_reg(words);
		for key in match.keys():
			item = match[key];
			for it in item:
				tdic = dict();
				tdic['type'] = 'NUM';
				if key == 'nreg':
					tdic['stype'] = it;
				else:
					tdic['stype'] = str(Han2Dig.cn2dig(it));
				tdic['str'] = it;
				struct[self.key].append(tdic);

	def _match_num_reg(self,words):
		data = self.net_data.get_data_key(self.key);
		tdic = dict();
		for key in data:
			idata = data[key];
			comp = re.compile(idata);
			match = comp.findall(words);
			if match is None or len(match) == 0:
				continue;
			tdic[key] = match;
		return tdic;
