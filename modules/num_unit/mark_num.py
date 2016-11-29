#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException
import struct_utils as Sutil
import hanzi2num as Han2Dig

class MarkNum():
	def __init__(self):
		self.data = dict();

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception:
			raise MyException(sys.exc_info());

	def encode(self,struct):
		try:
			if not struct.has_key('Nums'): struct['Nums'] = list();
			self._mark_num(struct);
			self._reset_inlist(struct);
		except Exception:
			raise MyException(sys.exc_info());

	#把数字组合在一起 并更新分词的列表
	def _reset_inlist(self,struct):
		sid = 0;
		for item in struct['Nums']:
			tstr = item['str'];
			sid = Sutil._merge_some_words(struct,tstr,sid);

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
				struct['Nums'].append(tdic);

	def _match_num_reg(self,words):
		tdic = dict();
		for key in self.data:
			idata = self.data[key];
			comp = re.compile(idata);
			match = comp.findall(words);
			if match is None or len(match) == 0:
				continue;
			tdic[key] = match;
		return tdic;
