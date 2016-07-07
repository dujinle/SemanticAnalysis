#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,copy
import re,time
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import common,alarm_common
from myexception import MyException
from base import Base

#find alarm name so we can make sure which clock this is #
class ACname(Base):

	def encode(self,struct):
		try:
			self._remove_ckdesc(struct);

			intext = struct['text'];
			self._find_text(struct);
			if not struct.has_key('ck_name') or struct['ck_name'] == 'null':
				self._find_inlist(struct);
		except MyException as e: raise e;

	#remove clock desc words like 这个 那个 这 那#
	def _remove_ckdesc(self,struct):
		inlist = struct['inlist'];
		idx = 0;
		while True:
			if idx >= len(inlist): break;
			tstr = inlist[idx];
			if tstr in self.data['ck_desc']:
				del inlist[idx];
				continue;
			idx = idx + 1;
		for st in self.data['ck_desc']:
			struct['text'] = struct['text'].replace(st,'');

	#find the clock name from inlist#
	def _find_inlist(self,struct):
		inlist = struct['inlist'];
		ckname_id = -1;
		for st in inlist:
			if st in self.data['ck_name']:
				ckname_id = inlist.index(st);
				break;
		if ckname_id >= 2 and inlist[ckname_id - 1] == u'的':
			struct['ck_name'] = inlist[ckname_id - 2];
		else:
			struct['ck_name'] = 'null';

	#find the clock name from text#
	def _find_text(self,struct):
		text = struct['text'];
		idx = -1;
		for k in self.data['ck_name']:
			idx = text.find(k);
			if idx >= 0: break;
		if idx >= 2 and text[idx - 1] == u'的':
			if text[:idx - 1].find('T') <> -1:
				if struct.has_key('ck_time'):
					struct['ck_name'] = struct['ck_time']['tname'];
		if not struct.has_key('ck_name'):
			struct['ck_name'] = 'null';


