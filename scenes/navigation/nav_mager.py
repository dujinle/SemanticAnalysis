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
from mark_body import MarkBody
from myexception import MyException
from nav_analysis import NavAnalysis

class NavMager:
	def __init__(self):
		self.tag_objs = list();
		self.tag_objs.append(MarkBody());
		self.tag_objs.append(NavAnalysis());

	def init(self,dtype):
		try:
			step = 1;
			fdir = config.dfiles[dtype];
			for obj in self.tag_objs:
				obj.load_data(fdir[str(step)]);
				step = step + 1;
		except Exception as e: raise e;

	def encode(self,struct):
		try:
			print 'go into Nav mager......'
			for obj in self.tag_objs:
				obj.encode(struct,self);
		except Exception as e:
			logging.error(str(e));
			print e;
