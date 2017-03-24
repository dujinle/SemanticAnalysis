#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException
import struct_utils as Sutil
#处理数字单位的组合
class WsvdWords():

	def encode(self,struct):
		try:
			self._wsvd(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _wsvd(self,struct):
		if not struct.has_key('text'): return None;
		text = ' '.join(list(struct['text']));
		slen = len(struct['text']);
		sid = 0;eid = slen;
		while True:
			if sid > slen: break;
			istr = struct['text'][sid:eid];
			if struct['stc'].has_key(istr):
				ostr = ' '.join(list(istr));
				text = text.replace(ostr,istr);
				sid = eid;
				eid = slen;
			else:
				eid = eid - 1;
			if eid == 0:
				eid = slen;
				sid = sid + 1;
		struct['stseg'] = text.split(' ');
