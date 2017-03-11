#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
import common,config
from mark_dist import MarkDist

class DistMager():
	def __init__(self):
		self.tag_objs = list();
		self.tag_objs.append(MarkDist());

	def init(self,dtype):
		try:
			step = 1;
			dfile = config.dfiles[dtype];
			for obj in self.tag_objs:
				obj.load_data(dfile[str(step)]);
				step = step + 1;
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			for obj in self.tag_objs:
				obj.encode(struct);
		except Exception as e:
			raise e;
