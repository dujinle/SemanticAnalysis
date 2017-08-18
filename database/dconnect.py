#!/usr/bin/python
#-*- coding:utf-8 -*-
from mongodb import BaseConnect
from commons import common

class Connect(BaseConnect):

	__instance = None;
	def __new__(cls,*args,**kw):
		if Connect.__instance is None:
			Connect.__instance = object.__new__(cls,*args,**kw);
			return Connect.__instance;

	def __init__(self,*args,**kw):
		super(Connect,self).__init__(*args,**kw);

	def connect(self,username = None,password = None,host = None,database = None):
		super(Connect,self).connect(username = username,password = password,host = host,database = database);


	def get_conn(self): return self.conn;

	def get_db(self): return self.db;

	def get_table(self,table_name):
		return super(Connect,self).get_table(table_name);

	def colse(self): super(Connect,self).close();

'''
	the super class define
	def insert_data(self,data):
		try:
			super.insert_data(data);
		except Exception as e:
			raise e;

	def update_data(self,data):
		try:
			super.update_data(data);
		except Exception as e:
			raise e;

	def delete_data(self,data):
		try:
			super.delete_data(data);
		except Exception as e:
			raise e;

	def query_data(self,data):
		try:
			super.query_data(data);
		except Exception as e:
			raise e;
'''
