#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common
#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../scene_common'));
#==============================================================

from common import logging
from guide_data import GuideData
from scene_mager import SceneMager
from myexception import MyException
from guide_analysis import GuideAnalysis

class GuideMager(SceneMager):
	def __init__(self):
		self.dfiles = [
			os.path.join(base_path,'tdata','traffic.txt'),
			os.path.join(base_path,'tdata','guide_data.txt')
		]
		self.tag_objs = list();
		self.ndata = GuideData();
		self.tag_objs.append(GuideAnalysis());
		self.tag_objs.append(self.ndata);

	def encode(self,struct):
		try:
			print 'go into nav guide mager ......';
			for obj in self.tag_objs:
				obj.encode(struct,self.ndata);
		except Exception:
			ee = MyException(sys.exc_info());
			logging.error(str(ee));
			raise ee;
