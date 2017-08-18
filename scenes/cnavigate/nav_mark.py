#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common
from myexception import MyException
from scene_base import SceneBase
import wsvd_words as Wsvd

#标记用户列表中的数据
class NavMark(SceneBase):

	def encode(self,struct,super_b):
		try:
			self._mark_body(struct,super_b);
			Wsvd.encode(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_body(self,struct,super_b):
		data = super_b.data['CONTACTS'];

		for key in data.keys():
			idx = struct['text'].find(key);
			if idx == -1: continue;
			if struct['stc'].has_key(key): continue;
			tdic = dict(data[key]);
			tdic['type'] = 'NB';
			tdic['stype'] = 'PERSON';
			tdic['str'] = key;
			struct['stc'][key] = tdic;

