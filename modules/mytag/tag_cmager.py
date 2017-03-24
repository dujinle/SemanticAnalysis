#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common

from tag_encode import TagEncode
from myexception import MyException

base_path = os.path.dirname(__file__);

class TagMager:
	def __init__(self):
		self.tag_objs = list();

		self.dfiles = [
			os.path.join(base_path,'tdata','mytag.txt')
		];
		# mark tag objs #
		self.tag_objs.append(TagEncode());

	def init(self,dtype):
		try:
			for i,dfile in enumerate(self.dfiles):
				self.tag_objs[i].init(dfile):
		except Exception as e: raise e;

	def encode(self,struct):
		try:
			for obj in self.tag_objs:
				obj.encode(struct);
		except Exception as e:
			raise e;
