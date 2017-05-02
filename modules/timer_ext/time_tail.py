#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,time,common
import time_common,re
from myexception import MyException

base_path = os.path.dirname(__file__);

class TimeTail():

	def __init__(self):
		self.after = u'后';
		self.prev = u'前';


	def load_data(self): pass;

	def encode(self,struct):
		for item in struct['time_stc']:
			astr = item['str'] + self.after;
			pstr = item['str'] + self.prev;
			aid = struct['text'].find(astr);
			pid = struct['text'].find(pstr);
			if aid <> -1:
				self.fetch_time_after(item,astr);
				continue;
			if pid <> -1:
				self.fetch_time_prev(item,astr);
				continue;

	def fetch_time_after(self,item,istr):
		if item['type'] == 'num':
			
		item['str'] = istr;
		item['stime'] = list();
		item['stime'].extend(item['etime']);
		item['etime'][time_common.tmenu['enable']] = -1;

	def fetch_time_prev(self,item,istr):
		item['str'] = istr;
		item['etime'] = list();
		item['etime'].extend(item['stime']);
		item['stime'][time_common.tmenu['enable']] = -1;
