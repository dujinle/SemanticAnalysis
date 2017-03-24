#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException
import hanzi2num as Han2Dig
from fetch_base import FetchBase
import struct_utils as Sutil
#处理数字单位的组合
class FetchNunit(FetchBase):

	def encode(self,struct):
		try:
			self._fetch_num(struct);
			self._fetch_unit(struct);
			self._fetch_num_unit(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _fetch_num(self,struct):
		if not struct.has_key('SomeNums'): struct['SomeNums'] = list();
		words = struct['text'];
		match = self._match_num_reg(words);
		for key in match.keys():
			item = match[key];
			for it in item:
				tdic = dict();
				tdic['type'] = 'NUM';
				if key == 'nreg' or key == 'freg':
					tdic['stype'] = it;
				else:
					tdic['stype'] = str(Han2Dig.cn2dig(it));
				tdic['str'] = it;
				struct['SomeNums'].append(tdic);

	def _match_num_reg(self,words):
		data = self.data['SomeNums'];
		tdic = dict();
		for key in data:
			idata = data[key];
			comp = re.compile(idata);
			match = comp.findall(words);
			if match is None or len(match) == 0:
				continue;
			tdic[key] = match;
		return tdic;

	def _fetch_unit(self,struct):
		if not struct.has_key('SomeUnits'): struct['SomeUnits'] = list();
		data = self.data['SomeUnits'];
		if data is None: return None;

		idx = 0;
		while True:
			if idx >= len(struct['text']): break;
			strs = struct['text'][idx:];
			wd = '';
			wlist = list();
			for word in list(strs):
				wd = wd + word;
				if data.has_key(wd):
					wlist.append(wd);
			max_len = 0;
			words = None;
			for istr in wlist:
				if len(istr) > max_len:
					max_len = len(istr);
					words = istr;
			if not words is None:
				tdic = data[words];
				struct['SomeUnits'].append(tdic);
				idx = idx + len(words) - 1;
			idx = idx + 1;

	def _fetch_num_unit(self,struct):
		if not struct.has_key('SomeNums'): return -1;
		if not struct.has_key('SomeUnits'): return -1;
		if not struct.has_key('Nunit'): struct['Nunit'] = list();
		pid = 0;
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
				match = comp.search(struct['text']);
				if not match is None:
					pstr = match.group(0);
#					Sutil._merge_some_words(struct,pstr,0,True);
					tdic = dict();
					tdic['str'] = pstr;
					tdic['type'] = 'NUNIT';
					tdic['stype'] = 'NUM';
					tdic['stc'] = [pit,vit];
					struct['Nunit'].append(tdic);
					del struct['SomeUnits'][tid];
					del struct['SomeNums'][pid];
					tid = tid - 1;
					pid = pid - 1;
				tid = tid + 1;
			pid = pid + 1;
