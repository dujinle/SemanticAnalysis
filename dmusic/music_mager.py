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
from music_data import MusicData
from myexception import MyException
from music_analysis import MusicAnalysis

class MusicMager:
	def __init__(self):
		self.tag_objs = list();
		self.mdata = MusicData();
		self.tag_objs.append(MusicAnalysis());

	def init(self,dtype):
		try:
			step = 1;
			fdir = config.dfiles[dtype];
			self.mdata.load_data(fdir[str(step)]);
			step = step + 1;
			for obj in self.tag_objs:
				obj.load_data(fdir[str(step)]);
				step = step + 1;
		except Exception as e: raise e;

	def encode(self,struct):
		try:
			print 'go into music mager......'
			for obj in self.tag_objs:
				obj.encode(struct,self.mdata);
		except Exception as e:
			logging.error(str(e));
			print e;
