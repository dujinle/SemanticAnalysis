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
import time_common,hanzi2num
from myexception import MyException
from base import Base

class TReplace(Base):
	def encode(self,struct):
		try:
			if not struct.has_key('rep_dict'):
				struct['rep_dict'] = dict();
			self._str2num(struct);
			self._replace(struct);
			self._match_deal(struct);
			return 0;
		except MyException as e: raise e;

	def _str2num(self,struct):
		for reg in self.data['str2num']:
			step_id = struct['step_id'];
			input_str = struct['text'][step_id:];
			if len(input_str) == 0: break;

			regstr = reg['reg'];
			comp = re.compile(regstr);
			match = comp.search(input_str);
			if match is None: continue;
			mdic = dict(reg);
			mdic['mstr'] = match.group(0);

			prev_str = struct['text'][:step_id];
			(org_str,num_str) = self._hanzi2num(mdic);
			input_str = input_str.replace(org_str,num_str,1);
			struct['text'] = prev_str + input_str;
			struct['rep_dict'][num_str] = org_str;


	def _replace(self,struct):
		for reg in self.data['replace']:
			step_id = struct['step_id'];
			input_str = struct['text'][step_id:];
			if len(input_str) == 0: break;

			regstr = reg['reg'];
			comp = re.compile(regstr);
			match = comp.match(input_str);
			if match is None: continue;
			mdic = dict(reg);
			mdic['mstr'] = match.group(0);

			prev_str = struct['text'][:step_id];
			input_str = input_str.replace(mdic['mstr'],mdic['value'],1);
			struct['text'] = prev_str + input_str;
			struct['rep_dict'][mdic['value']] = mdic['mstr'];

	def _hanzi2num(self,mdic):
		sub_reg = mdic['sub_reg'];
		mystr = mdic['mstr'];
		comp = re.compile(sub_reg);
		match = comp.search(mystr);
		if match is None: return None;
		num_str = hanzi2num.cn2dig(match.group(0));
		return (match.group(0),str(num_str));

	def _match_deal(self,struct):
		for reg in self.data['regs']:
			step_id = struct['step_id'];
			input_str = struct['text'][step_id:];
			if len(input_str) == 0: break;

			regstr = reg['reg'];
			comp = re.compile(regstr);
			match = comp.match(input_str);
			if match is None: continue;
			mdic = dict(reg);
			mdic['mstr'] = match.group(0);

			prev_str = struct['text'][:step_id];
			if mdic['func'] == 'add':
				if input_str.find(mdic['value']) == -1:
					input_str = input_str.replace(mdic['mstr'],mdic['mstr'] + mdic['value'],1);
					struct['rep_dict'][mdic['mstr'] + mdic['value']] = mdic['mstr'];
			if mdic['func'] == 'time':
				pre_num = re.findall('[0-9]{1,}',input_str)[0];
				if int(pre_num) <= 12:
					num = str(int(pre_num) + 12);
					input_str = input_str.replace(pre_num,num,1);
					struct['rep_dict'][num] = str(pre_num);
			if mdic['func'] == 'hour_half':
				input_str = input_str.replace(mdic['value'],u'30分',1);
				struct['rep_dict'][u'30分'] = mdic['value'];
			struct['text'] = prev_str + input_str;

