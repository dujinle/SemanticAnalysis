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
			for key in keys:
				struct['time_stc'].extend(struct[key]);
				del struct[key];
			self.merge_time(struct);
			self.fill_time(struct);

			self.match_item(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def match_item(self,struct):
		for item in self.data:
			comp = re.compile(item['reg']);
			match = comp.search(struct['text']);
			if match is None: continue;
			if item['type'] == 'big':
				self.merge_big_time(struct,item,match.group());
			elif item['type'] == 'up_down_week':
				self.merge_up_down(struct,item,match.group());


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

	def merge_item(self,sitem,eitem):
		ret = time_common._is_merge_able(sitem,eitem);
		if ret is None: return None;
		tdic = dict(sitem);
		tdic.update(eitem);
		tdic['str'] = sitem['str'] + eitem['str'];
		tdic['stime'] = ret[0];
		tdic['etime'] = ret[1];
		if sitem.has_key('func') and sitem['func'] == 'add':
			tdic['func'] = 'add';
		return tdic;

	def fill_time(self,struct):
		cur_time = time.localtime();
		for item in struct['time_stc']:
			if item.has_key('type') and item['type'] == 'num': continue;
			if item.has_key('reg'): del item['reg'];
			if item.has_key('region'): del item['region'];
			st = item['stime'];
			et = item['etime'];
			#fill year
			idx = time_common.tmenu['year'];
			if st[idx] == 'null': st[idx] = cur_time[idx];
			if et[idx] == 'null': et[idx] = cur_time[idx];
			if item.has_key('scope') and item['scope'] == 'year': continue;
			#fill month
			idx = time_common.tmenu['month'];
			if st[idx] == 'null': st[idx] = cur_time[idx];
			if et[idx] == 'null': et[idx] = cur_time[idx];
			if item.has_key('scope') and item['scope'] == 'month': continue;
			#fill day
			idx = time_common.tmenu['day'];
			if st[idx] == 'null': st[idx] = cur_time[idx];
			if et[idx] == 'null': et[idx] = cur_time[idx];
			if item.has_key('scope') and item['scope'] == 'day': continue;
			if item.has_key('scope') and item['scope'] == 'week': continue;
			#fill hour
			idx = time_common.tmenu['hour'];
			if st[idx] == 'null': st[idx] = cur_time[idx];
			if et[idx] == 'null': et[idx] = cur_time[idx];
			if item.has_key('scope') and item['scope'] == 'hour': continue;
			#fill min
			idx = time_common.tmenu['min'];
			if st[idx] == 'null': st[idx] = cur_time[idx];
			if et[idx] == 'null': et[idx] = cur_time[idx];
			if item.has_key('scope') and item['scope'] == 'min': continue;
			#fill sec
			idx = time_common.tmenu['sec'];
			if st[idx] == 'null': st[idx] = cur_time[idx];
			if et[idx] == 'null': et[idx] = cur_time[idx];
			if item.has_key('scope') and item['scope'] == 'sec': continue;

	def merge_big_time(self,struct,it,mstr):
		cur_time = time.localtime();
		comp = re.compile(it['sreg']);
		match = comp.search(mstr);
		for item in struct['time_stc']:
			lstr = match.group() + item['str'];
			if lstr <> mstr: continue;
			item['str'] = mstr;
			if it['dir'] == '-':
				idx = time_common.tmenu[it['scope']];
				item['stime'][idx] = item['stime'][idx] - len(match.group());
				item['etime'][idx] = item['etime'][idx] - len(match.group());
			else:
				idx = time_common.tmenu[it['scope']];
				item['stime'][idx] = item['stime'][idx] + len(match.group());
				item['etime'][idx] = item['etime'][idx] + len(match.group());

	def merge_up_down(self,struct,mstr):
		cur_time = time.localtime();
		comp = re.compile(it['sreg']);
		match = comp.search(mstr);
		for item in struct['time_stc']:
			lstr = match.group() + item['str'];
			if lstr <> mstr: continue;
			item['str'] = mstr;
			if it['dir'] == '-':
				idx = time_common.tmenu[it['scope']];
				item['stime'][idx] = item['stime'][idx] - len(match.group()) * 7;
				item['etime'][idx] = item['etime'][idx] - len(match.group()) * 7;
			else:
				idx = time_common.tmenu[it['scope']];
				item['stime'][idx] = item['stime'][idx] + len(match.group()) * 7;
				item['etime'][idx] = item['etime'][idx] + len(match.group()) * 7;
