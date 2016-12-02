#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
import common,config
from net_data import NetData
from mark_num import MarkNum
from mark_objs import MarkObjs
from mark_pronoun import MarkPronoun


class ConMager():
	def __init__(self):
		self.tag_objs = list();
		self.net_data = NetData();

		self.tag_objs.append(MarkObjs(self.net_data,'SomeBody'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomePlace'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomeThing'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomeAbst'));#标记抽象名词
		self.tag_objs.append(MarkObjs(self.net_data,'SomeCopula'));#标记系动词
		self.tag_objs.append(MarkObjs(self.net_data,'Adjs'));
		self.tag_objs.append(MarkObjs(self.net_data,'Verbs'));
		self.tag_objs.append(MarkObjs(self.net_data,'Units'));
		self.tag_objs.append(MarkObjs(self.net_data,'Relate'));
		self.tag_objs.append(MarkNum(self.net_data,'Nums'));
		self.tag_objs.append(MarkPronoun(self.net_data,'Bpronoun'));#标记人称代词
		self.tag_objs.append(MarkPronoun(self.net_data,'Lpronoun'));#标记逻辑代词
		self.tag_objs.append(MarkPronoun(self.net_data,'PlaceSpace'));#标记方位词
		self.tag_objs.append(MarkPronoun(self.net_data,'Adverb'));#标记副词

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
