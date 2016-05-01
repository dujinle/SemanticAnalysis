#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,re,common
from myexception import MyException
from pdeal_base import PDealBase
import hanzi2num as Han2Num

#汉字数字转换
class PDealHan2num(PDealBase):

	def encode(self,struct):
		try:
			self.match_item(struct);
		except Exception as e:
			raise e;

	def match_item(self,struct):
		try:
			for key in self.data:
				item = self.data[key];
				comp = re.compile(item['reg']);
				match = comp.findall(struct['text']);
				for im in match:
					numstr = Han2Num.cn2dig(im);
					struct['text'] = struct['text'].replace(im,numstr,1);
		except Exception :
			raise MyException(sys.exc_info());
