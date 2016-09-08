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

#传统国际节日处理春节,扫盲日......#
class TFestival(Base):
	def encode(self,struct):
		try:
			intext = struct['text'];
			step_id = struct['step_id'];
			input_str = intext[step_id:];
			mdic = self._get_match_reg(input_str);
			if mdic is None:return -1;
			if len(struct['intervals']) <= struct['my_inter_id']:
				struct['intervals'].append(time_common._creat_empty_interval());

			my_inter_id = struct['my_inter_id'];
			my_interval = struct['intervals'][my_inter_id];

			my_interval['str'] = my_interval['str'] + '_' + mdic['mstr'];
			if not my_interval.has_key('type'): my_interval['type'] = 'time_ft';
			self._convert_festival_day(my_interval,mdic);
			struct['step_id'] = step_id + len(mdic['mstr']);
			if not struct.has_key('scope'): struct['scope'] = 'year';
			struct['prev_func'] = 'time_ft';
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

	def _convert_festival_day(self,my_interval,mdic):
		curtime = time.localtime();
		mdate = mdic['date'];
		year = curtime[time_common.tmenu['year']];
		if my_interval['start'][time_common.tmenu['year']] <> 0:
			year = my_interval['start'][time_common.tmenu['year']];
		mon = int(mdate.split('/')[0]);
		day = int(mdate.split('/')[1]);
		#如果时间是农历时间则转换成阳历时间#
		if mdic['year_type'] == 'lunar':
			(year,mon,day) = time_calendar.ToSolarDate(year,mon,day);

		idx = time_common.tmenu['year'];
		my_interval['start'][idx] = my_interval['end'][idx] = year;
		idx = time_common.tmenu['month'];
		my_interval['start'][idx] = my_interval['end'][idx] = mon;
		idx = time_common.tmenu['day'];
		my_interval['start'][idx] = my_interval['end'][idx] = day;

	def _add(self,data):
		if not data.has_key('value'):
			raise MyException('not found reg value');
		if not data.has_key('date'):
			raise MyException('not found date value');
		if not data.has_key('year_type'):
			raise MyException('not found year type');
		tdic = dict();
		tdic['date'] = data['year_type'];
		tdic['reg'] = data['value'];
		tdic['year_type'] = data['year_type']
		self.data['regs'].append(tdic);

	def _del(self,data):
		if not data.has_key('value'):
			raise MyException('not found reg value');
		istr = data['value'];
		for item in self.data['regs']:
			if item['reg'] == istr:
				self.data['regs'].remove(item);
				break;

class TEFestival(Base):
	def encode(self,struct):
		try:
			intext = struct['text'];
			step_id = struct['step_id'];
			input_str = intext[step_id:];
			mdic = self._get_match_reg(input_str);
			if mdic is None: return -1;
			if len(struct['intervals']) <= struct['my_inter_id']:
				struct['intervals'].append(time_common._creat_empty_interval());

			my_inter_id = struct['my_inter_id'];
			my_interval = struct['intervals'][my_inter_id];

			my_interval['str'] = my_interval['str'] + '_' + mdic['mstr'];
			if not my_interval.has_key('type'): my_interval['type'] = 'time_ft';
			self._convert_efestival_day(my_interval,mdic);
			struct['step_id'] = step_id + len(mdic['mstr']);
			if not struct.has_key('scope'): struct['scope'] = 'year';
			struct['prev_func'] = 'time_ft';
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

	def _convert_efestival_day(self,my_interval,mdic):
		curtime = time.localtime();
		year = curtime[time_common.tmenu['year']];
		if my_interval['start'][time_common.tmenu['year']] <> 0:
			year = my_interval['start'][time_common.tmenu['year']];
		mon = mdic['month'];
		if mdic.has_key('week_type') and mdic['week_type'] == 'full':
			(year,mon,day) = time_calendar.GetSolarFullWeek(year,mon,mdic['week_idx'],mdic['week']);
		else:
			(year,mon,day) = time_calendar.GetSolarWeek(year,mon,mdic['week_idx'],mdic['week']);

		idx = time_common.tmenu['year'];
		my_interval['start'][idx] = my_interval['end'][idx] = year;
		idx = time_common.tmenu['month'];
		my_interval['start'][idx] = my_interval['end'][idx] = mon;
		idx = time_common.tmenu['day'];
		my_interval['start'][idx] = my_interval['end'][idx] = day;
