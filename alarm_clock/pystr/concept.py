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
from scene_base import SceneBase
import scene_param as SceneParam

class Concept(SceneBase):

	def encode(self,struct):
		try:
			if not struct.has_key('inlist'): return None;
			if not struct.has_key('clocks'): struct['clocks'] = list();
			clocks = struct['clocks'];
			for st in struct['inlist']:
				if struct.has_key('time_strs') and st in struct['time_strs']:
					tdic = dict();
					tdic['type'] = '_time';
					tdic['mystr'] = st;
					clocks.append(tdic);
				else:
					tag = False;
					for key in self.data.keys():
						if self._match_item(st,clocks,key) == True:
							tag = True;
							break;
					if tag == False:
						clocks.append(st);
			if struct.has_key('time_strs'): del struct['time_strs'];

		except Exception as e:
			raise MyException(sys.exc_info());

	def _match_item(self,strs,clocks,mtype):
		mdata = self.data[mtype];
		if type(mdata) == list:
			if strs in mdata:
				tdic = dict();
				tdic['mystr'] = strs;
				tdic['type'] = mtype;
				clocks.append(tdic);
				return True;
		return False;

