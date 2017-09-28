#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException
import hanzi2num as Han2Dig
import struct_utils as Sutil
#处理数字单位的组合
class CombineObjs():

	def load_data(self,dfile): pass;

	def encode(self,struct):
		try:
			self._fetch_num(struct);
			self._fetch_eng(struct);
			self._fetch_num_unit(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _fetch_num(self,struct):
		if not struct.has_key('SomeNums'): struct['SomeNums'] = list();
		words = struct['text'];
		comp = re.compile('[0-9.]+');
		matchs = comp.findall(words);
		if matchs is None: return False;
		for match in matchs:
			tdic = dict();
			tdic['type'] = 'NUM';
			tdic['stype'] = match;
			tdic['str'] = match;
			struct['SomeNums'].append(tdic);

	def _fetch_eng(self,struct):
		if not struct.has_key('SomeEngs'): struct['SomeEngs'] = list();
		words = struct['text'];
		comp = re.compile('[a-zA-Z]+');
		matchs = comp.findall(words);
		if matchs is None: return False;
		for match in matchs:
			tdic = dict();
			tdic['type'] = 'ENG';
			tdic['stype'] = match;
			tdic['str'] = match;
			struct['SomeEngs'].append(tdic);

	def _fetch_num_unit(self,struct):
		if not struct.has_key('SomeNums'): return -1;
		if not struct.has_key('SomeUnits'): return -1;
		if not struct.has_key('SomeNunit'): struct['SomeNunit'] = list();
		pid = 0;
		test = struct['text'];
		while True:
			if pid >= len(struct['SomeNums']): break;
			pit = struct['SomeNums'][pid];
			tid = 0;
			while True:
				if len(struct['SomeNums']) < 0: break;
				if tid >= len(struct['SomeUnits']): break;
				vit = struct['SomeUnits'][tid];
				pstr = pit['str'] + vit['str'];
				comp = re.compile(pstr);
				match = comp.search(test);
				if not match is None:
					pstr = match.group(0);
					tdic = dict();
					tdic['str'] = pstr;
					tdic['type'] = 'NUNIT';
					tdic['stype'] = 'NUNIT';
					tdic['stc'] = [pit,vit];
					struct['SomeNunit'].append(tdic);
					del struct['SomeUnits'][tid];
					del struct['SomeNums'][pid];
					tid = tid - 1;
					pid = pid - 1;
					test = test.replace(pstr,'',1);
				tid = tid + 1;
			pid = pid + 1;
