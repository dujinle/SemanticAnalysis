#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,time,common
import time_common,re
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

	def time_region(self,struct,key):
		cur_time = time.localtime();
		for item in struct[key]:
			mdate = item['region'];
			item['stime'] = time_common._create_null_time();
			item['etime'] = time_common._create_null_time();
			idx = time_common.tmenu[item['scope']];
			if item.has_key('func') and item['func'] == 'add':
				item['stime'][idx] = int(mdate[0]) + cur_time[idx];
				item['etime'][idx] = int(mdate[1]) + cur_time[idx];
			elif item['scope'] == 'week':
				day_idx = time_common.tmenu['day'];
				item['stime'][day_idx] = cur_time[day_idx] + int(mdate[0]) - cur_time[idx];
				item['etime'][day_idx] = cur_time[day_idx] + int(mdate[1]) - cur_time[idx];
			else:
				item['stime'][idx] = int(mdate[0]);
				item['etime'][idx] = int(mdate[1]);

	def time_week_festival(self,struct,key):
		for item in struct[key]:
			item['stime'] = time_common._create_null_time();
			item['etime'] = time_common._create_null_time();
			item['stime'][time_common.tmenu['week']] = int(item['week']) - 1;
			item['etime'][time_common.tmenu['week']] = int(item['week']);
			item['stime'][time_common.tmenu['week_idx']] = int(item['week_idx']);
			item['etime'][time_common.tmenu['week_idx']] = int(item['week_idx']);

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

	def time_nunit(self,struct,key):
		for item in struct[key]:
			item['stime'] = time_common._create_null_time();
			item['etime'] = time_common._create_null_time();
			num = re.findall('\d+',item['str']);
			if len(num) > 0: num = num[0];
			if item['type'] == 'date':
				if item.has_key('mnum'):
					item['stime'][time_common.tmenu[item['scope']]] = int(num) + int(item['mnum']);
					item['etime'][time_common.tmenu[item['scope']]] = int(num) + int(item['mnum']) + 1;
				else:
					item['stime'][time_common.tmenu[item['scope']]] = int(num);
					item['etime'][time_common.tmenu[item['scope']]] = int(num) + 1;

	def time_solarterm(self,struct,key):
		solarterm = self.data.get('SolarTerm');
		for item in struct[key]:
			item['stime'] = time_common._create_null_time();
			item['etime'] = time_common._create_null_time();
			solar = solarterm[int(item['order'])];

			item['stime'][time_common.tmenu['month']] = int(item['month']);
			item['etime'][time_common.tmenu['month']] = int(item['month']);
			item['stime'][time_common.tmenu['day']] = int(item['day']);
			item['etime'][time_common.tmenu['day']] = int(item['day']) + 1;
