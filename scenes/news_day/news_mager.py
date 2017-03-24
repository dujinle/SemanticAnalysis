#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
#==============================================================

import common
from common import logging
from news_data import NewsData
from myexception import MyException
from news_analysis import NewsAnalysis

class NewsMager:
	def __init__(self):
		self.dfiles = [
			os.path.join(base_path,'tdata','under_model.txt'),
			os.path.join(base_path,'tdata','pnews.txt')
		];
		self.tag_objs = list();
		self.ndata = NewsData();
		self.tag_objs.append(NewsAnalysis());
		self.tag_objs.append(self.ndata);

	def init(self):
		try:
			for i,sfile in enumerate(self.dfiles):
				obj = self.tag_objs[i];
				obj.load_data(self.dfiles[i]);
			self.tag_objs.pop();
		except Exception as e: raise e;

	def encode(self,struct):
		try:
			print 'go into news mager ......';
			for obj in self.tag_objs:
				obj.encode(struct,self.ndata);
		except Exception as e:
			logging.error(str(e));
			print e;
