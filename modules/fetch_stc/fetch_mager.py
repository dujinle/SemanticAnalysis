#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys
import common,config
import struct_utils as Sutil
from fetch_1layer import Fetch1Layer
from fetch_2layer import Fetch2Layer
from fetch_3layer import Fetch3Layer
from fetch_math import FetchMath
from fetch_before import FetchBefore

from fetch_tail import FetchTail

class FetchMager():
	def __init__(self):
		self.tag_objs = list();
		self.tail = FetchTail();

		self.tag_objs.append(FetchBefore()); #简单消除歧义词性
		self.tag_objs.append(Fetch1Layer());
		self.tag_objs.append(Fetch2Layer());
		self.tag_objs.append(Fetch3Layer());
		self.tag_objs.append(Fetch3Layer());

		self.tag_objs.append(FetchMath());

	def init(self,dtype):
		try:
			step = 1;
			for obj in self.tag_objs:
				obj.load_data(config.dfiles[dtype][str(step)]);
				step = step + 1;

		except Exception as e:
			raise e;

	def encode(self,struct):
		try:
			struct['remove'] = list();
			struct['deal'] = True;
			idx = 0;
			while True:
				if struct.has_key('deal') and struct['deal'] == True:
					for obj in self.tag_objs:
						obj.encode(struct);
				else:
					break;
				idx = idx + 1;
			del struct['deal'];
			self.tail.encode(struct);
		except Exception as e:
			raise e;
