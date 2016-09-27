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
from base import Base

#根据模板区分不同的场景
class PrevScene(Base):

	def encode(self,struct):
		try:
			self._replace_time_tag(struct);
		except MyException as e: raise e;

	def _replace_time_tag(self,struct):
		if struct.has_key('intervals') and len(struct['intervals']) > 0:
			inters = struct['intervals'];
			struct['rep'] = list();
			for ints in inters:
				tstr = ints['str'].replace('_','');
				struct['rep'].append(tstr);
				struct['text'] = struct['text'].replace(tstr,'time',1);

