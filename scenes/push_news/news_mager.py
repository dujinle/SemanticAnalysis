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
from news_data import NewsData
from myexception import MyException
from news_analysis import NewsAnalysis

class NewsMager:
	def __init__(self):
		self.tag_objs = list();
		self.ndata = NewsData();
		self.tag_objs.append(NewsAnalysis());

	def init(self,dtype):
		try:
			step = 1;
			fdir = config.dfiles[dtype];
			self.ndata.load_data(fdir[str(step)]);
			step = step + 1;
			for obj in self.tag_objs:
				obj.load_data(fdir[str(step)]);
				step = step + 1;
		except Exception as e: raise e;

	def encode(self,struct):
		try:
			print 'go into news mager ......';
			for obj in self.tag_objs:
				obj.encode(struct,self.ndata);
		except Exception as e:
			logging.error(str(e));
			print e;
