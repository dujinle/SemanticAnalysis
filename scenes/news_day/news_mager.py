#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../scene_common'));
#==============================================================

import common
from common import logging
from myexception import MyException
from scene_mager import SceneMager
from news_data import NewsData
from news_analysis import NewsAnalysis

class NewsMager(SceneMager):
	def __init__(self):
		self.dfiles = [
			os.path.join(base_path,'tdata','under_model.txt'),
			os.path.join(base_path,'tdata','pnews.txt')
		];
		self.tag_objs = list();
		self.ndata = NewsData();
		self.tag_objs.append(NewsAnalysis());
		self.tag_objs.append(self.ndata);

	def encode(self,struct):
		try:
			print 'go into news mager ......';
			for obj in self.tag_objs:
				obj.encode(struct,self.ndata);
		except Exception as e:
			ee = MyException(sys.exc_info());
			logging.error(str(ee));
			raise ee;
