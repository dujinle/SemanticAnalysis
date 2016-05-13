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
import common
from common import MyException

class Time_Notion:

	def __init__(self):
		self.data = None;
		self.curtime = None;
		pass;

	def load_data(self,tfile):

		try: self.data = common.read_json(tfile);
		except MyException as e: raise e;

	def encode(self,struct):
		try:
			self.curtime = time.localtime();
			inlist = struct.get('inlist');
			for dkey in self.data.keys():
				days = self.data.get(dkey);
				reglist = days.get('same');
				if not self._if_match_tag(inlist,reglist): continue;

				self._get_reg_tag(struct,days.get('notion'),dkey);
				self._get_reg_tag(struct,days.get('decorate'),dkey);
		except MyException as e: raise e;

	def _get_reg_tag(self,struct,data,dtype):
		inlist = struct.get('inlist');
		taglist = struct.get('taglist');
		for key in data.keys():
			for x in taglist:
				if type(x) == dict: continue;
				if x == key:
					idx = taglist.index(x);
					del taglist[idx];
					tdic = dict();
					tdic.update(data[key]);
					tdic['value'] = key;
					tdic['type'] = 'time';
					taglist.insert(idx,tdic);

	def _if_match_tag(self,inlist,reglist):
		if inlist is None or reglist is None: return False;
		rlist = [ x for x in inlist for y in reglist if x.find(y) <> -1 ]
		if len(rlist) > 0: return True;
		return False;
