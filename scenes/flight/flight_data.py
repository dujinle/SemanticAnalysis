#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common
from myexception import MyException
from com_base import ComBase as FlightBase
import struct_utils as Sutil
#标记用户列表中的数据
class FlightData(FlightBase):
	def __init__(self):
		FlightBase.__init__(self);
		self.fls = None;
		self.history = None;

	def get_flight_info(self,flight):
		self.history = 'Flight';
		self.fls = list();
		for fs in self.data['FLIGHTS']:
			if fs['start'] <> flight['start']: continue;
			if fs['end'] <> flight['end']: continue;
			self.fls.append(fs);
		return self.fls;

	def get_flight(self,time):
		itime = time['start'];
		if itime[0] == 'null':
			itime = time['end'];

		stime = str(itime[3]);
		if itime[4] <> 'null':
			stime = stime + ':' + str(itime[4]);
		else:
			stime = stime + ':0';
		if self.fls is None: self.fls = self.data['FLIGHTS']
		for fs in self.fls:
			if fs['stime'] == stime:
				return fs;
		return None;

	def get_hotel(self,addr,level):
		self.history = 'Hotel';
		for ht in self.data['HOTEL']:
			if ht['place'] == addr['str']:
				if level['str'] == ht['level']:
					return ht;
		return None;
