#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,re,common
from myexception import MyException
import struct_utils as Sutil

#介词的搭配组合计算
class MarkPrepCombine():
	def __init__(self):
		self.data = dict();

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception:
			raise MyException(sys.exc_info());

	def encode(self,struct):
		try:
			if not struct.has_key('PrepCom'): struct['PrepCom'] = list();
			self._mark_pcom_tag(struct);
			self._reset_inlist(struct);
		except Exception as e:
			raise MyException(sys.exc_info());

	def _mark_pcom_tag(self,struct):
		if not struct.has_key('objs'): return None;
		for key in self.data.keys():
			item = self.data[key];
			for ni in item:
				ni['key'] = key;
				if self._mark_words(struct,ni) == True: break;

	def _reset_inlist(self,struct):
		tid = 0;
		for item in struct['PrepCom']:
			tid = Sutil._merge_some_words(struct,item['str'],tid);

	def _mark_words(self,struct,reg_dic):
		reg = reg_dic['calc_reg'].replace('KEY',reg_dic['reg']);
		com = re.compile(reg);
		if reg['pos'] == 'after' or reg['pos'] == 'prev':
			for item in struct['objs']:
				text = struct['text'].replace(item['str'],item['stype']);
				match = com.search(text);
				if match is None: continue;
				tdic = dict();
				tdic['str'] = match.group(0).replace(item['stype'],item['str']);
				if struct['text'].find(tdic['str']) <> -1:
					tdic['stype'] = reg['key'];
					tdic['obj'] = item;
					struct['PrepCom'].append(tdic);
					return True;
		elif reg['pos'] == 'mid':
			for i1 in struct['objs']:
				text = struct['text'].replace(i1['str'],i1['stype']);
				for i2 in struct['objs']:
					text = text.replace(i2['str'],i2['stype']);
					match = com.search(text);
					if match is None: continue;
					tdic = dict();
					tdic['str'] = match.group(0).replace(i1['stype'],i1['str']).replace(i2['stype'],i2['str']);
					if struct['text'].find(tdic['str']) <> -1:
						tdic['stype'] = reg['key'];
						tdic['objs'] = [i1,i2]
						struct['PrepCom'].append(tdic);
						return True;
		return False;


