#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
import common,config
from myexception import MyException
from net_data import NetData
from mark_objs import MarkObjs
from mark_nunit import MarkNunit
from con_tail import ConTail

import struct_utils as Sutil

class ConMager():
	def __init__(self):
		self.tag_objs = list();
		self.net_data = NetData();

		self.tag_objs.append(MarkObjs(self.net_data,'SomeNouns'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomeVerbs'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomePois'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomeProns'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomeMoods'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomeTenses'));
		self.tag_objs.append(MarkNunit(self.net_data,'SomeNunit'));
		self.tag_objs.append(MarkObjs(self.net_data,'SomeLogics'));
#		self.tag_objs.append(MarkObjs(self.net_data,'SomeAuxs'));
		self.tail = ConTail();

	def init(self,dtype):
		try:
			self.net_data.load_data();
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			for obj in self.tag_objs:
				obj.encode(struct);
			self.tail.encode(struct);
		except Exception as e:
			raise MyException(sys.exc_info());
