#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
import struct_utils as Sutil
from myexception import MyException

class FetchBefore():
	def __init__(self):
		self.data = None;

	def load_data(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			for item in self.data:
				self._fetch_before(struct,item);
		except Exception:
			raise MyException(sys.exc_info());

	def _fetch_before(self,struct,item):
		if not struct.has_key(item['start']): return None;
		if not struct.has_key(item['end']): return None;

		tid = 0;
		while True:
			if tid >= len( struct[item['end']]): break;
			eit = struct[item['end']][tid];
			for sit in struct[item['start']]:
				if sit['str'].find(eit['str']) <> -1:
					del struct[item['end']][tid];
					tid = tid - 1;
					break;
			tid = tid + 1;

