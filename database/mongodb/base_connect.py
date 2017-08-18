#!/usr/bin/python
#-*- coding:utf-8 -*-

from pymongo import MongoClient

class BaseConnect(object):

	def __init__(self,*args,**kw):
		self.conn = None;
		self.db = None;
		self.table = None;
		self.db_auth = None;

	def connect(self,username = None,password = None,host = None,database = None):
		try:
			if self.db is None:
				self.conn = MongoClient(host,port = 27017);
				self.db_auth = self.conn.get_database("admin");
				self.db_auth.authenticate(username,password);
				return self.creat_db(database);
			else:
				return self.db;
		except Exception as e:
			raise e;

	def creat_db(self,database):
		try:
			self.db = self.conn.get_database(database);
			return self.db;
		except Exception as e:
			raise e;

	def drop_db(self,database):
		try:
			return self.conn.drop_database(database);
		except Exception as e:
			raise e;

	def get_table(self,table_name):
		try:
			self.table = self.db.get_collection(table_name);
			return self.table;
		except Exception as e:
			raise e;

	def get_tables(self):
		try:
			tables = self.db.collection_names();
			return tables;
		except Exception as e:
			raise e;

	def drop_table(self,table_name):
		try:
			self.table = self.db.get_collection(table_name);
			return self.table.drop();
		except Exception as e:
			raise e;

	def close(self): self.conn.close();

	def insert_data(self,data):
		try:
			return self.table.insert(data);
		except Exception as e:
			raise e;

	def update_data(self,data):
		try:
			return self.table.update(data);
		except Exception as e:
			raise e;

	def delete_data(self,data):
		try:
			return self.table.delete_many(data);
		except Exception as e:
			raise e;

	def query_data(self,data):
		try:
			if data is None:
				return self.table.find();
			else:
				return self.table.find(data);
		except Exception as e:
			raise e;
