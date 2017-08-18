#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common
from myexception import MyException
from scene_base import SceneBase
from time_utils import *
import struct_utils as Sutil
#标记用户列表中的数据
class TravelData(SceneBase):
	def __init__(self):
		self.flight = None;
		self.hotel = None;

	def book_flight_time(self,time):
		try:
			bfls = list();
			btime = list(self.flight['time']['start']);
			for i,v in enumerate(btime):
				if i < 3: continue;
				else: btime[i] = time['start'][i];

			btt = GetTimeStamp(btime);
			diff = left = 10000;
			for fs in self.flight['fls']:
				ftt = GetTimeStamp(fs['stime']);
				left = abs(ftt - btt);
				if diff > left:
					if len(bfls) > 0: bfls.pop();
					bfls.append(fs);
					diff = left;
			self.flight['book'] = bfls.pop();
			if self.flight.has_key('fls'): del self.flight['fls'];
		except Exception :
			raise MyException(sys.exc_info());

	def book_flight_fno(self,fno):
		pass;

	def get_flight_info(self):
		fls = list();
		stime = self.flight['time']['start'];
		etime = self.flight['time']['end'];
		stt = GetTimeStamp(stime);
		ett = GetTimeStamp(etime);
		for fs in self.data['FLIGHTS']:
			if fs['start'] <> self.flight['start']: continue;
			if fs['end'] <> self.flight['end']: continue;
			ftt = GetTimeStamp(fs['stime']);
			if stt <= ftt and ett >= ftt:
				fls.append(fs);
		self.flight['fls'] = fls;

	def get_hotel_info(self):
		self.hotel.update(self.data['HOTEL'][0]);

