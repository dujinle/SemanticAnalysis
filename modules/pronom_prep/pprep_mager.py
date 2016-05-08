#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os

import common,config
from myexception import MyException
from mark_local_prep import MarkLocalPrep
from mark_abs_pronom import MarkAbsPronom
from mark_per_pronom import MarkPerPronom
from calc_local_prep import CalcLocalPrep

class PPrepMager:
	def __init__(self):
		self.tag_objs = list();

		# mark tag objs #
		self.tag_objs.append(MarkLocalPrep());
		self.tag_objs.append(MarkAbsPronom());
		self.tag_objs.append(MarkPerPronom());
		self.tag_objs.append(CalcLocalPrep());

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

