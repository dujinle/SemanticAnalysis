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
from music_data import MusicData
from myexception import MyException
from music_analysis import MusicAnalysis
from scene_mager import SceneMager

class MusicMager(SceneMager):
	def __init__(self):
		self.dfiles = [
			os.path.join(base_path,'tdata','under_music.txt'),
			os.path.join(base_path,'tdata','music_data.txt')
		];
		self.tag_objs = list();
		self.mdata = MusicData();
		self.tag_objs.append(MusicAnalysis());
		self.tag_objs.append(self.mdata);

	def encode(self,struct):
		try:
			print 'go into music mager......'
			for obj in self.tag_objs:
				obj.encode(struct,self.mdata);
		except Exception as e:
			ee = MyException(sys.exc_info());
			logging.error(str(ee));
			raise ee;
