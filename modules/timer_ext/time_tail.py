#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,time,common
import time_common,re
from myexception import MyException
import time_calendar as time_tool

class TimeTail():

	def __init__(self):
		self.after = u'后';
		self.prev = u'前';

	def load_data(self): pass;

	def encode(self,struct):
#		common.print_dic(struct);
		for item in struct['time_stc']:
			astr = item['str'] + self.after;
			pstr = item['str'] + self.prev;
			aid = struct['text'].find(astr);
			pid = struct['text'].find(pstr);
			time_common._make_sure_time(item['stime'],item['scope']);
			time_common._make_sure_time(item['etime'],item['scope']);
			if aid <> -1:
				self.fetch_time_after(item,astr);
			if pid <> -1:
				self.fetch_time_prev(item,astr);
			self.year_type_match(item);
			self.remove_item_ext(item);
		self.remove_time_item(struct);

	def fetch_time_after(self,item,istr):
		item['str'] = istr;
		item['stime'] = list();
		item['stime'].extend(item['etime']);
		item['etime'][time_common.tmenu['enable']] = -1;

	def fetch_time_prev(self,item,istr):
		item['str'] = istr;
		item['etime'] = list();
		item['etime'].extend(item['stime']);
		item['stime'][time_common.tmenu['enable']] = -1;

	#移除无效的时间对象 通过最长匹配原则
	def remove_time_item(self,struct):
		struct['time_stcs'] = dict();
		slen = len(struct['text']);
		sid = flg = 0;eid = slen;
		while True:
			if sid > slen: break;
			istr = struct['text'][sid:eid];
			flg = 0;
			for item in struct['time_stc']:
				if item['str'] == istr:
					sid = eid;
					eid = slen;
					flg = 1;
					struct['time_stcs'][istr] = item;
					break;
			if flg == 0:
				eid = eid - 1;
			if eid == 0:
				eid = slen;
				sid = sid + 1;
		del struct['time_stc'];

	def remove_item_ext(self,item):
		idx = 0;
		while True:
			if idx >= len(item.keys()): break;
			key = item.keys()[idx];
			if key == 'stime' or key == 'etime' or key == 'str' or key == 'scope':
				idx = idx + 1;
				continue;
			else:
				del item[key];
				continue;

	def year_type_match(self,item):
		if item.has_key('year_type') and item['year_type'] == 'lunar':
			myear = item['stime'][time_common.tmenu['year']];
			mmonth = item['stime'][time_common.tmenu['month']];
			mday = item['stime'][time_common.tmenu['day']];
			(year,month,day) = time_tool.ToSolarDate(myear,mmonth,mday);
			item['stime'][time_common.tmenu['year']] = year;
			item['stime'][time_common.tmenu['month']] = month;
			item['stime'][time_common.tmenu['day']] = day;

			myear = item['etime'][time_common.tmenu['year']];
			mmonth = item['etime'][time_common.tmenu['month']];
			mday = item['etime'][time_common.tmenu['day']];
			(year,month,day) = time_tool.ToSolarDate(myear,mmonth,mday);
			item['etime'][time_common.tmenu['year']] = year;
			item['etime'][time_common.tmenu['month']] = month;
			item['etime'][time_common.tmenu['day']] = day;
