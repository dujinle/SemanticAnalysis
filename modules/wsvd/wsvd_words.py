#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException
import struct_utils as Sutil

class WsvdWords():
	def __init__(self):
		self.text = None;

	def encode(self,struct):
		try:
			self._wsvd(struct);
			self._esvd(struct);
			struct['stseg'] = self.text.split(' ');
		except Exception:
			raise MyException(sys.exc_info());

	#重新对分词的结果进行整理 处理分错的问题 最长匹配原则
	def _wsvd(self,struct):
		if self.text is None:
			if not struct.has_key('text'): return None;
			self.text = ' '.join(list(struct['text']));
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
	def _esvd(self,struct):
		if self.text is None:
			if not struct.has_key('text'): return None;
			self.text = ' '.join(list(struct['text']));
		comp = re.compile('[A-Za-z ]{1,}');
		match = comp.findall(self.text);
		for m in match:
			tm = m.replace(' ','');
			elf.text = self.text.replace(m,tm);
