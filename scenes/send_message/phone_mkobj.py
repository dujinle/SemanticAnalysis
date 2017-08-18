#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common
from myexception import MyException
from com_base import ComBase as PhoneBase
import struct_utils as Sutil
#标记用户列表中的数据
class PhoneMkobj(PhoneBase):

	def encode(self,struct,super_b):
		try:
			self._mark_body(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_body(self,struct):
		data = self.data['Users'];
		idx = 0;
		while True:
			if idx >= len(struct['text']): break;
			strs = struct['text'][idx:];
			wd = '';
			for word in list(strs):
				wd = wd + word;
				if data.has_key(wd):
					tdic = dict(data[wd]);
					idx = idx + len(wd) - 1;
					struct[wd] = tdic;
					Sutil._merge_some_words(struct,wd,0);
					wd = '';
					break;
			idx = idx + 1;
