#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException

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
		except Exception:
			raise MyException(sys.exc_info());

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
