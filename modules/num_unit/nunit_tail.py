#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException

class NunitTail():
	def __init__(self):
		self.data = dict();

	def load_data(self,dfile):
		pass;

	def encode(self,struct):
		try:
			if len(struct['Units']) == 0: del struct['Units'];
			if len(struct['Nums']) == 0: del struct['Nums'];
			if len(struct['Nunit']) == 0: del struct['Nunit'];
			if len(struct['Relat']) == 0: del struct['Relat'];
			if len(struct['RelatStc']) == 0: del struct['RelatStc'];
			self._fetch_type(struct,'Units');
			self._fetch_type(struct,'Nums');
			self._fetch_type(struct,'Nunit');
			self._fetch_type(struct,'Relat');
			self._fetch_type(struct,'RelatStc');

		except Exception:
			raise MyException(sys.exc_info());

	def _fetch_type(self,struct,key):
		if struct.has_key(key):
			for item in struct[key]: struct[item['str']] = item;
			del struct[key];
