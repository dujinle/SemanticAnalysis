#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,re
reload(sys);
sys.setdefaultencoding('utf-8');
import common,config,localmm
from myexception import MyException
class CR:
	def __init__(self):
		self.reg = u'L[与和]{1}L[的]*交叉[路]*口';

	def init(self,fdir):
		pass;

	def encode(self,struct):
		self._calc_them(struct);

	def _calc_them(self,struct):
		taglist = struct['locals'];
		strs = '';
		for tag in taglist:
			if type(tag) == dict and tag['type'].find('local') <> -1:
				strs = strs + 'L';
			else:
				strs = strs + tag;
		comp = re.compile(self.reg);
		match = comp.search(strs);
		while True:
			if match is None: return None;
			idx = strs.find(match.group(0));
			first = self._num_tag(strs,idx,taglist);
			tdic = dict();
			f1 = taglist[first];
			yu = taglist[first + 1];
			f2 = taglist[first + 2];
			tdic['d1'] = dict(f1);
			tdic['d2'] = dict(f2);
			tdic['type'] = 'local_cross';
			taglist[first] = tdic;
			del taglist[first + 1];
			del taglist[first + 1];
			if taglist[first + 1] == u'的':
				del taglist[first + 1];
			del taglist[first + 1];
			strs = strs.replace(match.group(0),'LL',1);
			match = comp.search(strs);

	def _num_tag(self,strs,idx,taglist):
		mystr = strs[:idx];
		ms = re.findall('L',mystr);
		num = len(ms);
		idx = 0
		while True:
			if idx >= len(taglist): break;
			tag = taglist[idx];
			if type(tag) == dict and tag['type'].find('local') <> -1:
				if num <= 0: return idx;
				else: num = num - 1;
			idx = idx + 1;
		return idx - 1;

