#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common
#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../scene_common'));
#==============================================================

from common import logging
from travel_data import TravelData
from myexception import MyException
from scene_mager import SceneMager
from travel_analy import TravelAnaly

class TravelMager(SceneMager):
	def __init__(self):
		self.tag_objs = list();
		self.dfiles = [
			os.path.join(base_path,'tdata','under_travel.txt'),
			os.path.join(base_path,'tdata','travel_data.txt')
		]
		self.fdata = TravelData();
		self.tag_objs.append(TravelAnaly());
		self.tag_objs.append(self.fdata);

	def encode(self,struct):
		try:
			print 'go into Travel mager......'
			for obj in self.tag_objs:
				obj.encode(struct,self.fdata);
		except Exception as e:
			ee = MyException(sys.exc_info());
			logging.error(str(ee));
			raise ee;
