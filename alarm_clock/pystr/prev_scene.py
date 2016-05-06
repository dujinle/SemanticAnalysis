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
class PrevScene(SceneBase):

	def encode(self,struct):
		try:
			self._filter_time_str(struct);
			self._replace_time_tag(struct);
		except Exception as e:
			raise MyException(sys.exc_info());

	def _replace_time_tag(self,struct):
		if struct.has_key('intervals') and len(struct['intervals']) > 0:
			inters = struct['intervals'];
			struct['rep'] = list();
			for ints in inters:
				tstr = ints['str'].replace('_','');
				struct['rep'].append(tstr);
				struct['text'] = struct['text'].replace(tstr,'time#',1);

	def _filter_time_str(self,struct):
		if not struct.has_key('intervals'):
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
				del struct['intervals'][cur];

	def _get_tag_ptime(self,struct,tstr):
		tnum = 0;
		for inter in struct['intervals']:
			time_str = inter['str'].replace('_','');
			pid = tstr.find(time_str);
			if pid == -1:
				break;
			else:
				tnum = tnum + 1;
				tstr = tstr[pid + len(time_str):];
		return tnum;

