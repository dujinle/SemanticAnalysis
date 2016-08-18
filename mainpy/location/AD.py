#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
reload(sys);
sys.setdefaultencoding('utf-8');
import common,config,localmm
from myexception import MyException
class AD:
	def __init__(self):
		self.S = dict();
		self.q = dict();
		self.p = dict();
		self.x = dict();
		self.c = dict();
		self.l = dict();
		self.s = dict();
		self.poi = dict();

	def init(self,fdir):
		try:
			self.q.update(localmm.readfile(fdir + '/BJHDQ.txt'));
			self.S.update(localmm.readfile(fdir + '/GSQ.txt'));
			self.x.update(localmm.readfile(fdir + '/BJHDX.txt'));
			self.x.update(localmm.readfile(fdir + '/GJH.txt'));
			self.c.update(localmm.readfile(fdir + '/BJHDC.txt'));
			self.s.update(localmm.readfile(fdir + '/BJHDS.txt'));
			self.p.update(localmm.readfile(fdir + '/BJHDP.txt'));
		except MyException as e:
			raise e;

	def encode(self,struct):
		self._paser_addr(struct);
		self._paser_poi(struct);
		self._paser_adcode(struct);
		self._calc_them(struct);

	def _paser_addr(self,struct):
		inlist = struct['inlist'];
		taglist = struct['locals'];
		for instr in taglist:
			if type(instr) == dict: continue;
			tdic = dict();
			tdic['type'] = 'local'
			tdic['value'] = instr;
			idx = taglist.index(instr);
			if self.q.has_key(instr):
				tdic['scope'] = 'q';
				taglist[idx] = tdic;
			elif self.x.has_key(instr):
				tdic['scope'] = 'x';
				taglist[idx] = tdic;
			elif self.c.has_key(instr):
				tdic['scope'] = 'c';
				taglist[idx] = tdic;
			elif self.S.has_key(instr):
				tdic['scope'] = 'S';
				taglist[idx] = tdic;

	def _paser_poi(self,struct):
		inlist = struct['inlist'];
		taglist = struct['locals'];
		for instr in inlist:
			tdic = dict();
			tdic['type'] = 'local';
			tdic['value'] = instr;
			if self.p.has_key(instr):
				idx = taglist.index(instr);
				tdic['scope'] = 'p';
				taglist[idx] = tdic;

	def _paser_adcode(self,struct):
		inlist = struct['inlist'];
		taglist = struct['locals'];
		idx = 0
		while True:
			if idx >= len(taglist): break;
			instr = taglist[idx];
			if type(instr) == dict:
				idx = idx + 1;
				continue;
			if self.s.has_key(instr):
				tdic = dict();
				tdic['type'] = 'local';
				tdic['scope'] = 'l';
				if idx < len(taglist) - 2:
					if taglist[idx + 2] == u'号':
						instr = instr + taglist[idx + 1] + taglist[idx + 2];
						del taglist[idx + 1];
						del taglist[idx + 1];
				tdic['value'] = instr;
				taglist[idx] = tdic;
			idx = idx + 1;

	def _calc_them(self,struct):
		taglist = struct['locals'];
		tdic = None;
		idx = firstidx = 0;
		flag = False;
		while True:
			if idx >= len(taglist): break;
			tag = taglist[idx];
			if type(tag) == dict and tag['type'] == 'local':
				scope = tag['scope'];
				if flag == False:
					flag = True;
					tdic = dict();
					tdic['type'] = 'locals';
					tdic[scope] = tag['value'];
					firstidx = idx;
				elif flag == True:
					tdic[scope] = tag['value'];
					del taglist[idx];
					idx = idx - 1;
			else:
				if not tdic is None:
					taglist[firstidx] = tdic;
					flag = False;
					tdic = None;
			idx = idx + 1;
		if flag == True:
			taglist[firstidx] = tdic;

