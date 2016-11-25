#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
import common,config
from fetch_math import FetchMath
from fetch_verbs import FetchVerbs
from fetch_artist import FetchArtist
from fetch_belongs import FetchBelongs
from fetch_verb_stc import FetchVerbStc
from fetch_local_unit import FetchLocalUnit

from con_tail import ConTail

class FetchMager():
	def __init__(self):
		self.tag_objs = list();

		self.tag_objs.append(FetchBelongs());
		self.tag_objs.append(FetchVerbs());
		self.tag_objs.append(FetchVerbStc());
		self.tag_objs.append(FetchArtist());
		self.tag_objs.append(FetchMath());
		self.tag_objs.append(FetchLocalUnit());
#		self.tag_objs.append(ConTail());

	def init(self,dtype):
		try:
			step = 1;
			for obj in self.tag_objs:
				obj.load_data(config.dfiles[dtype][str(step)]);
				step = step + 1;

		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			for obj in self.tag_objs:
				obj.encode(struct);
		except Exception as e:
			raise e;
