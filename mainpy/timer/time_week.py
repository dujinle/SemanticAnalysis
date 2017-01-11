#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json
import re,time
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

#周日,周1......#
class TWeek(Base):
	def encode(self,struct):
		try:
			intext = struct['text'];
			step_id = struct['step_id'];
			input_str = intext[step_id:];
			mdic = self._get_match_reg(input_str);
			self._convert_front_date(struct);

			if mdic is None:return -1;
			if len(struct['intervals']) <= struct['my_inter_id']:
				struct['intervals'].append(time_common._creat_empty_interval());
			my_inter_id = struct['my_inter_id'];
			my_interval = struct['intervals'][my_inter_id];

			my_interval['str'] = my_interval['str'] + '_' +mdic['mstr'];
			if not my_interval.has_key('type'): my_interval['type'] = 'time_wt';
			self._convert_week_day(my_interval,mdic);
			struct['step_id'] = step_id + len(mdic['mstr']);
			struct['scope'] = 'day';
			struct['prev_func'] = 'time_wt';
			return 0;
		except MyException as e: raise e;

	def _get_match_reg(self,inputstr):
		for reg in self.data['regs']:
			regstr = reg['reg'];
			comp = re.compile(regstr);
			match = comp.match(inputstr);
			if not match is None:
				mydic = dict(reg);
				mydic['mstr'] = match.group(0);
				num = re.findall('\d+',mydic['mstr']);
				if len(num) > 0: mydic['num'] = num[0];
				return mydic;
		return None;

	def _convert_week_day(self,my_interval,mdic):
		curtime = time.localtime();
		today_week = curtime[6];
		idx = time_common.tmenu['day'];
		if mdic.has_key('num'):
			left_days = int(mdic['num']) - (today_week + 1);
			my_interval['start'][idx] = curtime[idx] + left_days;
			my_interval['end'][idx] = curtime[idx] + left_days;
		elif mdic.has_key('interval'):
			left_days = mdic['interval'][0] - (today_week + 1);
			my_interval['start'][idx] = curtime[idx] + left_days;
			left_days = mdic['interval'][1] - (today_week + 1);
			my_interval['end'][idx] = curtime[idx] + left_days;
		match = re.findall(u'[上下]{1,}',mdic['mstr']);
		if len(match) <> 0:
			numdays = len(match[0]) * 7;
			if match[0].find(u'上') <> -1:
				my_interval['start'][idx] = my_interval['start'][idx] - numdays;
				my_interval['end'][idx] = my_interval['end'][idx] - numdays;
			elif match[0].find(u'下') <> -1:
				my_interval['start'][idx] = my_interval['start'][idx] + numdays;
				my_interval['end'][idx] = my_interval['end'][idx] + numdays;

	def _convert_front_date(self,struct):
		if struct.has_key('prev_func') and struct['prev_func'] == 'time_fot':
			left_tag = struct['tag'];
			if left_tag['scope'] <> 'week': return None;
			if len(struct['intervals']) == 0:
				struct['intervals'].append(time_common._creat_empty_interval());
			curtime = time.localtime();
			idx = time_common.tmenu['day'];
			my_inter_id = struct['my_inter_id'];
			my_interval = struct['intervals'][my_inter_id];
			start = time_common._list_copy(curtime,my_interval['start'],idx);
			end = time_common._list_copy(curtime,my_interval['end'],idx);

			cur_week = curtime[6];
			if left_tag['dir'] == '-':
				num = int(left_tag['num']);
				start_day = num * 7 + cur_week;
				end_day = cur_week + 1;
				start[idx] = curtime[idx] - start_day;
				end[idx] = curtime[idx] - end_day;
			elif left_tag['dir'] == '+':
				num = int(left_tag['num']);
				start_day = 7 - cur_week;
				end_day = start_day + num * 7;
				start[idx] = curtime[idx] + start_day;
				end[idx] = curtime[idx] + end_day;
			my_interval['str'] = my_interval['str'] + left_tag['mstr'];
			if not my_interval.has_key('type'): my_interval['type'] = 'time_wt';
			time_common._make_sure_time(start,idx);
			time_common._make_sure_time(end,idx);
			struct['scope'] = 'day';
			struct['prev_func'] = 'time_wt';
			del struct['tag'];

