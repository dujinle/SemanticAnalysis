#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
import common,config
from MT import MT
from MSR import MSR
from MSN import MSN

from myexception import MyException

class MusicMager:
	def __init__(self):
		self.tag_objs = list();

		# mark tag objs #
		self.tag_objs.append(MT());
		self.tag_objs.append(MSR());
		self.tag_objs.append(MSN());

	def init(self,dtype):
		try:
			step = 1;
			fdirs = config.dfiles[dtype];
			for obj in self.tag_objs:
				obj.load_data(fdirs[str(step)]);
				step = step + 1;
		except Exception as e: raise e;

	def encode(self,struct):
		try:
			struct['music'] = struct['inlist'][:];
			for obj in self.tag_objs:
				obj.encode(struct);
			return struct;
		except Exception as e:
			raise e;

	def deal_data(self,fname,action,data):
		try:
			ret = obj = None;
			if fname[0] == 'M':
				obj = self.tag_objs[0];
			elif fname[0] == 'S':
				obj = self.tag_objs[1];
			elif fname[0] == 'N':
				obj = self.tag_objs[2];

			if obj is None: return None;
			if action == 'add':
				ret = obj._add(data);
			elif action == 'del':
				ret = obj._del(data);
			elif action == 'get':
				ret = obj._get({'type':fname});
				return ret;
		except Exception as e:
			raise e;

	def write_file(self,dtype):
		try:
			step = 1;
			dfiles = config.dfiles[dtype];
			for obj in self.tag_objs:
				obj.write_file(dfiles[str(step)]);
				step = step + 1;
		except Exception as e:
			raise e;
'''
try:
	mg = MusicMager();
	mg.init('Music');
	struct = dict();
	struct['text'] = u'来一首笨小孩';
	struct['inlist'] = [u'来',u'一首',u'笨小孩'];
	mg.encode(struct);
	common.print_dic(struct);
except Exception as e:
	raise e;
'''
