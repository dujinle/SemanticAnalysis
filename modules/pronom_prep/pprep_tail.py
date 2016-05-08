#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,re,common
from myexception import MyException

#进行收尾工作,最后处理余下的结构
class PPrepTail():
	def __init__(self): pass;

	def load_data(self,dfile): pass;

	def encode(self,struct):
		try:
			#方位词归入inlist
			self._deal_prep_pronom(struct,'LocalPrep');
			#相对代词归入 inlist
			self._deal_prep_pronom(struct,'AbsPronom');
			#人称代词归入 inlist
			self._deal_prep_pronom(struct,'PerPronom');
		except Exception as e:
			raise MyException(sys.exc_info());

	def _deal_prep_pronom(self,struct,ikey):
		if struct.has_key(ikey):
			for item in struct[ikey]:
				tstr = item['str'];
				if tstr in struct['inlist']:
					idx = struct['inlist'].index(tstr);
					struct['inlist'][idx] = item;
			del struct[ikey];

