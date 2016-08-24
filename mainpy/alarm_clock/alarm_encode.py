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
			if struct.has_key('music'):
				for music in struct['music']:
					if type(music) == dict: clocks.append(music);
				del struct['music'];
			if struct.has_key('mood'):
				for mood in struct['mood']:
					if type(mood) == dict: clocks.append(mood);
				del struct['mood'];

			for st in inlist:
				for key in self.data.keys():
					self._match_item(st,clocks,key);
			self._analysis_date(struct);
			self._analysis_delay(struct);
			self._find_time(struct);
			self._analysis_able(struct);
			self._analysis_bell(struct);
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

	def _find_time(self,struct):
		if struct.has_key('intervals') and len(struct['intervals']) > 0:
			for myinterval in struct['intervals']:
				times = myinterval['start'];
				if myinterval['scope'] == 'day' or myinterval['scope'] == 'month' \
					or myinterval['scope'] == 'year':
					tdic = dict();
					tdic['date'] = str(times[0]) + '/' + str(times[1]) + '/' + str(times[2]);
					tdic['type'] = myinterval['type'];
					struct['ck_date'] = tdic;
				if times[3] <> 0:
					tdic = dict();
					tdic['time'] = str(times[3]) + ':' + str(times[4]);
					tdic['str'] = myinterval['str'];
					struct['ck_time'] = tdic;
			del struct['intervals'];

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
		able = ept = rate = 0;
		clocks = struct['clocks'];
		tdic = dict();
		for ck in clocks:
			if ck['type'] == 'able':
				if ck['style'] == 'workday':
					able = math.pow(2,5) - 1;
				elif ck['style'] == 'allin':
					able = math.pow(2,8) - 1;
				elif ck['style'] == 'workend':
					able = math.pow(2,7) - math.pow(2,5);
			if ck['type'] == 'mood_tm':
				if ck['mstr'] == u'每': rate = 1;
			if ck['type'] == 'except': ept = 1;
		if struct.has_key('ck_date'):
			date = struct['ck_date'];
			if date['type'] == 'time_ut' or date['type'] == 'time_nt':
				tdic['repeat'] = 'once';
				tdic['date'] = date['date'];
				tdic['type'] = 'date';
			if date['type'] == 'time_wt' and rate == 0:
				tdic['repeat'] = 'once';
				tdic['date'] = date['date'];
				tdic['type'] = 'date';
			if date['type'] == 'time_wt' and rate == 1:
				dates = date['date'].split('/');
				dat = datetime.date(int(dates[0]),int(dates[1]),int(dates[2]));
				week = dat.weekday();
				able = math.pow(2,week);
				tdic['type'] = 'week';
				tdic['repeat'] = 'repeat';
				tdic['able'] = able;
			del struct['ck_date'];
		elif able > 0:
			tdic['type'] = 'week';
			tdic['able'] = able;
			tdic['repeat'] = 'repeat';
		if ept == 1 and tdic.has_key('type') and tdic['type'] == 'week':
			able = math.pow(2,7) - 1 - able;
			tdic['able'] = able;
		if tdic.has_key('type'): struct['ck_able'] = tdic;

	def _analysis_bell(self,struct):
		clocks = struct['clocks'];
		tdic = dict();
		flag = False;
		for ck in clocks:
			if ck['type'].find('music') <> -1:
				if ck['scope'] == 'singname': flag = True;
				tdic[ck['scope']] = ck['value'];
		if flag == True: struct['ck_bell'] = tdic;
