#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,copy
import re,time,math
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

class AAD(Base):

	def encode(self,struct):
		try:
			intext = struct['text'];
			inlist = struct['inlist'];
			if not struct.has_key('clocks'): struct['clocks'] = list();
			clocks = struct['clocks'];
			if struct.has_key('taglist'):
				clocks.extend(struct['taglist']);
				del struct['taglist'];
			for st in inlist:
				for key in self.data.keys():
					self._match_item(st,clocks,key);
			self._analysis_date(struct);
			self._analysis_delay(struct);
			self._find_time(struct);
			self._analysis_able(struct);
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

	def _find_time(self,struct):
		clocks = struct['clocks'];
		tdic = dict();
		for ck in clocks:
			if ck['type'] == 'time_ut':
				tstr = scope = '';
				for tm in ck['times']:
					tstr = tstr + tm['value'];
					if tm['scope'] == 'day': scope = 'day';
				tdic['tname'] = tstr;
				tdic['scope'] = scope;
				tdic['time'] = ck['interval'][0];
				struct['ck_time'] = tdic;
				clocks.remove(ck);
				break;

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
			struct['adjust_date'] = tdic;

	def _analysis_delay(self,struct):
		delay = 0;
		tdic = dict();
		clocks = struct['clocks'];
		for ck in clocks:
			if ck['type'] == 'delay':
				tdic['type'] = ck['style'];
				delay = delay | (1 << 1);
			elif ck['type'] == 'ring':
				delay = delay | (1 << 0);
				break;
		if delay == 3: struct['ck_delay'] = tdic;

	def _analysis_able(self,struct):
		able = ept = 0;
		clocks = struct['clocks'];
		for ck in clocks:
			if ck['type'] == 'able':
				if ck['style'] == 'wordday':
					able = math.pow(2,5) - 1;
				elif ck['style'] == 'allin':
					able = math.pow(2,8) - 1;
				elif ck['style'] == 'workend':
					able = math.pow(2,7) - math.pow(2,5);
			if ck['type'] == 'time_wt':
				tm = ck['times'][0];
				if tm.has_key('num'):
					able = math.pow(2,int(tm['num']) - 1);
			if ck['type'] == 'except': ept = 1;
		if ept == 1: able = math.pow(2,7) - 1 - able;
		if able > 0: struct['ck_able'] = able;
