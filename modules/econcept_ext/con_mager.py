#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
import common,config
from myexception import MyException
from mark_objs import MarkObjs
from combine_objs import CombineObjs
from remark_words import RemarkWords
from con_tail import ConTail
from database import Connect

import struct_utils as Sutil

class ConMager():
	def __init__(self):
		self.tag_objs = list();
		self.conn = Connect();
		self.mark_objs = MarkObjs(self.conn);
		self.combine_objs = CombineObjs();
		self.tail = ConTail();
		self.remark = RemarkWords();

	def init(self,dtype):
		try:
			self.conn.connect(config.db_user,config.db_pwd,config.db_ip,config.db_name);
			for table in self.conn.get_tables():
				self.tag_objs.append(table);
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			for obj in self.tag_objs:
				self.mark_objs.encode(struct,obj,'inlist');
			self.combine_objs.encode(struct);
			self.tail.encode(struct,self.tag_objs);
			self.remark.encode(struct);
			for obj in self.tag_objs:
				self.mark_objs.encode(struct,obj,'stseg');
			self.combine_objs.encode(struct);
			self.tail.encode(struct,self.tag_objs);

		except Exception as e:
			raise MyException(sys.exc_info());
