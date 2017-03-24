#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os

import common
from myexception import MyException
from tag_base import TagBase

class TagEncode(TagBase):

	def init(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except MyException as e:
			raise e;

	def encode(self,struct):
		try:
			struct['tag'] = self.data;
		except MyException as e: raise e;

