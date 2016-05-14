#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,re,common
from myexception import MyException
import struct_utils as Sutil

#标记相对代词 这个可以和单位组合指定代词
class MarkRelat():
	def __init__(self):
		self.data = dict();

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception:
			raise MyException(sys.exc_info());

	def encode(self,struct):
		try:
			if not struct.has_key('Relat'): struct['Relat'] = list();
			if not struct.has_key('RelatStc'): struct['RelatStc'] = list();
			self._mark_relat(struct);
			self._merge_unit(struct);
			self._reset_inlist(struct);
			if len(struct['Relat']) == 0: del struct['Relat'];
			if len(struct['RelatStc']) == 0: del struct['RelatStc'];
		except Exception as e:
			raise MyException(sys.exc_info());

	def _mark_relat(self,struct):
		for key in self.data.keys():
			item = self.data[key];
			for it in item:
				reg_str = '';
				for istr in it['reg']: reg_str = reg_str + '(' + istr + ')|'
				if reg_str[-1] == '|': reg_str = reg_str[0:-1];
				com = re.compile(reg_str);
				match = com.search(struct['text']);
				if match is None: continue;
				tdic = dict();
				tdic['type'] = key;
				tdic['stype'] = it['type'];
				tdic['str'] = match.group(0);
				struct['Relat'].append(tdic);
		Sutil._sort_by_apper(struct,'Relat');

	def _merge_unit(self,struct):
		if not struct.has_key('unit_list'): return None;
		pid = tid = 0;
		while True:
			if pid >= len(struct['Relat']): break;
			pit = struct['Relat'][pid];
			tid = 0;
			while True:
				if tid >= len(struct['unit_list']): break;
				unit = struct['unit_list'][tid];
				ustr = pit['str'] + unit['str'];
				if struct['text'].find(ustr) <> -1:
					tdic = dict();
					tdic['type'] = 'RELAT';
					tdic['stype'] = pit['stype'];
					tdic['str'] = ustr;
					tdic['stc'] = [pit,unit];
					struct['RelatStc'].append(tdic);
					del struct['Relat'][pid];
					del struct['unit_list'][tid];
					pid = pid - 1;
					break;
				tid = tid + 1;
			pid = pid + 1;
		if len(struct['unit_list']) == 0: del struct['unit_list'];

	def _reset_inlist(self,struct):
		tid = 0;
		for item in struct['RelatStc']:
			tid = Sutil._merge_some_words(struct,item['str'],tid);
