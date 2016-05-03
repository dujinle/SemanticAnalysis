#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common
from pdeal_replace import PDealReplace
from pdeal_hanzi2num import PDealHan2num
from myexception import MyException

base_path = os.path.dirname(__file__);

class PDealMager:
	def __init__(self):
		self.tag_objs = list();

		self.dfiles = [
			os.path.join(base_path,'tdata','pdeal_hanzi2num.txt'),
			os.path.join(base_path,'tdata','pdeal_replace.txt')
		]
		# mark tag objs #
		self.tag_objs.append(PDealHan2num());
		self.tag_objs.append(PDealReplace());

	def init(self,dtype):
		try:
			for i,obj in enumerate(self.tag_objs):
				obj.load_data(self.dfiles[i]);
		except Exception as e: raise e;

	def encode(self,struct):
		try:
			print 'go into pdeal......';
			for obj in self.tag_objs:
				obj.encode(struct);
		except Exception as e:
			raise MyException(sys.exc_info());
