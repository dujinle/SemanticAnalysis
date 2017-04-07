#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common
#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../scene_common'));
#==============================================================

from common import logging
from cal_data import CalData
from myexception import MyException
from cal_analysis import CalAnalysis
from scene_mager import SceneMager

class CalMager(SceneMager):
	def __init__(self):
		self.dfiles = [
			os.path.join(base_path,'tdata','under_cal.txt'),
			os.path.join(base_path,'tdata','cal_data.txt')
		]
		self.tag_objs = list();
		self.pdata = CalData();
		self.tag_objs.append(CalAnalysis());
		self.tag_objs.append(self.pdata);

	def encode(self,struct):
		try:
			print 'go into calendar mager......'
			for obj in self.tag_objs:
				obj.encode(struct,self.pdata);
		except Exception as e:
			ee = MyException(sys.exc_info());
			logging.error(str(ee));
			raise ee;
