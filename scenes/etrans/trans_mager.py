#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../scene_common'));
#==============================================================

import common,config
from common import logging
from trans_data import TransData
from myexception import MyException
from trans_analysis import TransAnalysis
from scene_mager import SceneMager

class TransMager(SceneMager):
	def __init__(self):
		self.dfiles = [
			os.path.join(base_path,'tdata','under_trans.txt'),
			os.path.join(base_path,'tdata','trans_data.txt')
		];
		self.tag_objs = list();
		self.tdata = TransData();
		self.tag_objs.append(TransAnalysis());
		self.tag_objs.append(self.tdata);

	def encode(self,struct):
		try:
			print 'go into trans mager......'
			for obj in self.tag_objs:
				obj.encode(struct,self.tdata);
		except Exception as e:
			ee = MyException(sys.exc_info());
			logging.error(str(ee));
			raise ee;
