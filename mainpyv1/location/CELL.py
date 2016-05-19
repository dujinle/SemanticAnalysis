#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,re
reload(sys);
sys.setdefaultencoding('utf-8');
import common,config,localmm
from myexception import MyException
class CELL:
	def __init__(self):
		self.cell = dict();
		self.regs = [u'住宅区',u'家属[楼院]{1}',u'宿舍',u'[0-9]{1,}[号]*院'];

	def init(self,fdir):
		try:
			self.cell = localmm.readfile(fdir + '/BJHDCELL.txt');
		except MyException as e:
			raise e;

	def encode(self,struct):
		self._paser_cell(struct);
		self._calc_them(struct);

	def _paser_cell(self,struct):
		inlist = struct['inlist'];
		taglist = struct['locals'];
		for instr in taglist:
			if type(instr) == dict: continue;
			tdic = dict();
			tdic['type'] = 'local'
			tdic['value'] = instr;
			idx = taglist.index(instr);
			if self.cell.has_key(instr):
				tdic['scope'] = 'cell';
				taglist[idx] = tdic;

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
				if scope == 'cell':
					mtag = taglist[idx];
					match = self._match_cell(taglist,idx);
					if match is None:
						idx = idx + 1;
						continue;
					mstr = match.group(0);
					mtag['value'] = mtag['value'] + mstr;
					midx = idx + 1;
					strs = '';
					while True:
						if midx >= len(taglist): break;
						mtag = taglist[midx];
						if type(mtag) == dict: break;
						strs = strs + mtag;
						if mstr.find(strs) <> -1:
							del taglist[midx];
							midx = midx - 1;
						midx = midx + 1;
			idx = idx + 1;

	def _match_cell(self,taglist,idx):
		if idx + 1 >= len(taglist): return None;
		mytags = taglist[idx + 1:];
		strs = '';
		for m in mytags:
			if type(m) == dict: break;
			strs = strs + m;
		match = None;
		for reg in self.regs:
			comp = re.compile(reg);
			match = comp.match(strs);
			if match is None: continue;
			else: return match;
