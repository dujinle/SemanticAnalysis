#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
import struct_utils as Sutil
from myexception import MyException

#抓取对象与特殊词之间的关系 并标注
class FetchArtist():
	def __init__(self):
		self.data = None;

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			if not struct.has_key('Artist'): struct['Artist'] = list();
			self._fetch_artist(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _fetch_artist(self,struct):
		for key in self.data.keys():
			item = self.data[key];
			for it in item:
				for art in it['artists']:
					if struct.has_key(art):
						self._fetch_true(struct,it['reg'],art,it['pos'],key);

	def _fetch_true(self,struct,reg,objs_key,pos,key):
		tid = 0;
		while True:
			if tid >= len(struct[objs_key]): break;
			it = struct[objs_key][tid];
			#在 SP,ST,SB,STH
			pp = reg + it['str'];

			#SP,ST,SB,STH 在 
			if pos == 'after': pp = it['str'] + reg;
			comp = re.compile(pp);
			match = comp.search(struct['text']);
			if not match is None:
				tdic = dict();
				tdic['type'] = key + it['type'];
				tdic['stype'] = key + it['stype'];
				tdic['str'] = match.group(0);
				tdic['art'] = it;
				if pos == 'after':
					tdic['type'] = it['type'] + key;
					tdic['stype'] = it['stype'] + key;
				struct['Artist'].append(tdic);
				del struct[objs_key][tid];
				tid = tid - 1;
			tid = tid + 1;
