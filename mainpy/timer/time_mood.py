#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,time
reload(sys)
sys.setdefaultencoding('utf-8')
#=================================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#=================================================
import common
from myexception import MyException
from base import Base
class TS(Base):

	def __init__(self):
		self.data = None;
		pass;

	def encode(self,struct):
		try:
			inlist = struct['inlist'];
			taglist = struct['taglist'];
			for key in self.data.keys():
				if key in taglist:
					idx = taglist.index(key);
					taglist[idx] = dict();
					taglist[idx].update(self.data[key]);
		except MyException as e: raise e;

class TM(Base):

	def __init__(self):
		self.data = None;
		pass;

	def encode(self,struct):
		try:
			inlist = struct['inlist'];
			taglist = struct['taglist'];
			for key in self.data.keys():
				if key in taglist:
					idx = taglist.index(key);
					taglist[idx] = dict();
					taglist[idx].update(self.data[key]);
		except MyException as e: raise e;

class AS(Base):

	def __init__(self):
		self.data = None;
		pass;

	def encode(self,struct):
		try:
			inlist = struct['inlist'];
			taglist = struct['taglist'];
			for key in self.data.keys():
				if key in taglist:
					idx = taglist.index(key);
					taglist[idx] = dict();
					taglist[idx].update(self.data[key]);
		except MyException as e: raise e;
