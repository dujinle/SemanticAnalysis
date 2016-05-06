#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,copy
import re,time,math,datetime
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import common
from myexception import MyException
from scene_base import SceneBase
#根据模板区分不同的场景
class SceneReplace(SceneBase):

	def encode(self,struct):
		try:
			self._replace_str(struct);
			self._deal_time_rep(struct);
		except MyException as e: raise e;

	def _replace_str(self,struct):
		for reg in self.data['rep']:
			regstr = reg['reg'];
			value = reg['value'];
			compstr = re.compile(regstr);
			match = compstr.search(struct['text']);
			if not match is None:
				struct['text'] = struct['text'].replace(match.group(0),value);

	def _deal_time_rep(self,struct):
		com = re.compile(self.data['time_rep']);
		match = com.search(struct['text']);
		if not match is None:
			tstr = match.group(0);
			print tstr;
			if len(tstr) <> 4: return None;
			thour = tstr[2:];
			tnum = thour[0];
			nnum = int(tnum) + 10;
			phour = thour.replace(tnum,str(nnum));
			pstr = tstr.replace(thour,phour);
			struct['text'] = struct['text'].replace(tstr,pstr);

