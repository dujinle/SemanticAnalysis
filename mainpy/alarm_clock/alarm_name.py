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

#find the clock name
class ANA(Base):

	def encode(self,struct):
		try:
			intext = struct['text'];
			inlist = struct['inlist'];
			if not struct.has_key('clocks'): struct['clocks'] = list();
			clocks = struct['clocks'];
			for st in inlist:
				for key in self.data.keys():
					self._match_item(st,clocks,key);
			self._analysis_date(struct);
			self._analysis_delay(struct);
		except MyException as e: raise e;

	def _match_item(self,strs,clocks,mtype):
		mdata = self.data[mtype];
		if type(mdata) == list:
			for idata in mdata:
				if strs in idata['same']:
					tdic = dict(idata);
					tdic['mystr'] = strs;
					tdic['type'] = mtype;
					if mtype == 'action': tdic['type'] = idata['type'];
					clocks.append(tdic);
					break;
		else:
			if strs in mdata['same']:
				tdic = dict();
				tdic['mystr'] = strs;
				tdic['type'] = mtype;
				clocks.append(tdic);

	def _analysis_date(self,struct):
		clocks = struct['clocks'];
		adjust = 000;
		tdic = dict();
		for ck in clocks:
			if ck['type'] == 'set':
				adjust = adjust | (1 << 2);
				tdic['action'] = ck['mystr'];
			if ck['type'] == 'dir':
				adjust = adjust | (1 << 1);
				tdic['dir'] = ck['func'];
			if ck['type'] == 'level':
				adjust = adjust | (1 << 0);
				tdic['value'] = ck['value'];
		if adjust == 7:
			struct['ck_adjust'] = tdic;

	def _analysis_delay(self,struct):
		delay = 0;
		if not struct.has_key('taglist'): return;
		taglist = struct['taglist'];
		tdic = dict();
		for tag in taglist:
			if type(tag) == dict and tag['type'] == 'mood_tm':
				delay = delay | (1 << 1);
				if tag['level'] == 'high' or tag['level'] == 'saturation':
					tdic['type'] = 'last';
				elif tag['level'] == 'low':
					tdic['type'] = 'delay';
		clocks = struct['clocks'];
		for ck in clocks:
			if ck['type'] == 'ring':
				delay = delay | (1 << 0);
				break;
		if delay == 3: struct['delay'] = tdic;

