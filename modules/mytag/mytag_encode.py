#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,copy
import re,time,math,datetime
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import common
from myexception import MyException
from base import Base

class MyTagEncode(Base):

	def init(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except MyException as e:
			raise e;

	def encode(self,struct):
		try:
			struct['tag'] = self.data;
		except MyException as e: raise e;

