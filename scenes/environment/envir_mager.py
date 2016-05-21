#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common
#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../scene_common'));
#==============================================================

from common import logging
from envir_data import EnvirData
from scene_mager import SceneMager
from myexception import MyException
from envir_dist import EnvirDist
from envir_temp import EnvirTemp
from envir_volume import EnvirVolume

class EnvirMager(SceneMager):
	def __init__(self):
		self.dfiles = [
			os.path.join(base_path,'tdata','envir_dist.txt'),
			os.path.join(base_path,'tdata','envir_temp.txt'),
			os.path.join(base_path,'tdata','envir_volume.txt'),
			os.path.join(base_path,'tdata','envir_data.txt')
		]
		self.tag_objs = list();
		self.ndata = EnvirData();
		self.tag_objs.append(EnvirDist());
		self.tag_objs.append(EnvirTemp());
		self.tag_objs.append(EnvirVolume());
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
