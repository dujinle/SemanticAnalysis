#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json
import re
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
from base import Base
import common
from common import MyException

class CompositeTime(Base):

	def __init__(self):
		self.data = None;

	def load_data(self,lfile):
		try:
			self.data = common.read_json(lfile);
		except MyException as e: raise e;

	def encode(self,struct):
		try:
			inlist = struct['inlist'];
			taglist = struct['taglist'];
			keys = self.data.keys();
			for key in inlist:
				if key in keys:
					self.__make_sure_interval(taglist,key);
		except MyException as e: raise e;

	def __make_sure_interval(self,taglist,key):
		kdata = self.data.get(key);
		strt = '';
		for tag in taglist:
			if type(tag) == dict and tag['type'].find('time') <> -1:
				strt = strt + 't';
			else: strt = strt + tag;

		reg = kdata['reg'];
		idx = strt.find(reg);
		if idx == -1: return None;
		if idx + 1 >= len(taglist): return None;
		if kdata.has_key('dir'):
			taglist[idx + 1] = dict();
			taglist[idx + 1]['type'] = 'filter';
			taglist[idx + 1]['value'] = key;

			times = taglist[idx];
			times['value'] = times['value'] + key;
			tdir = kdata['dir'];
			if times['type'] == 'num_time':
				if times['meaning'] == 'number':
					if tdir == '-':
						times['interval'] = ['<<',int(times['num']) * -1];
					elif tdir == '+':
						times['interval'] = [int(times['num']),'>>'];
				elif times['meaning'] == 'date':
					if tdir == '-':
						times['interval'] = ['<<',0];
					elif tdir == '+':
						times['interval'] = [1,'>>'];
			elif times.has_key('interval'):
				if tdir == '-':
					times['interval'] = ['<<',times['interval'][0]];
				elif tdir == '+':
					times['interval'] = [times['interval'][1],'>>'];

		for tag in taglist:
			if type(tag) == dict and tag['type'] == 'filter':
				taglist.remove(tag);

