#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common
#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../scene_common'));
#==============================================================

from common import logging
from myexception import MyException
from calc_analy import CalcAnaly
from scene_mager import SceneMager

class CalcMager(SceneMager):
	def __init__(self):
		self.dfiles = [
			os.path.join(base_path,'tdata','under_calc.txt')
		];
		self.tag_objs = list();
		self.tag_objs.append(CalcAnaly());
		self.tag_objs.append(None);

	def encode(self,struct):
		try:
			print 'go into Math mager......'
			for obj in self.tag_objs:
				obj.encode(struct,self);
		except Exception as e:
			ee = MyException(sys.exc_info());
			logging.error(str(ee));
			raise ee;
