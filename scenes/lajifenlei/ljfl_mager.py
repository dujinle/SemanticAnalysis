#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
#==============================================================
''' import tagpy wordsegs '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#==============================================================

from common import logging
from myexception import MyException
from scene_mager import SceneMager
import com_funcs as SceneCommon
from ljfl_data import LJFLData
from ljfl_analysis import LJFLAnalysis
from ljfl_mkobj import LJFLMkobj

class LJFLMager(SceneMager):
	def __init__(self):
		self.tag_objs = list();

		self.dfiles = [
			os.path.join(base_path,'tdata','ljfl_mkobj.txt'),
			os.path.join(base_path,'tdata','ljfl_analysis.txt'),
			None
		]
		self.fdata = LJFLData();
		self.tag_objs.append(LJFLMkobj())
		self.tag_objs.append(LJFLAnalysis());
		self.tag_objs.append(self.fdata);

	def encode(self,struct):
		try:
			print 'go into lajifenlei mager......'
			for obj in self.tag_objs:
				obj.encode(struct,self.fdata);
		except Exception as e:
			print e;
			SceneCommon._set_msg(struct,self.fdata.get_err_msg());
			raise MyException(sys.exc_info());
