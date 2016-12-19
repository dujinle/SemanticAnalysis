#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
import struct_utils as Sutil
from myexception import MyException

#进行第1层的解析 合并同一词性的结构
class Fetch01Layer():
	def __init__(self):
		self.data = None;

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			print 'go into fetch 01......' + str(struct['deal']);
			self._fetch_2L(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _fetch_2L(self,struct):
		ret = False;
		for key in self.data.keys():
			item = self.data[key];
			for it in item:
				mret = 0;
				if it.has_key('way') and it['way'] == 'merge':
					mret = self._merge_objs(struct,it);
				else:
					mret = self._fetch_objs(struct,it);
				if mret == 1 and ret == False: ret = True;
		if struct['deal'] == False: struct['deal'] = ret;

	def _fetch_objs(self,struct,item):
		if not struct.has_key(item['key']): return -1;

		merg = pid = 0;
		while True:
			if pid >= len(struct[item['key']]): break;
			pit = struct[item['key']][pid];
			if pit['type'] == item['st'] or item['st'] == '*':
				tid = 0;
				while True:
					if tid >= len(struct[item['key']]): break;
					vit = struct[item['key']][tid];
					if vit['type'] == item['et'] or item['et'] == '*':
						pstr = pit['str'] + item['desc'] + vit['str'];
						comp = re.compile(pstr);
						match = comp.search(struct['text']);
						if not match is None:
							merg = 1;
							pstr = match.group(0);
							if struct['text'].find(pstr) == -1:
								pstr = pstr.replace(item['desc'],'',1);
							if item['force'] == 'tail':
								vit[item['type']] = pit;
								vit['flg'] = True;
								struct['text'] = struct['text'].replace(pstr,vit['str'],1);
								struct['remove'].append(pit['str']);
								del struct[item['key']][pid];
								pid = pid - 1;
							elif item['force'] == 'prev':
								pit[item['type']] = vit;
								pit['flg'] = True;
								struct['text'] = struct['text'].replace(pstr,pit['str'],1);
								struct['remove'].append(vit['str']);
								del struct[item['key']][tid];
								tid = tid - 1;
					tid = tid + 1;
			pid = pid + 1;
		if len(struct[item['key']]) == 0: del struct[item['key']];
		return merg;

	def _merge_objs(self,struct,item):
		if not struct.has_key(item['key']): return -1;
		merg = pid = 0;
		while True:
			if pid >= len(struct[item['key']]): break;
			pit = struct[item['key']][pid];
			if pit['type'] == item['st'] or item['st'] == '*':
				tid = 0;
				while True:
					if tid >= len(struct[item['key']]): break;
					vit = struct[item['key']][tid];
					if vit['type'] == item['et'] or item['et'] == '*':
						pstr = pit['str'] + item['desc'] + vit['str'];
						comp = re.compile(pstr);
						match = comp.search(struct['text']);
						if not match is None:
							merg = 1;
							pstr = match.group(0);
							Sutil._merge_some_words(struct,pstr,0,True);
							tdic = dict();
							tdic['str'] = pstr;
							tdic['stype'] = pit['stype'] + vit['stype'];
							if item['force'] == 'tail': tdic['type'] = vit['type'];
							else: tdic['type'] = pit['type'];
							tdic['stc'] = [pit,vit];
							struct[item['key']].append(tdic);
							if pid > tid:
								del struct[item['key']][tid];
								del struct[item['key']][pid - 1];
							else:
								del struct[item['key']][pid];
								del struct[item['key']][tid - 1];
							pid = pid - 1;
							tid = tid - 1;
					tid = tid + 1;
			pid = pid + 1;
		if len(struct[item['key']]) == 0: del struct[item['key']];
		return merg;

