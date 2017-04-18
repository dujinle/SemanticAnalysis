#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException
import struct_utils as Sutil

class RemarkWords():
	def __init__(self):
		self.encomp = re.compile('[A-Za-z ]{1,}');
		self.numcmp = re.compile('[0-9 ]{1,}');

	def encode(self,struct):
		try:
			self.text = None;
			self._wsvd(struct);
			self._esvd(struct,self.encomp);
			struct['stseg'] = self.text.split(' ');
		except Exception:
			raise MyException(sys.exc_info());

	#重新对分词的结果进行整理 处理分错的问题 最长匹配原则
	def _wsvd(self,struct):
		if self.text is None: self.text = ' '.join(list(struct['text']));
		slen = len(struct['text']);
		sid = 0;eid = slen;
		while True:
			if sid > slen: break;
			istr = struct['text'][sid:eid];
			if struct['stc'].has_key(istr):
				ostr = ' '.join(list(istr));
				self.text = self.text.replace(ostr,istr);
				sid = eid;
				eid = slen;
			else:
				eid = eid - 1;
			if eid == 0:
				eid = slen;
				sid = sid + 1;

	#组合邻近的英文字符 和 数字
	def _esvd(self,struct,comp):
		if self.text is None: self.text = ' '.join(list(struct['text']));
		match = comp.findall(self.text);
		for m in match:
			tm = m.replace(' ','');
			if tm == '' or len(tm) == 0: continue;
			self.text = self.text.replace(m,tm + ' ');
