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
import common
from common import MyException

class LabelUnits():

	def __init__(self):
		self.data = None;
		self.tag_time_num = 0;

	def load_data(self,lfile):
		try:
			self.data = common.read_json(lfile);
		except MyException as e: raise e;

	def encode(self,struct):
		try:
			self.tag_time_num = 0;
			inlist = struct['inlist'];
			rlist = self.__check_unit(inlist);
			for key in rlist:
				item = self.data.get(key);
				if not item.has_key('same'): item['same'] = list();
				item['same'].append(key);
				self.__paser_unit(struct,item);

			taglist = struct['taglist'];
			num = len(taglist);
			flag = False;
			while num > 0:
				tag = taglist[num - 1];
				if type(tag) <> dict: flag = False;
				elif tag['type'] <> 'num_time': flag = False;
				elif tag['type'] == 'num_time' and flag == False:
					tag['interval'] = [0,1];
					flag = True;
				num = num - 1;
		except MyException as e:
			print e.value;

	def __paser_unit(self,struct,reg_item):
		try:
			taglist = struct['taglist'];
			same = reg_item.get('same');
			myidx = -1;
			for value in same:
				myidx = taglist.index(value);
				if myidx == 0: return ;
				if myidx <> -1: break;

			mdic = dict();
			mstr = taglist[myidx - 1];
			tcompile = re.compile(reg_item['reg']);
			match = tcompile.match(mstr);
			if match is None: return;
			if match.end() - match.start() == len(mstr):
				mdic = dict();
				mdic['num'] = mstr;
				mdic['type'] = 'num_time';
				mdic['mytype'] = reg_item['type'];
				mdic['value'] = mstr + taglist[myidx];
				del taglist[myidx];
				taglist.remove(mstr);
				taglist.insert(myidx - 1,mdic);
				self.tag_time_num = self.tag_time_num + 1;
		except MyException as e:
			raise e;

	def __check_unit(self,inlist):
		rlist = list();
		for x in inlist:
			for y in self.data.keys():
				if x == y: rlist.append(x);
				if self.data[y].has_key('same'):
					same = self.data[y]['same'];
					if x in same: rlist.append(y);
		return rlist;
'''
lu = LabelUnits();
lu.load_data('./time_unit.txt');
struct = dict();
struct['inlist'] = [u'2014',u'年',u'我们','03',u'月','18',u'号'];
struct['taglist'] = [u'2014',u'年',u'我们','03',u'月','18',u'号'];
lu.encode(struct);
common.print_dic(struct);
'''
