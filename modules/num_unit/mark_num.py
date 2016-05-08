#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException
import struct_utils as Sutil

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
			if not struct.has_key('num_list'): struct['num_list'] = list();
			self._mark_num(struct);
			self._reset_inlist(struct);
		except Exception:
			raise MyException(sys.exc_info());

	#把数字组合在一起 并更新分词的列表
	def _reset_inlist(self,struct):
		sid = 0;
		for item in struct['num_list']:
			tstr = item['str'];
			sid = Sutil._merge_some_words(struct,tstr,sid);

	def _mark_num(self,struct):
		words = struct['text'];
		match = self._match_num_reg(words);
		if not match is None:
			for item in match:
				tdic = dict();
				tdic['stype'] = 'NUM';
				tdic['str'] = item;
				struct['num_list'].append(tdic);

	def _match_num_reg(self,words):
		for key in self.data:
			idata = self.data[key];
			comp = re.compile(idata);
			match = comp.findall(words);
			if match is None or len(match) == 0:
				continue;
			return match;
		return None;
