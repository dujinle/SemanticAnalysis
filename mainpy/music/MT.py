#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,re
reload(sys);
sys.setdefaultencoding('utf-8');
import common,config
from myexception import MyException

class MT:
	def __init__(self):
		self.mt = dict();

	def init(self,dfile):
		try:
			self.mt = common.read_json(dfile);
		except MyException as e: raise e

	def encode(self,struct):
		self._match_mt(struct,'music_type');
		self._match_mt(struct,'music_pro');
		self._match_mt(struct,'music_lan');
		self._match_mt(struct,'music_oth');

	def _match_mt(self,struct,mtype):
		mdata = self.mt[mtype];
		keys = mdata.keys();
		taglist = struct['music'];
		for key in keys:
			same = mdata[key]['same'];
			for tag in taglist:
				if type(tag) == dict: continue;
				if tag in same:
					idx = taglist.index(tag);
					tdic = dict();
					tdic['value'] = key;
					tdic['type'] = mtype;
					tdic['scope'] = mdata[key]['scope'];
					taglist[idx] = tdic;

