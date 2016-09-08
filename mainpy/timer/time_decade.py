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

#世纪类型时间处理[19世纪20年代 19世纪初期 ......]#
class TDecade(Base):

	def encode(self,struct):
		try:
			intext = struct['text'];
			step_id = struct['step_id'];
			input_str = intext[step_id:];
			mdic = self._get_match_reg(input_str);
			self._convert_front_date(struct);

			if mdic is None: return -1;
			if len(struct['intervals']) <= struct['my_inter_id']:
				struct['intervals'].append(time_common._creat_empty_interval());
			my_inter_id = struct['my_inter_id'];
			my_interval = struct['intervals'][my_inter_id];

			my_interval['str'] = my_interval['str'] + '_' + mdic['mstr'];
			if not my_interval.has_key('type'): my_interval['type'] = 'time_dt';
			self._convert_decade_day(my_interval,mdic);
			struct['step_id'] = step_id + len(mdic['mstr']);
			struct['prev_func'] = 'time_dt';
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

	def _convert_decade_day(self,my_interval,mdic):
		curtime = time.localtime();
		start = my_interval['start'];
		end = my_interval['end'];

		idx = time_common.tmenu['year'];
		if mdic['scope'] == 'decade':
			start[idx] = (int(mdic['num']) - 1) * 100;
			end[idx] = (int(mdic['num']) - 1) * 100;
		elif mdic['scope'] == 'years':
			if start[idx] == 0 and end[idx] == 0:
				start[idx] = end[idx] = 2000;
			start[idx] = start[idx] + int(mdic['num']);
			end[idx] = end[idx] + int(mdic['num']) + 10;
		elif mdic['scope'] == 'decade_desc':
			start[idx] = (int(mdic['num']) - 1) * 100 + mdic['interval'][0];
			end[idx] = (int(mdic['num']) - 1) * 100 + mdic['interval'][1];

	def _convert_front_date(self,struct):
		if struct.has_key('prev_func') and struct['prev_func'] == 'time_fot':
			left_tag = struct['tag'];
			if left_tag['scope'] <> 'decade': return None;
			if len(struct['intervals']) == 0:
				struct['intervals'].append(time_common._creat_empty_interval());
			curtime = time.localtime();
			idx = time_common.tmenu['year'];
			my_inter_id = struct['my_inter_id'];
			my_interval = struct['intervals'][my_inter_id];
			start = time_common._list_copy(curtime,my_interval['start'],idx);
			end = time_common._list_copy(curtime,my_interval['end'],idx);

			if left_tag['dir'] == '-':
				num = int(left_tag['num']);
				lf_year = num * 100;
				start[idx] = curtime[idx] - lf_year - 16;
				end[idx] = curtime[idx] - lf_year - 16;
			elif left_tag['dir'] == '+':
				num = int(left_tag['num']);
				lf_year = num * 100;
				start[idx] = curtime[idx] + lf_year - 16;
				end[idx] = curtime[idx] + lf_year - 16;
			my_interval['str'] = my_interval['str'] + left_tag['mstr'];
			if not my_interval.has_key('type'): my_interval['type'] = 'time_dt';
			time_common._make_sure_time(start,idx);
			time_common._make_sure_time(end,idx);
			struct['prev_func'] = 'time_dt';
			del struct['tag'];
