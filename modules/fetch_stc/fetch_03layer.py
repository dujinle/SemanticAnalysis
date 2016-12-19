#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
import struct_utils as Sutil
from myexception import MyException

#进行第三层的解析 合并一些 符合条件的 结构
class Fetch03Layer():
	def __init__(self):
		self.data = None;

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			print 'go into fetch 03......' + str(struct['deal']);
			self._fetch_03L(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _fetch_03L(self,struct):
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
		if not struct.has_key(item['start']): return -1;
		if not struct.has_key(item['end']): return -1;

		merg = pid = tid = 0;
		while True:
			if pid >= len(struct[item['start']]): break;

			pit = struct[item['start']][pid];
			if pit['type'] <> item['st'] and item['st'] <> '*':
				pid = pid + 1;
				continue;

			tid = 0;
			while True:
				if tid >= len(struct[item['end']]): break;
				vit = struct[item['end']][tid];
				if vit['type'] <> item['et'] and item['et'] <> '*':
					tid = tid + 1;
					continue;

				pstr = pit['str'] + vit['str'];
				comp = re.compile(pstr);
				match = comp.search(struct['text']);
				if not match is None:
					if item['force'] == 'tail':
						if not vit.has_key(item['type']):
							merg = 1;
							vit[item['type']] = pit;
							vit['flg'] = True;
							struct['text'] = struct['text'].replace(pstr,vit['str'],1);
							struct['remove'].append(pit['str']);
							del struct[item['start']][pid];
							pid = pid - 1;
					elif item['force'] == 'prev':
						if not pit.has_key(item['type']):
							merg = 1;
							pit[item['type']] = vit;
							pit['flg'] = True;
							struct['text'] = struct['text'].replace(pstr,pit['str'],1);
							struct['remove'].append(vit['str']);
							del struct[item['end']][tid];
							tid = tid - 1;
				tid = tid + 1;
			pid = pid + 1;
		if len(struct[item['end']]) == 0: del struct[item['end']];
		if len(struct[item['start']]) == 0: del struct[item['start']];
		return merg;
