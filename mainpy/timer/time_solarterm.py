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

#中国24节气的处理[立春,小寒......]#
class TSolarTerm(Base):
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
			if not my_interval.has_key('type'): my_interval['type'] = 'time_st';
			self._convert_solarterm_day(my_interval,mdic);
			struct['step_id'] = step_id + len(mdic['mstr']);
			if not struct.has_key('scope'): struct['scope'] = 'year';
			struct['prev_func'] = 'time_st';
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

	def _convert_solarterm_day(self,my_interval,mdic):
		curtime = time.localtime();
		order = mdic['order'];
		year_type = mdic['year_type'];

		year = curtime[time_common.tmenu['year']];
		if my_interval['start'][time_common.tmenu['year']] <> 0:
			year = my_interval['start'][time_common.tmenu['year']];
		(year,mon,day) = time_calendar.GetSolarTerm(year,order);

		idx = time_common.tmenu['year'];
		my_interval['start'][idx] = my_interval['end'][idx] = year;
		idx = time_common.tmenu['month'];
		my_interval['start'][idx] = my_interval['end'][idx] = mon;
		idx = time_common.tmenu['day'];
		my_interval['start'][idx] = my_interval['end'][idx] = day;

