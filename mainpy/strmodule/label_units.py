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

	def load_data(self,lfile):
		try:
			self.data = common.read_json(lfile);
		except MyException as e:
			print e.value;

	def paser_units(self,struct):
		try:
			inlist = struct['inlist'];
			keys = self.data.keys();
			for key in keys:
				item = self.data.get(key);
				item['value'] = key;
				match = self.__paser_unit(inlist,item);
				if match is None:
					continue;
				if not struct.has_key('match'):
					struct['match'] = list();
				struct['match'].append(match);
				break;
		except MyException as e:
			print e.value;

	def __paser_unit(self,inlist,reg_item):
		try:
			ldata = list();
			ldata.append(reg_item.get('value'));
			same = reg_item.get('same');
			if not same is None:
				ldata.append(same);
			value = self.__check_unit(ldata,inlist);
			if value is None: return;

			idx = inlist.index(value);
			if idx == 0: return ;

			mdic = dict();
			mstr = inlist[idx - 1];
			regstr = reg_item['reg'];
			tcompile = re.compile(regstr);
			match = tcompile.match(mstr);
			if match is None: return;
			if match.end() - match.start() == len(mstr):
				mdic['match'] = mstr;
				mdic['reg'] = reg_item['reg'];
			return mdic;
		except MyException as e:
			raise e;

	def __check_unit(self,ldata,inlist):
		for lstr in ldata:
			if lstr in inlist: return lstr;
		return None;

lu = LabelUnits();
lu.load_data('./time_unit.txt');
struct = dict();
struct['inlist'] = [u'3',u'号'];
lu.paser_units(struct);
common.print_dic(struct);

