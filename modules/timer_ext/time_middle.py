#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,time,common
import time_common,re
from myexception import MyException

base_path = os.path.dirname(__file__);

class TimeMiddle():

	def __init__(self):
		self.data = None;
		self.dfiles = [
			os.path.join(base_path,'tdata','time_middle.txt')
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
			for key in keys:
				struct['time_stc'].extend(struct[key]);
				del struct[key];
#进行一次去重 去除 多余的结构会对下一步造成影响
			self.remove_time_item(struct);
			self.match_item(struct,key);
		except Exception:
			raise MyException(sys.exc_info());

	def match_item(self,struct,key):
		for item in self.data:
			comp = re.compile(item['reg']);
			match = comp.search(struct['text']);
			if match is None: continue;
			if item['type'] == 'big':
				self.merge_big_time(struct,item,match.group());
			elif item['type'] == 'up_down_week':
				self.merge_up_down_week(struct,item,match.group());
			elif item['type'] == 'up_down_week_region':
				self.merge_up_down_week_region(struct,item,match.group());
			elif item['type'] == 'up_down_num':
				self.merge_up_down_num(struct,item,match.group());
			elif item['type'] == 'prev_after_num':
				self.merge_prev_after_num(struct,item,match.group());

	def merge_big_time(self,struct,it,mstr):
		cur_time = time.localtime();
		comp = re.compile(it['sreg']);
		match = comp.search(mstr);
		for item in struct['time_stc']:
			lstr = match.group() + item['str'];
			if lstr <> mstr: continue;
#			common.print_dic(item);
			item['str'] = mstr;
			if it['dir'] == '-':
				idx = time_common.tmenu[it['scope']];
				item['stime'][idx] = item['stime'][idx] - len(match.group());
				item['etime'][idx] = item['etime'][idx] - len(match.group());
			else:
				idx = time_common.tmenu[it['scope']];
				item['stime'][idx] = item['stime'][idx] + len(match.group());
				item['etime'][idx] = item['etime'][idx] + len(match.group());
			item['scope'] = it['scope'];
			item['type'] = 'date';

	def merge_up_down_week(self,struct,it,mstr):
		cur_time = time.localtime();
		comp = re.compile(it['sreg']);
		match = comp.search(mstr);
		cur_week = cur_time[time_common.tmenu['week']];
		for item in struct['time_stc']:
			lstr = match.group() + item['str'];
			if lstr <> mstr: continue;
#			common.print_dic(item);
			item['str'] = mstr;
			if it['dir'] == '-':
				idx = time_common.tmenu[it['scope']];
				item['stime'][idx] = item['stime'][idx] - len(match.group()) * 7;
				item['etime'][idx] = item['etime'][idx] - len(match.group()) * 7;
			else:
				idx = time_common.tmenu[it['scope']];
				item['stime'][idx] = item['stime'][idx] + len(match.group()) * 7;
				item['etime'][idx] = item['etime'][idx] + len(match.group()) * 7;
			item['scope'] = it['scope'];
			item['type'] = 'date';

	def merge_up_down_week_region(self,struct,it,mstr):
		item = dict();
		item['str'] = mstr;

		cur_time = time.localtime();
		idx = time_common.tmenu[it['scope']];
		item['stime'] = time_common._list_copy(time_common._create_null_time(),cur_time,idx);
		item['etime'] = time_common._list_copy(time_common._create_null_time(),cur_time,idx);
		cur_week = cur_time[time_common.tmenu['week']];
		comp = re.compile(it['sreg']);
		match = comp.search(mstr);
		if it['dir'] == '-':
			idx = time_common.tmenu[it['scope']];
			item['stime'][idx] = item['stime'][idx] - (len(match.group()) - 1) * 7 - (cur_week + 1);
			item['etime'][idx] = item['etime'][idx] - len(match.group()) * 7 - (cur_week + 1);
		else:
			idx = time_common.tmenu[it['scope']];
			item['stime'][idx] = item['stime'][idx] + (len(match.group()) - 1) * 7 + (7 - cur_week);
			item['etime'][idx] = item['etime'][idx] + len(match.group()) * 7 + (7 - cur_week);
		item['scope'] = it['scope'];
		item['type'] = 'date';
		struct['time_stc'].append(item);

	def merge_up_down_num(self,struct,it,mstr):
		cur_time = time.localtime();
		idx = time_common.tmenu[it['scope']];
		comp = re.compile(it['sreg']);
		match = comp.search(mstr);
		for item in struct['time_stc']:
			lstr = match.group() + item['str'];
			if lstr <> mstr: continue;
			item['str'] = lstr;
			item['stime'] = time_common._list_copy(time_common._create_null_time(),cur_time,idx);
			item['etime'] = time_common._list_copy(time_common._create_null_time(),cur_time,idx);
			if it['dir'] == '-':
				item['stime'][idx] = item['stime'][idx] - int(item['num']);
				item['etime'][idx] = item['etime'][idx] - 1;
			else:
				item['stime'][idx] = item['stime'][idx] + 1;
				item['etime'][idx] = item['etime'][idx] + int(item['num']) + 1;
			del item['num'];
			item['scope'] = it['scope'];
			item['type'] = 'date';

	def merge_prev_after_num(self,struct,it,mstr):
		cur_time = time.localtime();
		idx = time_common.tmenu[it['scope']];
		comp = re.compile(it['sreg']);
		match = comp.search(mstr);
		is_enable_id = time_common.tmenu['enable'];
		for item in struct['time_stc']:
			lstr = item['str'] + match.group();
			if lstr <> mstr: continue;
			item['str'] = lstr;
			item['stime'] = time_common._list_copy(time_common._create_null_time(),cur_time,idx);
			item['etime'] = time_common._list_copy(time_common._create_null_time(),cur_time,idx);
			if it['dir'] == '-':
				item['stime'][idx] = item['stime'][idx] - int(item['num']);
				item['etime'][is_enable_id] = -1;
			else:
				item['stime'][idx] = item['stime'][idx] + int(item['num']) + 1;
				item['etime'][is_enable_id] = -1;
			del item['num'];
			item['scope'] = it['scope'];
			item['type'] = 'date';

	#移除无效的时间对象 通过最长匹配原则
	def remove_time_item(self,struct):
		left_list = list();
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
					left_list.append(item);
					break;
			if flg == 0:
				eid = eid - 1;
			if eid == 0:
				eid = slen;
				sid = sid + 1;
		struct['time_stc'] = left_list;
