#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,re
reload(sys);
sys.setdefaultencoding('utf-8');
import common,config,music_com
from myexception import MyException
class MSR:
	def __init__(self):
		self.msr = dict();

	def init(self,dfile):
		try:
			self.msr = music_com.readfile(dfile);
		except MyException as e:
			raise e;

	def encode(self,struct):
		self._match_msr(struct);

	def _match_msr(self,struct):
		inlist = struct['inlist'];
		taglist = struct['music'];
		for instr in taglist:
			if type(instr) == dict: continue;
			tdic = dict();
			tdic['type'] = 'music_msr'
			tdic['value'] = instr;
			idx = taglist.index(instr);
			if self.msr.has_key(instr):
				tdic['scope'] = 'singer';
				taglist[idx] = tdic;
