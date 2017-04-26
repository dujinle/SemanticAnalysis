#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common
#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../scene_common'));
#==============================================================

from common import logging
from shop_data import ShopData
from myexception import MyException
from shop_analy import ShopAnaly
from scene_mager import SceneMager

class ShopMager(SceneMager):
	def __init__(self):
		self.dfiles = [
			os.path.join(base_path,'tdata','under_shop.txt'),
			os.path.join(base_path,'tdata','shop_data.txt')
		];
		self.tag_objs = list();
		self.sdata = ShopData();
		self.tag_objs.append(ShopAnaly());
		self.tag_objs.append(self.sdata);

	def encode(self,struct):
		try:
			print 'go into Shop mager......'
			for obj in self.tag_objs:
				obj.encode(struct,self.sdata);
		except Exception :
			ee = MyException(sys.exc_info());
			logging.error(str(ee));
			raise ee;
