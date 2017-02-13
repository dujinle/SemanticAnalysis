#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
import struct_utils as Sutil
from myexception import MyException

#进行第2层的解析 合并一些 符合条件的 词组 比如 数字单位组个
class Fetch02Layer():
	def __init__(self):
		self.data = None;

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			print 'go into fetch 02......' + str(struct['deal']);
			self._fetch_02L(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _fetch_02L(self,struct):
		ret = False;
		for key in self.data.keys():
			item = self.data[key];
			if key == 'MERGE':
				for it in item:
					mret = self._merge_objs(struct,it);
					if mret == 1 and ret == False:
						ret = True;
			'''
			elif key == 'USELESS':
				for it in item:
					mret = self._fetch_useless(struct,it);
					if mret == 1 and ret == False:
						ret = True;
			'''
		print ret
		struct['deal'] = ret;

	def _merge_objs(self,struct,item):
		if not struct.has_key(item['start']): return -1;
		if not struct.has_key(item['end']): return -1;
		if not struct.has_key(item['key']): struct[item['key']] = list();
		merg = pid = tid = 0;
		while True:
			if len(struct[item['start']]) <= 0: break;
			if pid >= len(struct[item['start']]): break;
			pit = struct[item['start']][pid];
			if item['st'] <> '*' and item['st'] <> pit['type']:
				pid = pid + 1;
				continue;
			tid = 0;
			while True:
				if len(struct[item['start']]) <= 0: break;
				if tid >= len(struct[item['end']]): break;
				vit = struct[item['end']][tid];
				if item['et'] <> '*' and item['et'] <> vit['type']:
					tid = tid + 1;
					continue;
				pstr = pit['str'] + vit['str'];
				comp = re.compile(pstr);
				match = comp.search(struct['text']);
				if not match is None:
					print pstr,match.group(0),pid,tid;
					merg = 1;
					tdic = dict();
					tdic['str'] = pstr;
					if item['force'] == 'tail':
						tdic['type'] = vit['type'];
						tdic['stype'] = vit['stype'];
					elif item['force'] == 'prev':
						tdic['type'] = pit['type'];
						tdic['stype'] = pit['stype'];
					elif item['force'] == 'all':
						tdic['stype'] = pit['stype'] + vit['stype'];
					if item.has_key('type'):
						tdic['type'] = item['type'];
					tdic['stc'] = [pit,vit];
					tdic['flg'] = True;
					struct[item['key']].append(tdic);
					struct['remove'].append(pit['str']);
					struct['remove'].append(vit['str']);
					common.print_dic(struct[item['start']][pid]);
					common.print_dic(struct[item['end']][tid]);
					del struct[item['start']][pid];
					del struct[item['end']][tid];
					pid = pid - 1;
					Sutil._merge_some_words(struct,pstr,0,True);
					break;
				tid = tid + 1;
			pid = pid + 1;
		if len(struct[item['end']]) == 0: del struct[item['end']];
		if len(struct[item['start']]) == 0: del struct[item['start']];
		return merg;

	def _fetch_useless(self,struct,key):
		if not struct.has_key(key): return -1;
		if len(struct[key]) == 0: return -1;
		merg = tid = 0;
		while True:
			if tid >= len(struct[key]): break;
			vit = struct[key][tid];
			if struct['text'].find(vit['str']) <> -1:
				merg = 1;
				struct['text'] = struct['text'].replace(vit['str'],'',1);
			tid = tid + 1;
		return merg;
