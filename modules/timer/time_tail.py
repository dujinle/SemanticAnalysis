#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,re,time
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import common
import time_common,time_calendar
from myexception import MyException
from base import Base

#对时间tag进行最后的检测处理#
class TTail(Base):
	def encode(self,struct):
		try:
			if struct.has_key('prev_func') and struct['prev_func'] == 'time_mood':
				return 0;
			if struct.has_key('intervals') and len(struct['intervals']) == 0:
				return 0;
			intext = struct['text'];
			step_id = struct['step_id'];
			input_str = intext[step_id:];
			mdic = self._get_match_reg(input_str);
			my_inter_id = struct['my_inter_id'];
			my_interval = struct['intervals'][my_inter_id];
			curtime = time.localtime();
			start = my_interval['start'];
			end = my_interval['end'];
			if struct.has_key('uttag') and struct['prev_func'] == 'time_ut':
				left_tag = struct['uttag'];
				tid = time_common.tmenu[left_tag['scope']]
				if mdic is None:
					del struct['uttag'];
					my_interval.update(left_tag);
					my_interval['str'] = my_interval['str'] + left_tag['mstr'];
					struct['step_id'] = struct['step_id'] + 1;
					return 0;
				struct['step_id'] = struct['step_id'] + mdic['slen'];
				my_interval['str'] = my_interval['str'] + left_tag['mstr'];
				my_interval['str'] = my_interval['str'] + mdic['mstr'];
				for idx,i in enumerate(start):
					start[idx] = end[idx] = curtime[idx];
					if tid == idx: break;
				dnum = int(left_tag['num']);
				if mdic['dir'] == '-':
					end[tid] = start[tid] - dnum;
					start[0] = 'null';
				elif mdic['dir'] == '+':
					start[tid] = end[tid] + dnum;
					end[0] = 'null';
				my_interval['scope'] = struct['scope'];
				my_interval['num'] = dnum;
				del struct['uttag'];
				del struct['scope'];
			elif struct.has_key('intervals') and len(struct['intervals']) > 0:
				if not struct.has_key('prev_func'): return 0;
				tid = time_common.tmenu[struct['scope']];
				for idx,i in enumerate(end):
					if idx > tid: break;
					if start[idx] == 'null': start[idx] = curtime[idx];
					if end[idx] == 'null': end[idx] = curtime[idx];
				self._calc_interval(start,end,struct['prev_func'],tid);
				if not mdic is None:
					if mdic['dir'] == '-':
						end[tid] = start[tid];
						start[0] = 'null';
					elif mdic['dir'] == '+':
						start[tid] = end[tid];
						end[0] = 'null';
					struct['step_id'] = struct['step_id'] + mdic['slen'];
					my_interval['str'] = my_interval['str'] + mdic['mstr'];
				my_interval['scope'] = struct['scope'];
				del struct['scope'];
			time_common._make_sure_time(start,tid);
			time_common._make_sure_time(end,tid);
			self._calc_mid_value(my_interval);
			self._undo_strs(struct,my_interval);
			del struct['prev_func']
			return 0;
		except Exception as e: raise e;

	def _get_match_reg(self,inputstr):
		prev = u'[以之]*前';
		tail = u'[以之]*后';
		comp = re.compile(prev);
		match = comp.match(inputstr);
		if not match is None:
			mydic = dict();
			mydic['mstr'] = match.group(0);
			mydic['dir'] = '-';
			mydic['slen'] = len(mydic['mstr']);
			return mydic;
		comp = re.compile(tail);
		match = comp.match(inputstr);
		if not match is None:
			mydic = dict();
			mydic['mstr'] = match.group(0);
			mydic['dir'] = '+';
			mydic['slen'] = len(mydic['mstr']);
			return mydic;
		return None;

	def _calc_interval(self,start,end,prev_func,idx):
		if prev_func is None:
			return
		elif prev_func == 'time_tof':
			return
		elif prev_func == 'time_ut' or prev_func == 'time_bt' or prev_func == 'time_st':
			if start[idx] == end[idx]: end[idx] = end[idx] + 1;
		elif prev_func == 'time_wt' or prev_func == 'time_ft':
			if start[idx] == end[idx]: end[idx] = end[idx] + 1;

	def _calc_mid_value(self,my_interval):
		s_stamp = time_calendar.GetTimeStamp(my_interval['start']);
		if s_stamp == 0: return None;
		e_stamp = time_calendar.GetTimeStamp(my_interval['end']);
		if e_stamp == 0: return None;
		m_stamp = (s_stamp + e_stamp) / 2;
		my_interval['mvalue'] = m_stamp;

	def _undo_strs(self,struct,my_interval):
		sp_str = my_interval['str'].split('_');
		undo_str = '';
		for istr in sp_str:
			for key in struct['rep_dict']:
				if istr.find(key) <> -1:
					istr = istr.replace(key,struct['rep_dict'][key],1);
					struct['text'] = struct['text'].replace(key,struct['rep_dict'][key],1);
					struct['step_id'] = struct['step_id'] + len(struct['rep_dict'][key]) - len(key);
			if len(istr) > 0:
				undo_str = undo_str + '_' + istr;
		my_interval['str'] = undo_str;
		if struct.has_key('rep_dict'): del struct['rep_dict'];
