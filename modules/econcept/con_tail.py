#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException
import struct_utils as Sutil
class ConTail():
	def __init__(self):
		self.data = dict();
		self.flist = [
			"SomeBody",
			"SomePlace",
			"SomeThing",
			"Lpronoun",
			"Lunit","Sds",
			"ADJS","Verbs",
			"Math","Relat",
			"Nunit",
			"RelatStc",
			"Localizer"
		]

	def load_data(self,dfile):
		pass;

	def encode(self,struct):
		try:
			for fi in self.flist:
				if not struct.has_key(fi): continue;
				if len(struct[fi]) == 0: del struct[fi];
				self._fetch_type(struct,fi);
			self._fetch_time(struct);
			self._dist_scene(struct);

		except Exception:
			raise MyException(sys.exc_info());

	def _fetch_type(self,struct,key):
		if struct.has_key(key):
			for item in struct[key]: struct[item['str']] = item;
			del struct[key];

	def _dist_scene(self,struct):
		if struct.has_key('SomeThing'):
			for it in struct['SomeThing']:
				if it.has_key('scope'):
					struct['Scene'] = it['scope'];
	
	def _fetch_time(self,struct):
		if not struct.has_key('intervals'): return None;
		for inter in struct['intervals']:
			istr = inter['str'].replace('_','');
			Sutil._merge_some_words(struct,istr,0);
			inter['stype'] = 'TIME';
			inter['type'] = 'TIME';
			struct[istr] = inter;
		del struct['intervals'];
