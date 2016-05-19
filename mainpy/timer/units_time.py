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
import common,config
from base import Base
from common import MyException

class LabelUnits(Base):

	def __init__(self):
		self.data = None;

	def encode(self,struct):
		try:
			inlist = struct['inlist'];
			rlist = self.__check_unit(inlist);
			for key in rlist:
				item = self.data.get(key);
				if not item.has_key('same'): item['same'] = list();
				item['same'].append(key);
				self.__paser_unit(struct,item);

		except MyException as e: raise e;

	def __paser_unit(self,struct,reg_item):
		taglist = struct['taglist'];
		same = reg_item.get('same');
		myidx = -1;
		for value in same:
			myidx = taglist.index(value);
			if myidx == 0: return ;
			if myidx <> -1: break;

		mstr = taglist[myidx - 1];
		tcompile = re.compile(reg_item['reg']);
		match = tcompile.match(mstr);
		if match is None: return;
		if match.end() - match.start() == len(mstr):
			mdic = dict();
			mdic['num'] = mstr;
			mdic['type'] = 'num_time';
			mdic['scope'] = reg_item['type'];
			mdic['value'] = mstr + taglist[myidx];
			mdic['meaning'] = reg_item['meaning'];
			del taglist[myidx];
			taglist.remove(mstr);
			taglist.insert(myidx - 1,mdic);

	def __check_unit(self,inlist):
		rlist = list();
		for x in inlist:
			for y in self.data.keys():
				if x == y: rlist.append(x);
				if self.data[y].has_key('same'):
					same = self.data[y]['same'];
					if x in same: rlist.append(y);
		return rlist;
