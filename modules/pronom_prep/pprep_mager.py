#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os

import common,config
from myexception import MyException
from mark_local_prep import MarkLocalPrep
from mark_abs_pronom import MarkAbsPronom
from mark_per_pronom import MarkPerPronom
from mark_prep_combine import MarkPrepCombine
from mark_verb_combine import MarkVerbCombine
from pprep_tail import PPrepTail

class PPrepMager:
	def __init__(self):
		self.tag_objs = list();

		# mark tag objs #
		self.tag_objs.append(MarkLocalPrep());
		self.tag_objs.append(MarkAbsPronom());
		self.tag_objs.append(MarkPerPronom());
		self.tag_objs.append(MarkPrepCombine());
		self.tag_objs.append(MarkVerbCombine());
		#self.tag_objs.append(PPrepTail());

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

