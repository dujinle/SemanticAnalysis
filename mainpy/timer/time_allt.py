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
#可能会有各种组合这里处理 UT + NT 或者 UT + QT NT + UT  WT + NT/UT
class ALLT(Base):

	def encode(self,struct):
		try:
			self._find_all(struct);
			self._find_t2t(struct);
		except MyException as e: raise e;

	def _find_match(self,reg,rename,cname,struct):
		if not struct.has_key('taglist'): return None;
		text = struct['text'];
		taglist = struct['taglist'];
		comp = re.compile(reg);
		match = comp.search(text);
		#check all the match status#
		while True:
			if match is None: break;
			mat = match.group(0);
			idx = time_common._find_idx(text,mat,'null');
			mytag = taglist[idx];
			ntag = taglist[idx + 1];
			mytag['type'] = cname;
			mytag['ntimes'] = mytag['ntimes'] + ntag['ntimes'];
			mytag['times'].extend(ntag['times']);
			mytag['attr'] = ['date'];
			del taglist[idx + 1];
			text = text.replace(mat,rename,1);
			struct['text'] = struct['text'].replace(mat,rename,1);
			comp = re.compile(reg);
			match = comp.search(text);

	def _find_all(self,struct):
		#find ut_nt format#
		self._find_match('(UT){1,}NT','UNT','time_utnt',struct);
		#find ut_qt format#
		self._find_match('(UT){1,}QT','UQT','time_utqt',struct);
		#find nt_ut format#
		self._find_match('NT(UT){1,}','NUT','time_ntut',struct);
		#find wt_nt format#
		self._find_match('WTE*(NT){1,}','WNT','time_wtnt',struct);
		#find wt_nut format#
		self._find_match('WTE*(NUT){1,}','WNUT','time_wtnut',struct);

	#是否是 time xxxx time and t1.scope > t2.scope
	def _find_t2t(self,struct):
		if not struct.has_key('taglist'): return None;
		text = struct['text'];
		taglist = struct['taglist'];
		#check all the match status#
		tidx = 1;
		while True:
			if tidx >= len(taglist): break;
			prev_tag = taglist[tidx - 1];
			tag = taglist[tidx];
			if tag['type'].find('time_dt') <> -1:
				tidx = tidx + 1;
				continue;
			prev_scope = curr_scope = -1;
			for t in prev_tag['times']:
				if t.has_key('scope'): prev_scope = t['scope'];
			for t in tag['times']:
				if t.has_key('scope'): curr_scope = t['scope'];
			pscope_id = time_common.tmenu[prev_scope];
			cscope_id = time_common.tmenu[curr_scope];
			if pscope_id < cscope_id:
				prev_tag['type'] = 'time_t2t';
				prev_tag['ntimes'] = prev_tag['ntimes'] + tag['ntimes'];
				prev_tag['times'].extend(tag['times']);
				prev_tag['attr'] = ['date'];
				del taglist[tidx];
			else:
				tidx = tidx + 1;

#计算各种组合时间
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
				elif tag['type'] == 'time_wtnt':
					self._calc_wtnt_date_times(curtime,tag);
				elif tag['type'] == 'time_wtnut':
					self._calc_wtnut_date_times(curtime,tag);
				elif tag['type'] == 'time_t2t':
					self._calc_t2t_date_times(curtime,tag);
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
				elif tm['value'] == u'下午' or tm['value'] == u'晚上' or tm['value'] == u'深夜': hour = 2;
			else: hour = 0;

			if tm['type'] == 'time_nt':
				if not tm.has_key('interval'): break;
				if tm['func'] == 'add':
					start_time[idx] = start_time[idx] + tm['interval'][0];
					end_time[idx] = end_time[idx] + tm['interval'][0];
				elif tm['func'] == 'equal':
					start_time[idx] = tm['interval'][0];
					end_time[idx] = tm['interval'][0];
			elif tm['type'] == 'time_ut':
				if hour == 2 and tm['scope'] == 'hour':
					if tm['num'] < 12:
						start_time[idx] = int(tm['num']) + 12;
						end_time[idx] = int(tm['num']) + 12;
					else:
						start_time[idx] = int(tm['num']);
						end_time[idx] = int(tm['num']);
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
			if tm['num'] < 12:
				start_time[idx] = int(tm['num']) + 12;
				end_time[idx] = int(tm['num']) + 13;
			else:
				start_time[idx] = int(tm['num']);
				end_time[idx] = int(tm['num']) + 1;
		else:
			start_time[idx] = int(tm['num']);
			end_time[idx]  = int(tm['num']) + 1;
		time_common._make_sure_time(start_time,idx);
		time_common._make_sure_time(end_time,idx);
		tag['interval'] = [start_time,end_time];

	#计算 周3上午#
	def _calc_wtnt_date_times(self,curtime,tag):
		times = tag['times'];
		start_time = list(curtime);
		end_time = list(curtime);
		tidx = 0;
		while True:
			if tidx >= len(times) - 1: break;
			tm = times[tidx];
			if tm['type'] == 'time_wte':
				tidx = tidx + 1;
				continue;
			idx = time_common.tmenu[tm['scope']];
			start_time[idx] = tm['interval'][0] + start_time[idx];
			end_time[idx] = tm['interval'][0] + end_time[idx];

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

	#计算周3上午7点#
	def _calc_wtnut_date_times(self,curtime,tag):
		times = tag['times'];
		start_time = list(curtime);
		end_time = list(curtime);
		tidx = hour = 0;
		while True:
			if tidx >= len(times) - 1: break;
			tm = times[tidx];
			if tm['type'] == 'time_wte':
				tidx = tidx + 1;
				continue;
			idx = time_common.tmenu[tm['scope']];
			if tm['scope'] == 'hour':
				if tm['value'] == u'上午': hour = 1;
				elif tm['value'] == u'下午' or tm['value'] == u'晚上' or tm['value'] == u'深夜': hour = 2;
			else: hour = 0;

			if tm['type'] == 'time_nt' or tm['type'] == 'time_wt':
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

	#计算多个时间区间下降组合#
	def _calc_t2t_date_times(self,curtime,tag):
		times = tag['times'];
		start_time = list(curtime);
		end_time = list(curtime);
		tidx = hour = 0;
		while True:
			if tidx >= len(times) - 1: break;
			tm = times[tidx];
			if tm['type'] == 'time_wte' or tm['type'] == 'time_dt' or tm['type'] == 'time_dte':
				tidx = tidx + 1;
				continue;
			idx = time_common.tmenu[tm['scope']];
			if tm['scope'] == 'hour':
				if tm['value'] == u'上午': hour = 1;
				elif tm['value'] == u'下午' or tm['value'] == u'晚上' or tm['value'] == u'深夜': hour = 2;
			else: hour = 0;

			if tm['type'] == 'time_nt' or tm['type'] == 'time_wt':
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
		if tm['type'] == 'time_ut':
			if hour == 2 and tm['scope'] == 'hour':
				start_time[idx] = int(tm['num']) + 12;
				end_time[idx] = int(tm['num']) + 13;
			else:
				start_time[idx] = int(tm['num']);
				end_time[idx]  = int(tm['num']) + 1;
		elif tm['type'] == 'time_qt':
			start_time[idx] = tm['interval'][0];
			end_time[idx] = tm['interval'][1];
		time_common._make_sure_time(start_time,idx);
		time_common._make_sure_time(end_time,idx);
		tag['interval'] = [start_time,end_time];
