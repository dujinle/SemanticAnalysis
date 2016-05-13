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
import common,config
from common import MyException

class Calc_Time_Notion:

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
			self._calc_interval(struct);
		except MyException as e: raise e;

	def _calc_interval(self,struct):
		taglist = struct.get('taglist');
		struct['intervals'] = list();
		start_time = list(self.curtime[:]);
		end_time = list(self.curtime[:]);

		flag = False;
		for tag in taglist:
			if type(tag) <> dict and flag == True:
				interval = [time.mktime(start_time),time.mktime(end_time)];
				struct['intervals'].append(interval);
				flag = False;
			elif tag['type'] == 'time':
				self._calc_start_end_time(start_time,end_time,tag);
				flag = True;
			elif tag['type'] == 'num_time':
				self._fill_time(start_time,end_time,tag);
				flag = True;
			elif flag == True:
				interval = [time.mktime(start_time),time.mktime(end_time)];
				struct['intervals'].append(interval);
				flag = False;
			self._make_sure_time(start_time);
			self._make_sure_time(end_time);
		if flag == True:
			interval = [time.mktime(start_time),time.mktime(end_time)];
			struct['intervals'].append(interval);

	def _fill_time(self,start_time,end_time,tag):
		idx = self.ttype[tag['mytype']];
		start_time[idx] = int(tag['num']);
		end_time[idx] = int(tag['num']);
		if tag.has_key('interval'):
			start_time[idx] = int(tag['num']) + tag['interval'][0];
			end_time[idx] = int(tag['num']) + tag['interval'][1];

	def _calc_start_end_time(self,start_time,end_time,tag):
		interval = tag.get('interval');
		idx = self.ttype[tag['scope']];
		start_time[idx] = start_time[idx] + interval[0];
		end_time[idx] = end_time[idx] + interval[1];
		start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
		end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);

	def _make_sure_time(self,mytime):
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
