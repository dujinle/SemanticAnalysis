#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
import common,config
import struct_utils as Sutil
from fetch_01layer import Fetch01Layer
from fetch_02layer import Fetch02Layer
from fetch_03layer import Fetch03Layer
from fetch_10layer import Fetch10Layer
from fetch_11layer import Fetch11Layer
from fetch_math import FetchMath
from fetch_before import FetchBefore

from fetch_tail import FetchTail

class FetchMager():
	def __init__(self):
		self.f1_layer = list();
		self.f2_layer = list();
		self.tail = FetchTail();

		self.f1_layer.append(FetchBefore()); #简单消除歧义词性
		self.f1_layer.append(Fetch01Layer());#处理同一词性结构
		self.f1_layer.append(Fetch02Layer());#处理组合后词性结构发生改变
		self.f1_layer.append(Fetch03Layer());
		self.f1_layer.append(FetchMath());

		self.f2_layer.append(Fetch10Layer());
		self.f2_layer.append(Fetch11Layer());

	def init(self,dtype):
		try:
			step = 1;
			for obj in self.f1_layer:
				obj.load_data(config.dfiles[dtype][str(step)]);
				step = step + 1;
			for obj in self.f2_layer:
				obj.load_data(config.dfiles[dtype][str(step)]);
				step = step + 1;

		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			struct['remove'] = list();
			struct['deal'] = True;
			while True:
				if struct.has_key('deal') and struct['deal'] == True:
					for obj in self.f1_layer:
						obj.encode(struct);
				else: break;

			struct['deal'] = True;
			while True:
				if struct.has_key('deal') and struct['deal'] == True:
					for obj in self.f2_layer:
						obj.encode(struct);
				else: break;
			del struct['deal'];
			self.tail.encode(struct);
		except Exception as e:
			raise e;
