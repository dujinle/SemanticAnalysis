#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,time,common
import time_common,re
from myexception import MyException

base_path = os.path.dirname(__file__);

class TimeReduce():

	def __init__(self):
		self.data = None;
		self.dfiles = [
			os.path.join(base_path,'tdata','time_reduce.txt')
		];

	def load_data(self):
		try:
			if self.data is None: self.data = list();
			for f in self.dfiles:
				self.data.extend(common.read_json(f));
		except Exception :
			raise MyException(sys.exc_info());

	def encode(self,struct,keys):
		try:
			if not struct.has_key('time_stc'): struct['time_stc'] = list();
			self.match_item(struct);
			self.merge_time(struct);
			self.fill_time(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def match_item(self,struct):
		for item in self.data:
			comp = re.compile(item['reg']);
			match = comp.search(struct['text']);
			if match is None: continue;
			if item['type'] <> 'hour_hour': continue;
			ret = self.get_match_items(struct,match.group());
			if ret is None: continue;
			ret = self.merge_match_item(ret[0],ret[1],item);
			struct['time_stc'].append(ret);

	def merge_time(self,struct):
		left_list = list();
		while True:
			if len(struct['time_stc']) <= 0: break;
			one_time = False;
			item = struct['time_stc'].pop();
			for it in struct['time_stc']:
				rstr = item['str'] + it['str'];
				lstr = it['str'] + item['str'];
				if struct['text'].find(rstr) <> -1:
					ret = self.merge_item(item,it);
					if not ret is None:
						struct['time_stc'].append(ret);
						struct['time_stc'].remove(it);
						one_time = True;
						break;
				elif struct['text'].find(lstr) <> -1:
					ret = self.merge_item(it,item);
					if not ret is None:
						struct['time_stc'].append(ret);
						struct['time_stc'].remove(it);
						one_time = True;
						break;
			if one_time == False:
				left_list.append(item);
		struct['time_stc'].extend(left_list);

	def merge_match_item(self,sitem,eitem,item):

		ret = time_common._is_merge_able(sitem,eitem,True);
		tdic = dict(sitem);
		tdic.update(eitem);
		tdic['str'] = sitem['str'] + eitem['str'];
		tdic['stime'] = ret[0];
		tdic['etime'] = ret[1];
		idx = time_common.tmenu[item['scope']];
		tdic['stime'][idx] = int(tdic['stime'][idx]) + int(item['mnum']);
		tdic['etime'][idx] = int(tdic['etime'][idx]) + int(item['mnum']);
		return tdic;

	def merge_item(self,sitem,eitem):
		lstr = sitem['str'] + eitem['str'];

		ret = time_common._is_merge_able(sitem,eitem);
		if not ret is None:
			tdic = dict(sitem);
			tdic.update(eitem);
			tdic['str'] = sitem['str'] + eitem['str'];
			tdic['stime'] = ret[0];
			tdic['etime'] = ret[1];
#			tdic['scope'] = sitem['scope'];
			if sitem.has_key('func') and sitem['func'] == 'add':
				tdic['func'] = 'add';
			return tdic;
		return None;

	def fill_time(self,struct):
		cur_time = time.localtime();
		for item in struct['time_stc']:
			if item.has_key('type') and item['type'] == 'num': continue;
			if item.has_key('reg'): del item['reg'];
			if item.has_key('region'): del item['region'];
			idx = time_common.tmenu[item['scope']];
			if idx - 1 < 0: continue;
			item['stime'] = time_common._list_empty_copy(item['stime'],cur_time,idx);
			item['etime'] = time_common._list_empty_copy(item['etime'],cur_time,idx);

	def get_match_items(self,struct,mstr):
		left_list = list();
		while True:
			if len(struct['time_stc']) <= 0: break;
			one_time = False;
			item = struct['time_stc'].pop();
			for it in struct['time_stc']:
				rstr = item['str'] + it['str'];
				lstr = it['str'] + item['str'];
				if rstr == mstr:
					mdic = dict(it);
					struct['time_stc'].remove(it);
					return [item,it];
				if lstr == mstr:
					mdic = dict(item);
					struct['time_stc'].remove(it);
					return [it,item];
			if one_time == False:
				left_list.append(item);
		struct['time_stc'].extend(left_list);
