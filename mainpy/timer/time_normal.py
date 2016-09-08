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
import time_common
from myexception import MyException
from base import Base

#2016年3月8号17点18分20秒......#
class TNormal(Base):
	def encode(self,struct):
		try:
			intext = struct['text'];
			step_id = struct['step_id'];
			input_str = intext[step_id:];
			mdic = self._get_match_reg(input_str);

			if mdic is None: return -1;
			if len(struct['intervals']) <= struct['my_inter_id']:
				my_interval = time_common._creat_empty_interval();
				struct['intervals'].append(my_interval);
			self._convert_normal_date(struct,mdic);
			struct['step_id'] = step_id + len(mdic['mstr']);
			if not struct.has_key('scope'): struct['scope'] = mdic['scope'];
			struct['prev_func'] = 'time_ut';
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
				mydic['num'] = re.findall('\d+',mydic['mstr'])[0];
				return mydic;
		return None;

	def _convert_normal_date(self,struct,mdic):
		my_inter_id = struct['my_inter_id'];
		my_interval = struct['intervals'][my_inter_id];
		start = my_interval['start'];
		end = my_interval['end'];
		idx = time_common.tmenu[mdic['scope']];
		if mdic['scope'] == 'day' and mdic['mstr'].find(u'天') <> -1:
			struct['uttag'] = mdic;
			return None;
		start[idx] = int(mdic['num']);
		end[idx] = int(mdic['num']);
		my_interval['str'] = my_interval['str'] + '_' + mdic['mstr'];
		if not my_interval.has_key('type'): my_interval['type'] = 'time_ut';

#明天 昨晚 上午......#
class TBucket(Base):
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

			self._convert_bucket_date(my_interval,mdic);
			struct['step_id'] = step_id + len(mdic['mstr']);
			if not struct.has_key('scope'): struct['scope'] = mdic['scope']
			struct['prev_func'] = 'time_bt';
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
				return mydic;
		return None;

	def _convert_bucket_date(self,my_interval,mdic):
		start = my_interval['start'];
		end = my_interval['end'];
		idx = time_common.tmenu[mdic['scope']];
		my_interval['str'] = my_interval['str'] + '_' + mdic['mstr'];
		match = re.findall(u'大{1,}',mdic['mstr']);
		expend_day = 0;
		if len(match) > 0:
			dlen = len(match[0]) - 1;
			if mdic['interval'][0] < 0: expend_day = dlen * -1;
			elif mdic['interval'][0] > 0: expend_day = dlen;
		if mdic['func'] == 'equal':
			start[idx] = int(mdic['interval'][0]);
			end[idx] = int(mdic['interval'][1]);
		elif mdic['func'] == 'add':
			curtime = time.localtime();
			start[idx] = curtime[idx] + int(mdic['interval'][0]) + expend_day;
			end[idx] = curtime[idx] + int(mdic['interval'][0]) + expend_day;
		if not my_interval.has_key('type'): my_interval['type'] = 'time_nt';

	def _convert_front_date(self,struct):
		if struct.has_key('prev_func') and struct['prev_func'] == 'time_fot':
			left_tag = struct['tag'];
			if left_tag['scope'] == 'week' or left_tag['scope'] == 'decade': return None;
			if len(struct['intervals']) == 0:
				struct['intervals'].append(time_common._creat_empty_interval());
			curtime = time.localtime();
			my_inter_id = struct['my_inter_id'];
			my_interval = struct['intervals'][my_inter_id];
			if left_tag['scope'] == 'quarter':
				idx = time_common.tmenu['month'];
				start = time_common._list_copy(curtime,my_interval['start'],idx);
				end = time_common._list_copy(curtime,my_interval['end'],idx);
				cur_month = curtime[idx];
				cur_quarter = 0;
				if cur_month >= 2 and cur_month < 5: cur_quarter = 1;
				elif cur_month >= 5 and cur_month < 8: cur_quarter = 2;
				elif cur_month >= 8 and cur_month < 11: cur_quarter = 3;
				else: cur_quarter = 4;
				qnum = int(left_tag['num']);
				if left_tag['dir'] == '-':
					if cur_quarter - qnum <= 0: raise MyException('the quarter is less 0');
					start[idx] = 2 + (cur_quarter - 1) * 3 - qnum * 3;
					end[idx] = 2 + cur_quarter * 3 - qnum * 3;
				if left_tag['dir'] == '+':
					if cur_quarter - qnum > 4: raise MyException('the quarter is larger 4');
					start[idx] = 2 + (cur_quarter - 1) * 3 + qnum * 3;
					end[idx] = 2 + cur_quarter * 3 + qnum * 3;
				struct['scope'] = 'year';
			else:
				idx = time_common.tmenu[left_tag['scope']];
				start = time_common._list_copy(curtime,my_interval['start'],idx);
				end = time_common._list_copy(curtime,my_interval['end'],idx);
				start[idx] = curtime[idx] + left_tag['interval'][0];
				end[idx] = curtime[idx] + left_tag['interval'][1];
				struct['scope'] = 'year';
			my_interval['str'] = my_interval['str'] + left_tag['mstr'];
			if not my_interval.has_key('type'): my_interval['type'] = 'time_nt';
			time_common._make_sure_time(start,idx);
			time_common._make_sure_time(end,idx);
			struct['prev_func'] = 'time_bt';
			del struct['tag'];

	def _add(self,data):
		if not data.has_key('scope'):
			raise MyException('not found scope value');
		if not data.has_key('value'):
			raise MyException('not found value');
		if not data.has_key('func'):
			raise MyException('not found func value');
		if not data.has_key('interval'):
			raise MyException('not found interval list');
		tdic = dict();
		tdic['scope'] = data['scope'];
		tdic['interval'] = json.loads(data['interval']);
		tdic['func'] = data['func'];
		tdic['reg'] = data['value'];
		self.data['regs'].append(tdic);

	def _del(self,data):
		if not data.has_key('value'):
			raise MyException('not found reg value');
		istr = data['value'];
		for item in self.data['regs']:
			if item['reg'] == istr:
				self.data['regs'].remove(item);
				break;
