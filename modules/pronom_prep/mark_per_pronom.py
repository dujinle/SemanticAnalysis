#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,re,common
from myexception import MyException

#mark the pronom words
class MarkPerPronom():
	def __init__(self):
		self.data = dict();

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception:
			raise MyException(sys.exc_info());

	def encode(self,struct):
		try:
			if not struct.has_key('PerPronom'): struct['PerPronom'] = list();
			self._mark_PerPronom_tag(struct);
		except Exception as e:
			raise MyException(sys.exc_info());

	def _mark_PerPronom_tag(self,struct):
		for tag in struct['inlist']:
			tdic = self._mark_words(tag);
			if not tdic is None:
				struct['PerPronom'].append(tdic);

	def _mark_words(self,tstr):
		for key in self.data.keys():
			item = self.data[key];
			for k2 in item.keys():
				kitem = item[k2];
				if tstr in kitem['reg']:
					tdic = dict();
					tdic['type'] = key;
					tdic['stype'] = k2;
					tdic['str'] = tstr;
					return tdic;
		return None;

