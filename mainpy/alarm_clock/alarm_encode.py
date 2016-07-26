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

class AlarmEncode(Base):

	def encode(self,struct):
		try:
			intext = struct['text'];
			inlist = struct['inlist'];
			if not struct.has_key('clocks'): struct['clocks'] = list();
			clocks = struct['clocks'];
			if struct.has_key('taglist'):
				clocks.extend(struct['taglist']);
				del struct['taglist'];
			if struct.has_key('music'):
				for music in struct['music']:
					if type(music) == dict:
						clocks.append(music);
				del struct['music'];

			for st in inlist:
				for key in self.data.keys():
					self._match_item(st,clocks,key);
			self._analysis_date(struct);
			self._analysis_delay(struct);
			self._find_time(struct);
			self._analysis_able(struct);
			self._analysis_bell(struct);
			self._find_action(struct);
		except MyException as e: raise e;

	def _match_item(self,strs,clocks,mtype):
		mdata = self.data[mtype];
		if type(mdata) == list:
			for idata in mdata:
				if strs in idata['same']:
					tdic = dict(idata);
					tdic['mystr'] = strs;
					tdic['type'] = mtype;
					if idata.has_key('type'):
						tdic['type'] = idata['type'];
					clocks.append(tdic);
					break;
		else:
			if strs in mdata['same']:
				tdic = dict();
				tdic['mystr'] = strs;
				tdic['type'] = mtype;
				clocks.append(tdic);

	#find this action [add del modify search other]
	#|--|open|close|clock|no|ring|--|#
	def _find_action(self,struct):
		tag = 0;
		for ck in struct['clocks']:
			if ck['type'] == 'add':
				struct['ck_action'] = 'add';
				break;
			elif ck['type'] == 'set':
				for key in struct.keys():
					if key.find('ck_') <> -1:
						struct['ck_action'] = 'modify';
						break;
				if not struct.has_key('ck_action'): struct['ck_action'] = 'add';
				break;
			elif ck['type'] == 'del':
				struct['ck_action'] = 'del';
				break;
			elif ck['type'] == 'search':
				struct['ck_action'] = 'search';
				break;
			elif ck['type'] == 'off':
				struct['ck_action'] = 'off';
				break;
			elif ck['type'] == 'open':
				struct['ck_action'] = 'open';
				break;
			elif ck['type'] == 'no':
				tag = tag | (1 << 2);
			elif ck['type'] == 'ring':
				tag = tag | (1 << 1);
			elif ck['type'] == 'clock':
				tag = tag | (1 << 3);
			elif ck['type'] == 'off':
				tag = tag | (1 << 4);
		if tag & 6 > 0: struct['ck_action'] = 'off';
		elif tag & 32 > 0: struct['ck_action'] = 'open';
		elif tag & 10 > 0: struct['ck_action'] = 'open';

	def _find_time(self,struct):
		clocks = struct['clocks'];
		tdic = dict();
		for ck in clocks:
			if ck['type'] == 'time_ut' or ck['type'] == 'time_ntut':
				tstr = scope = '';
				times = ck['interval'][0];
				for tm in ck['times']:
					tstr = tstr + tm['value'];
					if tm['scope'] == 'day':
						scope = str(times[2]);
				tdic['scope'] = scope;
				tdic['time'] = str(times[3]) + ':' + str(times[4]);
				struct['ck_time'] = tdic;
				clocks.remove(ck);
				break;

	def _analysis_date(self,struct):
		clocks = struct['clocks'];
		adjust = 000;
		tdic = dict();
		for ck in clocks:
			if ck['type'] == 'set' or ck['type'] == 'modify':
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
		if delay == 3: struct['ck_delay'] = tdic['type'];

	def _analysis_able(self,struct):
		able = ept = 0;
		clocks = struct['clocks'];
		for ck in clocks:
			if ck['type'] == 'able':
				if ck['style'] == 'workday':
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
		if struct.has_key('ck_time'):
			scope = struct['ck_time']['scope'];
			if scope <> '':
				curtime = time.localtime();
				curday = curtime[2];
				left = int(scope) - curday;
				if left < 0: return ;
				curweek = curtime[6];
				lfweek = curweek + left;
				able = math.pow(2,lfweek);

		if ept == 1: able = math.pow(2,7) - 1 - able;
		if able > 0: struct['ck_able'] = able;

	def _analysis_bell(self,struct):
		clocks = struct['clocks'];
		tdic = dict();
		for ck in clocks:
			if ck['type'].find('music') <> -1:
				tdic[ck['scope']] = ck['value'];
				struct['ck_bell'] = tdic;
