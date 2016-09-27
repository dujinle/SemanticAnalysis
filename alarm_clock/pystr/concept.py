#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,copy
import re,time,math,datetime
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import common
from myexception import MyException
from base import Base

class Concept(Base):

	def encode(self,struct):
		try:
			if not struct.has_key('inlist'): return None;
			if not struct.has_key('clocks'): struct['clocks'] = list();
			clocks = struct['clocks'];

			for st in struct['inlist']:
				if st == 'time':
					tdic = dict();
					tdic['type'] = '_time';
					tdic['mystr'] = struct['rep'][0];
					struct['text'] = struct['text'].replace('time',tdic['mystr'],1);
					clocks.append(tdic);
					del struct['rep'][0];
				for key in self.data.keys():
					self._match_item(st,clocks,key);
			if struct.has_key('rep'): del struct['rep'];

		except MyException as e: raise e;

	def _match_item(self,strs,clocks,mtype):
		mdata = self.data[mtype];
		if type(mdata) == list:
			if strs in mdata:
				tdic = dict();
				tdic['mystr'] = strs;
				tdic['type'] = mtype;
				clocks.append(tdic);

