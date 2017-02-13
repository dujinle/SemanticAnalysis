#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException
import struct_utils as Sutil

class FetchTail():
	def __init__(self):
		self.data = dict();
		self.flist = [
			"SomeObjs",
			"SomeVerb",
			"SomePronoun",
			"SomeUnits",
			"SomeAdj",
			"SomeAux",
			"SomeTmood",
			"SomePrep",
			"SomeTime",
			"SomeNoun",
			"Math",
			"Nunit",
			"SomeNums",
			"SomeOther",
			"SomeSpace",
			"SomeCopula",
			"SomeAdverb"
		]

	def load_data(self,dfile):
		pass;

	def encode(self,struct):
		try:
			for fi in self.flist:
				if not struct.has_key(fi): continue
				if len(struct[fi]) == 0: del struct[fi];
				self._fetch_type(struct,fi);

		except Exception:
			raise MyException(sys.exc_info());

	def _fetch_type(self,struct,key):
		if struct.has_key(key):
			for item in struct[key]:
				if struct.has_key('remove'):
					if item['str'] in struct['remove']:
						continue;
				if struct.has_key(item['str']):
					sit = struct[item['str']];
					if sit.has_key('flg'): continue;
				struct[item['str']] = item;
			del struct[key];
