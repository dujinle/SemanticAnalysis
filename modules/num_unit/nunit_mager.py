#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os

import common,config
from myexception import MyException
from mark_num import MarkNum
from mark_unit import MarkUnit
from mark_relat import MarkRelat
from calc_num_unit import CalcNumUnit
from nunit_tail import NunitTail


class NunitMager:
	def __init__(self):
		self.tag_objs = list();

		# mark tag objs #
		self.tag_objs.append(MarkNum());
		self.tag_objs.append(MarkUnit());
		self.tag_objs.append(MarkRelat());
		self.tag_objs.append(CalcNumUnit());
		self.tag_objs.append(NunitTail());

	def init(self,dtype):
		try:
			step = 1;
			dfiles = config.dfiles[dtype];
			for obj in self.tag_objs:
				obj.load_data(dfiles[str(step)]);
				step = step + 1;
		except Exception as e: raise e;

	def encode(self,struct):
		try:
			for obj in self.tag_objs:
				obj.encode(struct);
		except Exception as e:
			raise e;
