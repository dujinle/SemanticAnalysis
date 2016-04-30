#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,time,common
import time_common,re,datetime
from myexception import MyException

base_path = os.path.dirname(__file__);
#世纪类型时间处理[19世纪20年代 19世纪初期 ......]#
class TimeModule():

	def __init__(self):
		self.data = None;
		self.dfiles = [
			os.path.join(base_path,'tdata','time_init_data.txt')
		];

	def load_data(self):
		try:
			if self.data is None: self.data = dict();
			for f in self.dfiles:
				self.data.update(common.read_json(f));
		except Exception :
			raise MyException(sys.exc_info());

	def encode(self,struct,key):
		try:
			if not struct.has_key(key): return None;
			if key == 'TimeFestival':
				self.time_festival(struct,key);
			elif key == 'TimeRegion':
				self.time_region(struct,key);
			elif key == 'TimeWeek':
				self.time_region(struct,key);
			elif key == 'TimeWeekFestival':
				self.time_week_festival(struct,key);
			elif key == 'TimeDecade':
				self.time_decade(struct,key);
			elif key == 'TimeNunit':
				self.time_nunit(struct,key);
			elif key == 'TimeSolarTerm':
				self.time_solarterm(struct,key);
		except Exception:
			raise MyException(sys.exc_info());

	def time_festival(self,struct,key):
		for item in struct[key]:
			mdate = item['date'];
			item['stime'] = time_common._create_null_time();
			item['etime'] = time_common._create_null_time();

			(month,day) = mdate.split('/');

			item['stime'][time_common.tmenu['month']] = int(month);
			item['etime'][time_common.tmenu['month']] = int(month);

			item['stime'][time_common.tmenu['day']] = int(day);
			item['etime'][time_common.tmenu['day']] = int(day) + 1;
			item['scope'] = 'day';

	def time_region(self,struct,key):
		cur_time = time.localtime();
		for item in struct[key]:
			mdate = item['region'];
			item['stime'] = time_common._create_null_time();
			item['etime'] = time_common._create_null_time();
			idx = time_common.tmenu[item['scope']];
			if item['scope'] == 'week':
				day_idx = time_common.tmenu['day'];
				item['stime'][day_idx] = cur_time[day_idx] + int(mdate[0]) - cur_time[idx];
				item['etime'][day_idx] = cur_time[day_idx] + int(mdate[1]) - cur_time[idx];
				item['scope'] = 'day';
				continue;
			if item.has_key('func') and item['func'] == 'add':
				item['stime'][idx] = int(mdate[0]) + cur_time[idx];
				item['etime'][idx] = int(mdate[1]) + cur_time[idx];
			else:
				item['stime'][idx] = int(mdate[0]);
				item['etime'][idx] = int(mdate[1]);

	def time_week_festival(self,struct,key):
		cur_time = time.localtime();
		for item in struct[key]:
			item['stime'] = time_common._create_null_time();
			item['etime'] = time_common._create_null_time();

			item['stime'][time_common.tmenu['month']] = int(item['month']);
			item['etime'][time_common.tmenu['month']] = int(item['month']);
			mdate = datetime.date(cur_time[time_common.tmenu['year']],int(item['month']),1);
			nmdate = datetime.date(cur_time[time_common.tmenu['year']],int(item['month']) + 1,1);
			week = mdate.weekday();
			nweek = nmdate.weekday();
			left_day = 0;
			if int(item['week_idx']) > 0:
				if week < int(item['week']):
					left_day = int(item['week']) - week + 1;
				else:
					left_day = 7 - week + int(item['week']);
				left_day = (int(item['week_idx']) - 1) * 7 + left_day;
				item['stime'][time_common.tmenu['day']] = left_day;
				item['etime'][time_common.tmenu['day']] = left_day + 1;
			elif int(item['week_idx']) == -1:
				left_day = int(item['week']) - nweek - 7 + 1;
				item['stime'][time_common.tmenu['month']] = int(item['month']) + 1;
				item['etime'][time_common.tmenu['month']] = int(item['month']) + 1;
				item['stime'][time_common.tmenu['day']] = left_day;
				item['etime'][time_common.tmenu['day']] = left_day + 1;
			item['scope'] = 'day';

	def time_decade(self,struct,key):
		for item in struct[key]:
			item['stime'] = time_common._create_null_time();
			item['etime'] = time_common._create_null_time();
			year_num = re.findall('\d+',item['str']);
			if len(year_num) > 0: year_num = year_num[0];
			if item['scope'] == 'decade_desc':
				item['stime'][time_common.tmenu['year']] = (int(year_num) - 1) * 100 + int(item['region'][0]);
				item['etime'][time_common.tmenu['year']] = (int(year_num) - 1) * 100 + int(item['region'][1]);
			elif item['scope'] == 'decade':
				item['stime'][time_common.tmenu['year']] = (int(year_num) - 1) * 100;
				item['etime'][time_common.tmenu['year']] = int(year_num) * 100;
			elif item['scope'] == 'year':
				item['stime'][time_common.tmenu['year']] = int(year_num)
				item['etime'][time_common.tmenu['year']] = int(year_num) + 10;
			item['scope'] = 'year';

	def time_nunit(self,struct,key):
		for item in struct[key]:
			try:
				item['stime'] = time_common._create_null_time();
				item['etime'] = time_common._create_null_time();
				num = re.findall('\d+',item['str']);
				for sid,scope in enumerate(item['scope']):
					idx = time_common.tmenu[scope];
					inum = num[sid];
					if item['type'] == 'date':
						item['stime'][idx] = int(inum);
						if sid == len(item['scope']) - 1:
							item['etime'][idx] = int(inum) + 1;
							item['scope'] = scope;
						else:
							item['etime'][idx] = int(inum);
					else:
						item['num'] = inum;
			except Exception:
				raise MyException(sys.exc_info());

	def time_solarterm(self,struct,key):
		solarterm = self.data.get('SolarTerm');
		for item in struct[key]:
			item['stime'] = time_common._create_null_time();
			item['etime'] = time_common._create_null_time();
			solar = solarterm[int(item['order'])];

			item['stime'][time_common.tmenu['month']] = int(solar['month']);
			item['etime'][time_common.tmenu['month']] = int(solar['month']);
			item['stime'][time_common.tmenu['day']] = int(solar['day']);
			item['etime'][time_common.tmenu['day']] = int(solar['day']) + 1;
			item['scope'] = 'day';
