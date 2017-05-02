#!/usr/bin/python
#-*- coding:utf-8 -*-

import os,sys,common
from myexception import MyException
from net_data import NetData
from mark_objs import MarkObjs
from time_module import TimeModule
from time_middle import TimeMiddle
from time_reduce import TimeReduce
from time_tail import TimeTail

class TimeMager():
	def __init__(self):
		self.net_data = NetData();
		self.mobjs = MarkObjs();
		self.tmodu = TimeModule();
		self.tmiddle = TimeMiddle();
		self.treduce = TimeReduce();
		self.tail = TimeTail();

		self.tag_keys = list();
		self.tag_keys.append('TimeNunit');
		self.tag_keys.append('TimeRegion');
		self.tag_keys.append('TimeWeek');
		self.tag_keys.append('TimeFestival');
		self.tag_keys.append('TimeWeekFestival');
		self.tag_keys.append('TimeDecade');
		self.tag_keys.append('TimeSolarTerm');

	def init(self):
		try:
			self.net_data.load_data();
			self.tmodu.load_data();
			self.tmiddle.load_data();
			self.treduce.load_data();
		except Exception as e:
			raise MyException(sys.exc_info());

	def encode(self,struct):
		try:
			for key in self.tag_keys:
				self.mobjs.encode(struct,key,self.net_data);
				self.tmodu.encode(struct,key);
			self.tmiddle.encode(struct,self.tag_keys);
			self.treduce.encode(struct,self.tag_keys);
			self.tail.encode(struct);
		except Exception as e:
			raise MyException(sys.exc_info());
