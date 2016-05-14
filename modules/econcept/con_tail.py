#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException

class ConTail():
	def __init__(self):
		self.data = dict();

	def load_data(self,dfile):
		pass;

	def encode(self,struct):
		try:
			if len(struct['Objs']) == 0: del struct['Objs'];
			if len(struct['Verbs']) == 0: del struct['Verbs'];
			if len(struct['Sds']) == 0: del struct['Sds'];
			self._fetch_type(struct,'Objs');
			self._fetch_type(struct,'Verbs');
			self._fetch_type(struct,'Sds');

		except Exception:
			raise MyException(sys.exc_info());

	def _fetch_type(self,struct,key):
		if struct.has_key(key):
			for item in struct[key]: struct[item['str']] = item;
			del struct[key];
