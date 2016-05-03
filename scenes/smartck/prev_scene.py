#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,copy
import re,time,math,datetime

import common
from common import logging
from myexception import MyException
from scene_base import SceneBase
#根据模板区分不同的场景
class PrevScene(SceneBase):

	def encode(self,struct):
		try:
			self._filter_time_str(struct);
			self._replace_time_tag(struct);
		except Exception as e:
			raise MyException(sys.exc_info());

	def _replace_time_tag(self,struct):
		if struct.has_key('Times') and len(struct['Times']) > 0:
			inters = struct['Times'];
			struct['time_strs'] = list();
			for ints in inters:
				tstr = ints['str'].replace('_','');
				tid = struct['text'].find(tstr);
				cid = idx = i = slen = 0;
				remove = set();
				for i,istr in enumerate(struct['inlist']):
					if idx == tid:
						if slen == len(tstr): break;
						if slen > len(tstr):
							logging.error('word not can be found');
							return None;
						remove.add(i);
						slen = slen + len(istr);
						continue;
					if idx > tid:
						logging.error('word not can be found');
						return None;
					idx = idx + len(istr);
				for i,j in enumerate(remove):
					if i == 0:
						del struct['inlist'][j];
						cid = j;
					else: del struct['inlist'][cid];
				struct['inlist'].insert(cid,tstr);
				struct['time_strs'].append(tstr);


	def _filter_time_str(self,struct):
		if not struct.has_key('Times'):
			return None;
		for reg in self.data['filter']:
			regstr = reg['reg'];
			compstr = re.compile(regstr);
			match = compstr.search(struct['text']);
			if not match is None:
				pid = struct['text'].find(match.group(0));
				tlen = len(match.group(0));
				pstr = struct['text'][:pid];
				cur = self._get_tag_ptime(struct,pstr);
				del struct['Times'][cur];

	def _get_tag_ptime(self,struct,tstr):
		tnum = 0;
		for inter in struct['Times']:
			time_str = inter['str'].replace('_','');
			pid = tstr.find(time_str);
			if pid == -1:
				break;
			else:
				tnum = tnum + 1;
				tstr = tstr[pid + len(time_str):];
		return tnum;

