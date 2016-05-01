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

class TReplace(Base):
	def encode(self,struct):
		try:
			intext = struct['text'];
			step_id = struct['step_id'];
			input_str = intext[step_id:];
			if len(input_str) == 0: return 0;
			mdic = self._get_match_reg(input_str);
			if mdic is None: return 0;
			prev_str = intext[:step_id];
			if mdic['func'] == 'replace':
				input_str = input_str.replace(mdic['mstr'],mdic['value'],1);
			elif mdic['func'] == 'add':
				if input_str.find(mdic['value']) == -1:
					input_str = input_str.replace(mdic['mstr'],mdic['mstr'] + mdic['value'],1);
			elif mdic['func'] == 'time':
				pre_num = re.findall('[0-9]{1,}',input_str)[0];
				if int(pre_num) <= 12:
					num = str(int(pre_num) + 12);
					input_str = input_str.replace(pre_num,num,1);
			struct['text'] = prev_str + input_str;
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
