#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
import struct_utils as Sutil
from myexception import MyException

#进行第二层的解析 合并一些 符合条件的 结构
class Fetch2Layer():
	def __init__(self):
		self.data = None;

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			print 'go into fetch 2......' + str(struct['deal']);
			self._fetch_2L(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _fetch_2L(self,struct):
		ret = False;
		for key in self.data.keys():
			item = self.data[key];
			for it in item:
				mret = self._merge_objs(struct,it);
				if mret == 1 and ret == False:
					ret = True;
		print ret
		if struct['deal'] == False: struct['deal'] = ret;

	def _merge_objs(self,struct,item):
		if not struct.has_key(item['key']): return -1;

		merg = pid = tid = 0;
		while True:
			if pid >= len(struct[item['key']]): break;

			pit = struct[item['key']][pid];
			if pit['type'] <> item['st'] and item['st'] <> '*':
				pid = pid + 1;
				continue;

			tid = 0;
			while True:
				if tid >= len(struct[item['key']]): break;
				vit = struct[item['key']][tid];
				if vit['type'] <> item['et'] and item['et'] <> '*':
					tid = tid + 1;
					continue;

				pstr = pit['str'] + item['desc'] + vit['str'];
				comp = re.compile(pstr);
				match = comp.search(struct['text']);
				if not match is None:
					merg = 1;
					if item['force'] == 'tail':
						vit[item['type']] = pit;
						struct['text'] = struct['text'].replace(pstr,vit['str'],1);
						struct['remove'].append(pit['str']);
						del struct[item['key']][pid];
						pid = pid - 1;
						break;
					elif item['force'] == 'prev':
						pit[item['type']] = vit;
						struct['text'] = struct['text'].replace(pstr,pit['str'],1);
						struct['remove'].append(vit['str']);
						del struct[item['end']][tid];
						tid = tid - 1;
				tid = tid + 1;
			pid = pid + 1;
		if len(struct[item['key']]) == 0: del struct[item['key']];
		return merg;
