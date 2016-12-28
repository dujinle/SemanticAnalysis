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
from shop_data import ShopData
from myexception import MyException
from shop_analysis import ShopAnalysis

class ShopMager:
	def __init__(self):
		self.tag_objs = list();
		self.sdata = ShopData();
		self.tag_objs.append(ShopAnalysis());

	def init(self,dtype):
		try:
			step = 1;
			fdir = config.dfiles[dtype];
			self.sdata.load_data(fdir['1']);
			step = step + 1;
			for obj in self.tag_objs:
				obj.load_data(fdir[str(step)]);
				step = step + 1;
		except Exception as e: raise e;

	def encode(self,struct):
		try:
			print 'go into Shop mager......'
			for obj in self.tag_objs:
				obj.encode(struct,self.sdata);
		except Exception as e:
			logging.error(str(e));
			print e;
