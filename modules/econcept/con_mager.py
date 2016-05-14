#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
import common,config
from net_data import NetData
from mark_objs import MarkObjs
from merge_objs import MergeObjs
from merge_sds import MergeSbDoSth
from con_tail import ConTail

class ConMager():
	def __init__(self):
		self.tag_objs = list();
		self.net_data = NetData();

		self.tag_objs.append(MarkObjs(self.net_data));
		self.tag_objs.append(MergeObjs(self.net_data));
		self.tag_objs.append(MergeSbDoSth(self.net_data));
		self.tag_objs.append(ConTail());

	def init(self,dtype):
		try:
			nfile = config.dfiles[dtype]['1'];
			self.net_data.set_noun_net(nfile);

			vfile = config.dfiles[dtype]['2'];
			self.net_data.set_verb_net(vfile);

			gfile = config.dfiles[dtype]['3'];
			self.net_data.set_gerund_net(gfile);
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			for obj in self.tag_objs:
				obj.encode(struct);
		except Exception as e:
			raise e;
