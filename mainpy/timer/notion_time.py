#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,time
reload(sys)
sys.setdefaultencoding('utf-8')
#=================================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#=================================================
from base import Base
import common
from common import MyException

class TimeNotion(Base):

	def __init__(self):
		self.data = None;
		pass;

	def load_data(self,tfile):
		try: self.data = common.read_json(tfile);
		except MyException as e: raise e;

	def encode(self,struct):
		try:
			inlist = struct.get('inlist');
			for dkey in self.data.keys():
				days = self.data.get(dkey);
				self._get_reg_tag(struct,days.get('notion'));
				self._get_reg_tag(struct,days.get('decorate'));
		except MyException as e: raise e;

	def _get_reg_tag(self,struct,data):
		inlist = struct.get('inlist');
		taglist = struct.get('taglist');
		for key in data.keys():
			for x in taglist:
				if type(x) == dict: continue;
				if x == key:
					idx = taglist.index(x);
					taglist[idx] = dict();
					taglist[idx]['value'] = key;
					taglist[idx]['type'] = 'ex_time';
					taglist[idx].update(data[key]);
