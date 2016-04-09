#!/usr/bin/python
#-*- coding:utf-8 -*-

import redis
from logger import *

class MyRedis:

	def __init__(self):
		self.r = None;

	def get_conn(self,ip,p,dbnum):
		try:
			self.r = redis.Redis(host=ip, port=p, db=dbnum);
			info = self.r.info();
		except Exception as e:
			raise e;
	def insert_data(self,key,value):
		if self.r is None:
			raise ValueError('the redis conn is close');
		try:
			old_data = self.r.getset(key,value);
		except Exception as e:
			raise e;
		if old_data is not None and len(old_data) > 0:
			logging.info('the last save info:' + old_data);
	def get_data(self,key):
		if self.r is None:
			raise ValueError('the redis conn is close');
		try:
			if self.r.exists(key):
				data = self.r.get(key);
				return data;
		except Exception as e:
			raise e;
		return None;
	def save_db(self,key):
		if self.r is None:
			raise ValueError('the redis conn is close');
		try:
			self.r.save();
		except Exception as e:
			raise e;
