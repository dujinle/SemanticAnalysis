#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#==============================================================

import common,config
from common import logging
from flight_data import FlightData
from myexception import MyException
from flight_analysis import FlightAnalysis

class FlightMager:
	def __init__(self):
		self.tag_objs = list();
		self.fdata = FlightData();
		self.tag_objs.append(FlightAnalysis());

	def init(self,dtype):
		try:
			step = 1;
			fdir = config.dfiles[dtype];
			self.fdata.load_data(fdir[str(step)]);
			step = step + 1;
			for obj in self.tag_objs:
				obj.load_data(fdir[str(step)]);
				step = step + 1;
		except Exception as e: raise e;

	def encode(self,struct):
		try:
			print 'go into Flight mager......'
			for obj in self.tag_objs:
				obj.encode(struct,self.fdata);
		except Exception as e:
			logging.error(str(e));
			print e;
