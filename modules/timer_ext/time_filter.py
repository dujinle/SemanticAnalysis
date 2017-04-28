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

#过滤一些带有时间的词但是又不表示时间概念
class TFilter(Base):
	def encode(self,struct):
		try:
			intext = struct['text'];
			step_id = struct['step_id'];
			input_str = intext[step_id:];
			mdic = self._get_match_reg(input_str);
			if mdic is None:return -1;
			if mdic['dir'] == '-':
				mdic['interval'] = [-1 * int(mdic['num']),0];
			elif mdic['dir'] == '+':
				mdic['interval'] = [1,int(mdic['num']) + 1];
			struct['step_id'] = step_id + len(mdic['mstr']);
			struct['prev_func'] = 'time_fot';
			struct['tag'] = mdic;
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
