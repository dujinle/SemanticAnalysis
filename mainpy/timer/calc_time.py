#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,time
reload(sys)
sys.setdefaultencoding('utf-8')
#=================================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#=================================================
from base import Base
import common,config
from common import MyException

class CalcTimeInterval(Base):

	def __init__(self):
		self.data = None;
		self.curtime = None;
		self.month = [31,31,28,31,30,31,30,31,31,30,31,30,31];
		self.leap_mon = [31,31,29,31,30,31,30,31,31,30,31,30,31];
		self.ttype = {
			'sec':config.tm_sec,
			'min':config.tm_min,
			'hour':config.tm_hour,
			'day':config.tm_day,
			'month':config.tm_mon,
			'year':config.tm_year
		};
		pass;

	def encode(self,struct):
		try:
			self.curtime = time.localtime();
			self._deal_num_time(struct);
			self._deal_ex_time(struct);
			self._deal_composite(struct);
			self._deal_week_time(struct);
			self._merge_num_ex_com_times(struct);
			self._deal_interval(struct);
		except MyException as e: raise e;

	def _deal_num_time(self,struct):
		taglist = struct['taglist'];
		tagdic = dict();
		tagdic['type'] = 'num_time';
		tagdic['attr'] = ['date','num'];
		tagdic['times'] = list();
		first_tag = None;
		idx_step = 0;
		while True:
			if idx_step >= len(taglist): break;
			tag = taglist[idx_step];
			if type(tag) == dict and tag['type'] == 'num_time' and first_tag is None:
				tdic = dict(tag);
				tagdic['times'].append(tdic);
				first_tag = tag;
			elif type(tag) == dict and tag['type'] == 'num_time':
				tdic = dict(tag);
				tagdic['times'].append(tdic);
				taglist.remove(tag);
				idx_step = idx_step - 1;
			elif not first_tag is None:
				if len(tagdic['times']) > 1:
					tagdic['attr'] = ['date'];
				if first_tag is not None:
					idx = taglist.index(first_tag);
					taglist[idx] = dict(tagdic);
				tagdic['times'] = list();
				tagdic['attr'] = ['date','num'];
				first_tag = None;
			idx_step = idx_step + 1;
		if not first_tag is None:
			if len(tagdic['times']) > 1:
				tagdic['attr'] = ['date'];
			idx = taglist.index(first_tag);
			taglist[idx] = dict(tagdic);
			first_tag = None;

	def _deal_ex_time(self,struct):
		taglist = struct['taglist'];
		tagdic = dict();
		tagdic['type'] = 'ex_time';
		tagdic['attr'] = ['date'];
		tagdic['times'] = list();
		first_tag = None;
		idx_step = 0;
		while True:
			if idx_step >= len(taglist): break;
			tag = taglist[idx_step];
			if type(tag) == dict and tag['type'] == 'ex_time' and first_tag is None:
				tdic = dict(tag);
				tagdic['times'].append(tdic);
				first_tag = tag;
			elif type(tag) == dict and tag['type'] == 'ex_time':
				tdic = dict(tag);
				tagdic['times'].append(tdic);
				taglist.remove(tag);
				idx_step = idx_step - 1;
			elif not first_tag is None:
				if len(tagdic['times']) > 1:
					tagdic['attr'] = ['date'];
				if first_tag is not None:
					idx = taglist.index(first_tag);
					taglist[idx] = dict(tagdic);
				tagdic['times'] = list();
				tagdic['attr'] = ['date'];
				first_tag = None;
			idx_step = idx_step + 1;
		if not first_tag is None:
			idx = taglist.index(first_tag);
			taglist[idx] = dict(tagdic);
			first_tag = None;

	def _deal_week_time(self,struct):
		taglist = struct['taglist'];
		tagdic = dict();
		tagdic['type'] = 'time_weeks';
		tagdic['attr'] = ['date'];
		tagdic['times'] = list();
		first_tag = None;
		idx_step = 0;
		while True:
			if idx_step >= len(taglist): break;
			tag = taglist[idx_step];
			if type(tag) == dict and tag['type'].find('time_week') <> -1 and first_tag is None:
				tdic = dict(tag);
				tagdic['times'].append(tdic);
				first_tag = tag;
			elif type(tag) == dict and tag['type'].find('timw_week') <> -1:
				tdic = dict(tag);
				tagdic['times'].append(tdic);
				taglist.remove(tag);
				idx_step = idx_step - 1;
			elif not first_tag is None:
				if len(tagdic['times']) > 1:
					tagdic['attr'] = ['date'];
				if first_tag is not None:
					idx = taglist.index(first_tag);
					taglist[idx] = dict(tagdic);
				tagdic['times'] = list();
				tagdic['attr'] = ['date'];
				first_tag = None;
			idx_step = idx_step + 1;
		if not first_tag is None:
			idx = taglist.index(first_tag);
			taglist[idx] = dict(tagdic);
			first_tag = None;

	def _deal_composite(self,struct):
		taglist = struct['taglist'];
		idx_step = 0;
		while True:
			if idx_step >= len(taglist): break;
			tag = taglist[idx_step];
			if type(tag) <> dict:
				idx_step = idx_step + 1;
			elif tag['type'] == 'time_composite':
				if tag['kpoint'] == 'last':
					times = taglist[idx_step - 1];
					times['times'].append(tag);
				elif tag['kpoint'] == 'first':
					times = taglist[idx_step + 1];
					times['times'].insert(0,tag);
				taglist.remove(tag);
				idx_step = idx_step - 1;
				self._calc_com_time(times,tag);
			idx_step = idx_step + 1;

	def _calc_com_time(self,tag,com):
		times = tag['times'];
		ttidx = times.index(com);
		mytime = None;
		if com['kpoint'] == 'first':
			mytime = times[ttidx + 1];
			mytime['value'] = com['value'] + mytime['value'];
		elif com['kpoint'] == 'last':
			mytime = times[ttidx - 1];
			mytime['value'] = mytime['value'] + com['value'];
		myinterval = None;
		if mytime.has_key('interval'): myinterval = mytime['interval'];

		mytime['interval'] = dict();
		times.remove(com);
		for tp in tag['attr']:
			if tp == 'num':
				if mytime['type'] == 'num_time':
					if com['dir'] == '-':
						mytime['interval']['num'] = ['<',-1 * mytime['num']];
					elif com['dir'] == '+':
						mytime['interval']['num'] = [mytime['num'],'>'];
			elif tp == 'date':
				if mytime['type'] == 'num_time':
					if com['dir'] == '-':
						mytime['interval']['num'] = ['<',0];
					elif com['dir'] == '+':
						mytime['interval']['num'] = [0,'>'];
				elif mytime['type'] == 'ex_time':
					if com['dir'] == '-':
						mytime['interval']['date'] = ['<',myinterval[0]];
					elif com['dir'] == '+':
						mytime['interval']['date'] = [myinterval[1],'>'];

	def _merge_num_ex_com_times(self,struct):
		taglist = struct['taglist'];
		first_tag = None;
		idx_step = 0;
		while True:
			if idx_step >= len(taglist): break;
			tag = taglist[idx_step];
			if type(tag) == dict and tag['type'].find('time') <> -1 and first_tag is None:
				first_tag = tag;
			elif type(tag) == dict and tag['type'].find('time') <> -1:
				if len(first_tag['attr']) > 1: first_tag['attr'].remove('num');
				first_tag['times'].extend(tag['times']);
				taglist.remove(tag);
				idx_step = idx_step - 1;
			elif not first_tag is None:
				first_tag = None;
			idx_step = idx_step + 1;

		check_list = [-1,-1,-1,-1,-1,-1];
		idx_step = 0;
		while True:
			if idx_step >= len(taglist): break;
			tag = taglist[idx_step];
			if type(tag) == dict and tag['type'].find('time') <> -1:
				times = tag['times'];
				for tt in times:
					if tt['type'] == 'time_composite':
						continue;
					flag = check_list[self.ttype[tt['scope']]];
					idx = times.index(tt);
					if flag == -1:
						check_list[self.ttype[tt['scope']]] = idx;
					else:
						raise MyException('which %s or %s' %(tt['value'],times[flag]['value']));
			else:
				check_list = [-1,-1,-1,-1,-1,-1];
			idx_step = idx_step + 1;

	def _deal_interval(self,struct):
		taglist = struct.get('taglist');
		if len(taglist) <= 0: return None;

		idx_step = 0;
		while True:
			if idx_step >= len(taglist): break;
			tag = taglist[idx_step];
			if type(tag) == dict and tag['type'].find('time') <> -1:
				tag['interval'] = dict();
				self._calc_interval(tag);
			idx_step = idx_step + 1;

	def _calc_interval(self,tag):
		start_time = list(self.curtime[:]);
		end_time = list(self.curtime[:]);
		times = tag['times'];
		lens = len(times);
		for attr in tag['attr']:
			tag['interval'][attr] = [start_time,end_time];
			tidx = 1;
			while True:
				if tidx - 1>= lens: break;
				tt = times[tidx - 1];
				if tidx < lens:
					if tt['type'] == 'num_time':
						self._fill_num_time(tt,tag['interval'][attr],attr);
					elif tt['type'] == 'ex_time' or tt['type'].find('time_week') <> -1:
						self._fill_ex_time(tt,tag['interval'][attr],attr);
				elif tidx >= lens:
					if tt['type'] == 'num_time':
						self._calc_num_time(tt,tag['interval'][attr],attr);
					elif tt['type'] == 'ex_time' or tt['type'].find('time_week') <> -1:
						self._calc_ex_time(tt,tag['interval'][attr],attr);
				tidx = tidx + 1;
				self._make_sure_time(tag['interval'][attr][0]);
				self._make_sure_time(tag['interval'][attr][1]);

	def _calc_num_time(self,mtime,interval,attr):
		idx = self.ttype[mtime['scope']];
		start_time = interval[0];
		end_time = interval[1];

		start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
		end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);

		if attr == 'num':
			if mtime.has_key('interval'):
				minterval = mtime['interval'];
				if type(minterval) == dict and minterval.has_key(attr): minterval = minterval[attr];
				if minterval[0] == '<':
					start_time[-1] = 'null';
					end_time[idx] = end_time[idx] + minterval[1];
				elif minterval[1] == '>':
					start_time[idx] = start_time[idx] + minterval[0];
					end_time[-1] = 'null';
				else:
					start_time[idx] = start_time[idx] + minterval[0];
					end_time[idx] = end_time[idx] + minterval[1];
			else:
				start_time[0] = 'null';
				end_time[0] = 'null';
		elif attr == 'date':
			if mtime.has_key('interval'):
				minterval = mtime['interval'];
				if minterval.has_key(attr): minterval = minterval[attr];
				if minterval[0] == '<':
					start_time[-1] = 'null';
					end_time[idx] = int(mtime['num']);
				elif minterval[1] == '>':
					end_time[-1] = 'null';
					start_time[idx] = int(mtime['num']);
				else:
					end_time[idx] = int(mtime['num']);
					start_time[idx] = int(mtime['num']) + 1;

	def _calc_ex_time(self,mtime,interval,attr):
		print mtime;
		idx = self.ttype[mtime['scope']];
		start_time = interval[0];
		end_time = interval[1];
		start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
		end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);
		if attr == 'num':
			start_time[0] = 'null';
			end_time[0] = 'null';
		elif attr == 'date':
			if mtime.has_key('interval'):
				minterval = mtime['interval'];
				if type(minterval) == dict and minterval.has_key(attr): minterval = minterval[attr];
				if minterval[0] == '<':
					start_time[-1] = 'null';
					if mtime['func'] == 'add':
						end_time[idx] = end_time[idx] + minterval[1];
					elif mtime['func'] == 'equal':
						end_time[idx] = minterval[1];
				elif minterval[1] == '>':
					end_time[-1] = 'null';
					if mtime['func'] == 'add':
						start_time[idx] = start_time[idx] + minterval[0];
					elif mtime['func'] == 'equal':
						start_time[idx] = minterval[0];
				else:
					if mtime['func'] == 'add':
						start_time[idx] = start_time[idx] + int(mtime['interval'][0]);
						end_time[idx] = end_time[idx] + int(mtime['interval'][1]);
					elif mtime['func'] == 'equal':
						start_time[idx] = int(mtime['interval'][0]);
						end_time[idx] = int(mtime['interval'][1]);

	def _fill_num_time(self,mtime,interval,attr):
		idx = self.ttype[mtime['scope']];
		start_time = interval[0];
		end_time = interval[1];
		if attr == 'num':
			if mtime.has_key('interval'):
				minterval = mtime['interval'];
				if type(minterval) == dict and minterval.has_key(attr): minterval = minterval[attr];
				if minterval[0] == '<':
					start_time[-1] = 'null';
					end_time[idx] = end_time[idx] + minterval[1];
				elif minterval[1] == '>':
					start_time[idx] = start_time[idx] + minterval[0];
					end_time[-1] = 'null';
				else:
					start_time[idx] = start_time[idx] + minterval[0];
					end_time[idx] = end_time[idx] + minterval[1];
			else:
				start_time[0] = 'null';
				end_time[0] = 'null';
		else:
			end_time[idx] = int(mtime['num']);
			start_time[idx] = int(mtime['num']);

	def _fill_ex_time(self,mtime,interval,attr):
		idx = self.ttype[mtime['scope']];
		start_time = interval[0];
		end_time = interval[1];
		if attr == 'num':
			start_time[0] = 'null';
			end_time[0] = 'null';
		elif attr == 'date':
			if attr.has_key('interval'):
				minterval = mtime['interval'];
				if type(minterval) == dict and minterval.has_key(attr): minterval = minterval[attr];
				if minterval[0] == '<':
					start_time[-1] = 'null';
					end_time[idx] = end_time[idx] + minterval[0];
				elif minterval[1] == '>':
					end_time[-1] = 'null';
					start_time[idx] = start_time[idx] + minterval[1];
				else:
					if mtime['func'] == 'add':
						start_time[idx] = start_time[idx] + int(mtime['interval'][0]);
						end_time[idx] = end_time[idx] + int(mtime['interval'][0]);
					elif mtime['func'] == 'equal':
						start_time[idx] = int(mtime['interval'][0]);
						end_time[idx] = int(mtime['interval'][0]);

	def _calc_start_end_time(self,start_time,end_time,tag):
		idx = self.ttype[tag['scope']];
		if tag['type'] == 'num_time':
			if tag['meaning'] == 'date':
				if not tag.has_key('interval'):
					start_time[idx] = int(tag['num']);
					end_time[idx] = int(tag['num']) + 1;
				else:
					interval = tag['interval'];
					start_time[idx] = int(tag['num']);
					end_time[idx] = int(tag['num'])
					if interval[0] == '<<':
						start_time.insert(0,'null');
						end_time[idx] = end_time[idx] + interval[1];
					if interval[1] == '>>':
						start_time[idx] = start_time[idx] + interval[0];
						end_time.insert(0,'null');
			elif tag['meaning'] == 'number':
				if not tag.has_key('interval'):
					start_time[idx] = start_time[idx] + int(tag['num']);
					end_time[idx] = end_time[idx] + int(tag['num']);
				else:
					interval = tag['interval'];
					if interval[0] == '<<':
						start_time.insert(0,'null');
						end_time[idx] = end_time[idx] + interval[1];
					elif interval[1] == '>>':
						start_time[idx] = start_time[idx] + interval[0];
						end_time.insert(0,'null');
		if start_time[0] <> 'null':
			start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
		if end_time[0] <> 'null':
			end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);

	def _make_sure_time(self,mytime):
		if mytime[0] == 'null': return False;
		if mytime[config.tm_sec] > 60:
			mytime[config.tm_sec] = mytime[config.tm_sec] - 60;
			mytime[config.tm_min] = mytime[config.tm_min] + 1;
			return True;
		elif mytime[config.tm_sec] < 0:
			mytime[config.tm_sec] = mytime[config.tm_sec] + 60;
			mytime[config.tm_min] = mytime[config.tm_min] - 1;
			return True;

		if mytime[config.tm_min] > 60:
			mytime[config.tm_min] = mytime[config.tm_min] - 60;
			mytime[config.tm_hour] = mytime[config.tm_hour] + 1;
			return True;
		elif mytime[config.tm_min] < 0:
			mytime[config.tm_min] = mytime[config.tm_min] + 60;
			mytime[config.tm_hour] = mytime[config.tm_hour] - 1;
			return True;

		if mytime[config.tm_hour] > 24:
			mytime[config.tm_hour] = mytime[config.tm_hour] - 24;
			mytime[config.tm_day] = mytime[config.tm_day] + 1;
			return True;
		elif mytime[config.tm_hour] < 0:
			mytime[config.tm_hour] = mytime[config.tm_hour] + 24;
			mytime[config.tm_day] = mytime[config.tm_day] - 1;
			return True;

		if self._is_leap_year(mytime[config.tm_year]):
			if mytime[config.tm_day] > self.leap_mon[mytime[config.tm_mon]]:
				mytime[config.tm_day] = mytime[config.tm_day] - self.leap_mon[mytime[config.tm_mon]];
				mytime[config.tm_mon] = mytime[config.tm_mon] + 1;
				return True;
			elif mytime[config.tm_day] <= 0:
				mytime[config.tm_day] = mytime[config.tm_day] + self.leap_mon[mytime[config.tm_mon] - 1];
				mytime[config.tm_mon] = mytime[config.tm_mon] - 1;
				return True;
		else:
			if mytime[config.tm_day] > self.month[mytime[config.tm_mon]]:
				mytime[config.tm_day] = mytime[config.tm_day] - self.month[mytime[config.tm_mon]];
				mytime[config.tm_mon] = mytime[config.tm_mon] + 1;
				return True;
			elif mytime[config.tm_day] <= 0:
				mytime[config.tm_day] = mytime[config.tm_day] + self.month[mytime[config.tm_mon] - 1];
				mytime[config.tm_mon] = mytime[config.tm_mon] - 1;
				return True;

		if mytime[config.tm_mon] > 12:
			mytime[config.tm_mon] = mytime[config.tm_mon] - 12;
			mytime[config.tm_year] = mytime[config.tm_year] + 1;
			return True;
		elif mytime[config.tm_mon] <= 0:
			mytime[config.tm_mon] = mytime[config.tm_mon] + 12;
			mytime[config.tm_year] = mytime[config.tm_year] - 1;
			return True;
		return False;

	def _is_leap_year(self,myyear):
		if myyear % 400 == 0 or (myyear % 4 == 0 and myyear % 100 <> 0):
			return True;
		return False;
