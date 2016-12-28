#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os

import common,config
from common import logging
from scene_engin import SEngin
from myexception import MyException

class SceneMager:
	def __init__(self):
		self.engine = SEngin();

	def init(self,dtype):
		try:
			fdir = config.dfiles[dtype];
			self.engine.init(fdir);
		except Exception as e: raise e;

	def encode(self,struct):
		try:
			self.engine.encode(struct);
		except Exception as e:
			logging.error(str(e));
			raise e;
