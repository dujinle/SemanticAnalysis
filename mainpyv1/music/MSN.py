#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,re
reload(sys);
sys.setdefaultencoding('utf-8');
import common,config,music_com
from myexception import MyException
class MSN:
	def __init__(self):
		self.data = None;
	def init(self,dfile):
		try:
			self.data = music_com.readfile(dfile);
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
			tdic['type'] = 'music_msn'
			tdic['value'] = instr;
			idx = taglist.index(instr);
			if self.data.has_key(instr):
				tdic['scope'] = 'singname';
				taglist[idx] = tdic;

	def _add(self,data):
		try:
			value = data['value'];
			if not self.data.has_key(value):
				self.data[value] = 1;
		except Exception as e:
			raise MyException(format(e));

	def _del(self,data):
		try:
			value = data['value'];
			if self.data.has_key(value):
				del self.data[value];
		except Exception as e:
			raise MyException(format(e));

	def _get(self,data):
		return self.data;

	def write_file(self,dfile):
		try:
			if dfile is None: return None;
			os.rename(dfile,dfile + '.1');
			fd = open(dfile,'w');
			for key in self.data.keys():
				fd.write(key + '\n');
			fd.close();
		except Exception as e:
			raise MyException(format(e));
