#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common
from myexception import MyException
import struct_utils as Sutil
#标记对象名词以及链接的网络
class MarkObjs():
	def __init__(self,conn):
		self.conn = conn;
		self.table = None;
		self.label = None;

	def load_data(self,dfile): pass;

	def encode(self,struct,table,label):
		try:
			self.label = label;
			self.table = table;
			if not struct.has_key(table): struct[table] = list();
			self._mark_objs_list(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _mark_objs_list(self,struct):
		try:
			self.conn.get_table(self.table);

			for tstr in struct[self.label]:
				res = self.conn.query_data({'str':tstr});
				if res.count() <= 0:
					continue;
				for item in res:
					if not item.has_key('stype'):
						print '%s,no stype[%s]' %(tstr,self.table);
					else:
						myd = dict();
						myd['stype'] = item['stype'].replace('_','');
						myd['type'] = item['type'].replace('_','');
						myd['str'] = item['str'];
						myd['track'] = item['track'];
						struct[self.table].append(myd);
		except Exception as e:
			raise MyException(sys.exc_info());
