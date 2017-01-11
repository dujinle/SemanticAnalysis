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

#find alarm name so we can make sure which clock this is #
class AlarmFname():

	def encode(self,struct):
		try:
			self._remove_ckdesc(struct);
			self._find_text(struct);
			if not struct.has_key('ck_name') or struct['ck_name'] == '':
				self._find_inlist(struct);
			if struct.has_key('ck_name') and struct['ck_name'] == u'所有':
				struct['ck_name'] = '';
		except MyException as e: raise e;

	#remove clock desc words like 这个 那个 这 那#
	def _remove_ckdesc(self,struct):
		inlist = struct['inlist'];
		if not struct.has_key('clocks'): return None;
		clocks = struct['clocks'];
		for ck in clocks:
			if ck['type'] == 'filter':
				inlist.remove(ck['mystr']);
				clocks.remove(ck);
				struct['text'] = struct['text'].replace(ck['mystr'],'');

	#find the clock name from inlist#
	def _find_inlist(self,struct):
		if not struct.has_key('clocks'): return None;
		inlist = struct['inlist'];
		clocks = struct['clocks'];
		ckname_id = -1;
		for ck in clocks:
			if ck['type'] == 'clock':
				ckname_id = inlist.index(ck['mystr']);
				break;
		if ckname_id >= 2 and inlist[ckname_id - 1] == u'的':
			if len(inlist[ckname_id - 2]) > 1:
				struct['ck_name'] = inlist[ckname_id - 2];
		else:
			struct['ck_name'] = '';

	#find the clock name from text#
	def _find_text(self,struct):
		if not struct.has_key('clocks'): return None;
		if not struct.has_key('ck_time'): return None;
		clocks = struct['clocks'];
		text = struct['text'];
		idx = -1;
		for ck in clocks:
			if ck['type'] == 'clock':
				idx = text.find(ck['mystr']);
				break;
		if idx >= 2 and text[idx - 1] == u'的':
			name_str = struct['ck_time']['str'].replace('_','');
			pid = text.find(name_str);
			if pid <> -1 and (pid + len(name_str)) == (idx - 1):
				struct['ck_name'] = struct['ck_time']['time'];
				del struct['ck_time'];
		if not struct.has_key('ck_name'):
			struct['ck_name'] = '';

