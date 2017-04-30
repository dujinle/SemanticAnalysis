#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,json,os,common
from myexception import MyException
abspath = os.path.dirname(__file__);

#story all the data net info
class NetData():
	def __init__(self):
		self.dfiles = {
			#时间表达式 xx年 等 结构
			"TimeNunit":[
				os.path.join(abspath,'tdata','time_mnum.txt')
			],
			#时间区间表达式 明天 等 结构
			"TimeRegion":[
				os.path.join(abspath,'tdata','time_region.txt')
			],
			#星期表达式 周三 等 结构
			"TimeWeek":[
				os.path.join(abspath,'tdata','time_week.txt')
			],
			#节日表达式 情人节 等 结构
			"TimeFestival":[
				os.path.join(abspath,'tdata','time_festival.txt')
			],
			#与星期相关的节日表达式
			"TimeWeekFestival":[
				os.path.join(abspath,'tdata','time_week_festival.txt')
			],
			#世纪年代表达式
			"TimeDecade":[
				os.path.join(abspath,'tdata','time_decade.txt')
			],
			#24节气表达式
			"TimeSolarTerm":[
				os.path.join(abspath,'tdata','time_solarterm.txt')
			]
		}
		self.data = {
			"TimeNunit":list(),
			"TimeRegion":list(),
			"TimeWeek":list(),
			"TimeFestival":list(),
			"TimeWeekFestival":list(),
			"TimeDecade":list(),
			"TimeSolarTerm":list()
		}

	def get_data_key(self,key):
		if self.data.has_key(key):
			return self.data[key];
		return None;

	def load_data(self):
		for key in self.data.keys():
			dfile = self.dfiles[key];
			if isinstance(dfile,list):
				for tfile in dfile:
					tdic = common.read_json(tfile);
					if not tdic is None:
						self.data[key].extend(tdic);
			else:
				tdic = common.read_json(dfile);
				if not tdic is None:
					self.data[key].extend(tdic);
