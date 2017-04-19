#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common
#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../scene_common'));
#==============================================================

from common import logging
from nav_mark import NavMark
from nav_data import NavData
from myexception import MyException
from nav_analy import NavAnaly
from scene_mager import SceneMager

class NavMager(SceneMager):
	def __init__(self):
		self.dfiles = [
			None,
			os.path.join(base_path,'tdata','under_nav.txt'),
			os.path.join(base_path,'tdata','nav_data.txt')
		];
		self.tag_objs = list();
		self.pdata = NavData();
		self.tag_objs.append(NavMark());
		self.tag_objs.append(NavAnaly());
		self.tag_objs.append(self.pdata);

	def encode(self,struct):
		try:
			print 'go into Nav mager......'
			for obj in self.tag_objs:
				obj.encode(struct,self.pdata);
		except Exception:
			ee = MyException(sys.exc_info());
			logging.error(str(ee));
			raise ee;
