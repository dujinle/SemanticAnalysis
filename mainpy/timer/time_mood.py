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
import common
from common import MyException

tm_year = 0;
tm_mon = 1;
tm_day = 2;
tm_hour = 3;
tm_min = 4;
tm_sec = 5;

class TimeMood:

	def __init__(self):
		self.data = None;
		self.moth = [31,31,28,31,30,31,30,31,31,30,31,30,31];
		self.leap_mon = [31,31,29,31,30,31,30,31,31,30,31,30,31];
		pass;

	def init(self):
		self.mytime = time.localtime();
		print self.mytime;

	def load_data(self,tfile):

		try: self.data = common.read_json(tfile);
		except MyException as e: raise e;

	def encode(self,struct):
		try:
			self._mark_reg(struct);
			self._mark_range(struct);
		except MyException as e: raise e;

	def _mark_reg(self,struct):
		try:
			inlist = struct['inlist'];
			keys = self.data.keys();
			for key in keys:
				item = self.data[key];
				regs = item['regs'];
				for reg in regs:
					if reg['reg'] in inlist:
						tdic = dict();
						tdic['type'] = item['type'];
						tdic['unit'] = item['unit'];
						tdic.update(reg);
						struct['time_notion'] = tdic;
			common.print_dic(struct);
		except MyException as e:
			raise e;

	def _mark_range(self,struct):
		try:
			if not struct.has_key('time_notion'): return ;
			time_notion = struct['time_notion'];
			start_time = list();
			end_time = list();

			start_time.extend(self.mytime);
			end_time.extend(self.mytime);
			print start_time;
			ttype = time_notion['type'];
			ranges = time_notion['range'];
			if ttype == 'day':
				start_time[tm_day] = start_time[tm_day] + ranges[0];
				end_time[tm_day] = end_time[tm_day] + ranges[1];
			elif ttype == 'month':
				start_time[tm_mon] = start_time[tm_mon] + ranges[0];
				end_time[tm_mon] = end_time[tm_mon] + ranges[1];
			elif ttype == 'year':
				start_time[tm_year] = start_time[tm_year] + ranges[0];
				end_time[tm_year] = end_time[tm_year] + ranges[1];

			while True:
				if not self._make_sure_time(start_time): break;
			while True:
				if not self._make_sure_time(end_time): break;
			struct['time_notion']['start'] = start_time;
			struct['time_notion']['end'] = end_time;

		except MyException as e:
			raise e;

	def _make_sure_time(self,mytime):
		if mytime[tm_sec] > 60:
			mytime[tm_sec] = mytime[tm_sec] - 60;
			mytime[tm_min] = mytime[tm_min] + 1;
			return True;
		elif mytime[tm_sec] < 0:
			mytime[tm_sec] = mytime[tm_sec] + 60;
			mytime[tm_min] = mytime[tm_min] - 1;
			return True;

		if mytime[tm_min] > 60:
			mytime[tm_min] = mytime[tm_min] - 60;
			mytime[tm_hour] = mytime[tm_hour] + 1;
			return True;
		elif mytime[tm_min] < 0:
			mytime[tm_min] = mytime[tm_min] + 60;
			mytime[tm_hour] = mytime[tm_hour] - 1;
			return True;

		if mytime[tm_hour] > 24:
			mytime[tm_hour] = mytime[tm_hour] - 24;
			mytime[tm_day] = mytime[tm_day] + 1;
			return True;
		elif mytime[tm_hour] < 0:
			mytime[tm_hour] = mytime[tm_hour] + 24;
			mytime[tm_day] = mytime[tm_day] - 1;
			return True;

		if self._is_leap_year():
			if mytime[tm_day] > self.leap_mon[mytime[tm_mon]]:
				mytime[tm_day] = mytime[tm_day] - self.leap_mon[mytime[tm_mon]];
				mytime[tm_mon] = mytime[tm_mon] + 1;
				return True;
			elif mytime[tm_day] <= 0:
				mytime[tm_day] = mytime[tm_day] + self.leap_mon[mytime[tm_mon] - 1];
				mytime[tm_mon] = mytime[tm_mon] - 1;
				return True;
		else:
			if mytime[tm_day] > self.mon[mytime[tm_mon]]:
				mytime[tm_day] = mytime[tm_day] - self.mon[mytime[tm_mon]];
				mytime[tm_mon] = mytime[tm_mon] + 1;
				return True;
			elif mytime[tm_day] <= 0:
				mytime[tm_day] = mytime[tm_day] + self.mon[mytime[tm_mon] - 1];
				mytime[tm_mon] = mytime[tm_mon] - 1;
				return True;

		if mytime[tm_mon] > 12:
			mytime[tm_mon] = mytime[tm_mon] - 12;
			mytime[tm_year] = mytime[tm_year] + 1;
			return True;
		elif mytime[tm_mon] <= 0:
			mytime[tm_mon] = mytime[tm_mon] + 12;
			mytime[tm_year] = mytime[tm_year] - 1;
			return True;
		return False;

	def _is_leap_year(self):
		myyear = self.mytime[tm_year];
		if myyear % 400 == 0 or (myyear % 4 == 0 and myyear % 100 <> 0):
			return True;
		return False;

tn = Time_Notion();
tn.load_data('./time_type.txt');
tn.init();
struct = dict();
struct['inlist'] = [u'前天'];
tn.encode(struct);
common.print_dic(struct);
