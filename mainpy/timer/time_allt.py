#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json
import re,time
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import common
import time_common
from myexception import MyException
from base import Base
#可能会有各种组合这里处理 UT + NT 或者 UT + QT NT + UT
class ALLT(Base):

	def encode(self,struct):
		try:
			self._find_utnt(struct);
			self._find_utqt(struct);
			self._find_ntut(struct);
		except MyException as e: raise e;

	def _find_utnt(self,struct):
		if not struct.has_key('taglist'): return None;
		text = struct['text'];
		taglist = struct['taglist'];
		comp = re.compile('(UT){1,}NT');
		match = comp.search(text);
		#check all the match status#
		while True:
			if match is None: break;
			mat = match.group(0);
			idx = time_common._find_idx(text,mat,'null');
			mytag = taglist[idx];
			ntag = taglist[idx + 1];
			mytag['type'] = 'time_utnt';
			mytag['ntimes'] = mytag['ntimes'] + ntag['ntimes'];
			mytag['times'].extend(ntag['times']);
			mytag['attr'] = ['date'];
			del taglist[idx + 1];
			text = text.replace(mat,'UNT',1);
			struct['text'] = struct['text'].replace(mat,'UNT',1);
			comp = re.compile('(UT){1,}NT');
			match = comp.search(text);

	def _find_utqt(self,struct):
		if not struct.has_key('taglist'): return None;
		text = struct['text'];
		taglist = struct['taglist'];
		comp = re.compile('(UT){1,}QT');
		match = comp.search(text);
		#check all the match status#
		while True:
			if match is None: break;
			mat = match.group(0);
			idx = time_common._find_idx(text,mat,'null');
			mytag = taglist[idx];
			ntag = taglist[idx + 1];
			mytag['type'] = 'time_utqt';
			mytag['ntimes'] = mytag['ntimes'] + ntag['ntimes'];
			mytag['times'].extend(ntag['times']);
			mytag['attr'] = ['date'];
			del taglist[idx + 1];
			text = text.replace(mat,'UQT',1);
			struct['text'] = struct['text'].replace(mat,'UQT',1);
			comp = re.compile('(UT){1,}QT');
			match = comp.search(text);

	def _find_ntut(self,struct):
		if not struct.has_key('taglist'): return None;
		text = struct['text'];
		taglist = struct['taglist'];
		comp = re.compile('NTUT{1,}');
		match = comp.search(text);
		#check all the match status#
		while True:
			if match is None: break;
			mat = match.group(0);
			idx = time_common._find_idx(text,mat,'null');
			mytag = taglist[idx];
			ntag = taglist[idx + 1];
			mytag['type'] = 'time_ntut';
			mytag['ntimes'] = mytag['ntimes'] + ntag['ntimes'];
			mytag['times'].extend(ntag['times']);
			mytag['attr'] = ['date'];
			del taglist[idx + 1];
			text = text.replace(mat,'NUT',1);
			struct['text'] = struct['text'].replace(mat,'NUT',1);
			comp = re.compile('NTUT{1,}');
			match = comp.search(text);

#计算UT模式下的时间区间包括UTE模式
class CALLT(Base):
	def encode(self,struct):
		try:
			if not struct.has_key('taglist'): return None;
			curtime = time.localtime();
			taglist = struct['taglist'];
			for tag in taglist:
				if tag['type'] == 'time_utnt':
					self._calc_utnt_date_times(curtime,tag);
				elif tag['type'] == 'time_utqt':
					self._calc_utqt_date_times(curtime,tag);
				elif tag['type'] == 'time_ntut':
					self._calc_ntut_date_times(curtime,tag);
		except MyException as e: raise e;

	#计算2014年4月7号下午#
	def _calc_utnt_date_times(self,curtime,tag):
		times = tag['times'];
		start_time = list(curtime);
		end_time = list(curtime);
		tidx = 0;
		while True:
			if tidx >= len(times) - 1: break;
			tm = times[tidx];
			idx = time_common.tmenu[tm['scope']];
			start_time[idx] = int(tm['num']);
			end_time[idx] = int(tm['num']);

			start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
			end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);
			tidx = tidx + 1;
		tm = times[tidx];
		idx = time_common.tmenu[tm['scope']];
		start_time[idx] = tm['interval'][0];
		end_time[idx]  = tm['interval'][1];
		time_common._make_sure_time(start_time,idx);
		time_common._make_sure_time(end_time,idx);
		tag['interval'] = [start_time,end_time];

	#计算5时3刻 5月上旬#
	def _calc_utqt_date_times(self,curtime,tag):
		times = tag['times'];
		start_time = list(curtime);
		end_time = list(curtime);
		tidx = 0;
		if tag['ntimes'] > 2: return None;
		while True:
			if tidx >= len(times) - 1: break;
			tm = times[tidx];
			idx = time_common.tmenu[tm['scope']];
			start_time[idx] = int(tm['num']);
			end_time[idx] = int(tm['num']);

			start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
			end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);
			tidx = tidx + 1;
		tm = times[tidx];
		if tm['type'] == 'time_qt':
			if tm['scope'] == 'qt':
				num = int(tm['num']);
				tm['scope'] = 'min';
				idx = time_common.tmenu[tm['scope']];
				start_time[idx] = num * 15;
				end_time[idx]  = num * 15 + 1;
				time_common._make_sure_time(start_time,idx);
				time_common._make_sure_time(end_time,idx);
				tag['interval'] = [start_time,end_time];
			elif tm.has_key('interval'):
				idx = time_common.tmenu[tm['scope']];
				start_time[idx] = tm['interval'][0];
				end_time[idx] = tm['interval'][1];
				time_common._make_sure_time(start_time,idx);
				time_common._make_sure_time(end_time,idx);
				tag['interval'] = [start_time,end_time];

	#计算后天17点#
	def _calc_ntut_date_times(self,curtime,tag):
		times = tag['times'];
		start_time = list(curtime);
		end_time = list(curtime);
		tidx = hour = 0;
		while True:
			if tidx >= len(times) - 1: break;
			tm = times[tidx];
			idx = time_common.tmenu[tm['scope']];
			if tm['scope'] == 'hour':
				if tm['value'] == u'上午': hour = 1;
				elif tm['value'] == u'下午': hour = 2;
			else: hour = 0;

			if tm['type'] == 'time_nt':
				if not tm.has_key('interval'): break;
				start_time[idx] = start_time[idx] + tm['interval'][0];
				end_time[idx] = end_time[idx] + tm['interval'][0];
			elif tm['type'] == 'time_ut':
				if hour == 2 and tm['scope'] == 'hour':
					start_time[idx] = int(tm['num']) + 12;
					end_time[idx] = int(tm['num']) + 12;
					hour = 0;
				else:
					start_time[idx] = int(tm['num']);
					end_time[idx] = int(tm['num']);

			start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
			end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);
			tidx = tidx + 1;
		tm = times[tidx];
		idx = time_common.tmenu[tm['scope']];
		if hour == 2 and tm['scope'] == 'hour':
			start_time[idx] = int(tm['num']) + 12;
			end_time[idx] = int(tm['num']) + 13;
		else:
			start_time[idx] = int(tm['num']);
			end_time[idx]  = int(tm['num']) + 1;
		time_common._make_sure_time(start_time,idx);
		time_common._make_sure_time(end_time,idx);
		tag['interval'] = [start_time,end_time];
