#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common

class SceneMager:

	def init(self):
		try:
			for i,sfile in enumerate(self.dfiles):
				obj = self.tag_objs[i];
				obj.load_data(self.dfiles[i]);
			self.tag_objs.pop();
		except Exception as e: raise e;

	def encode(self,struct): pass;
