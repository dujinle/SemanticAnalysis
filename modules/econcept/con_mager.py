#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
import common,config
from net_data import NetData
from mark_objs import MarkObjs
from mark_pronoun import MarkPronoun

from con_tail import ConTail

class ConMager():
	def __init__(self):
		self.tag_objs = list();
		self.net_data = NetData();

		self.tag_objs.append(MarkObjs(self.net_data,'SomeBody'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomePlace'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomeThing'));
		self.tag_objs.append(MarkObjs(self.net_data,'Adjs'));
		self.tag_objs.append(MarkObjs(self.net_data,'Verbs'));
		self.tag_objs.append(MarkPronoun(self.net_data,'Bpronoun'));
		self.tag_objs.append(MarkPronoun(self.net_data,'Lpronoun'));
		self.tag_objs.append(MarkPronoun(self.net_data,'PlaceSpace'));

	def init(self,dtype):
		try:
			self.net_data.load_data();
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			for obj in self.tag_objs:
				obj.encode(struct);
		except Exception as e:
			raise e;
