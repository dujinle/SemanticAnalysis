#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,time,copy,re
reload(sys)
sys.setdefaultencoding('utf-8')
#=================================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#=================================================
import common
from myexception import MyException
from base import Base

#时间的状态 现在,过去,未来
class TMood(Base):
	def encode(self,struct):
		try:
			intext = struct['text'];
			step_id = struct['step_id'];
			input_str = intext[step_id:];
			mdic = self._get_match_reg(input_str);
			if mdic is None:return -1;
			if struct.has_key('mood'):
				struct['mood'].append(mdic);
			else:
				struct['mood'] = list();
				struct['mood'].append(mdic);
			struct['step_id'] = step_id + len(mdic['mstr']);
			struct['prev_func'] = 'time_mood';
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

	def _add(self,data):
		if not data.has_key('type'):
			raise MyException('not found type value');
		if not data.has_key('reg'):
			raise MyException('not found reg value');
		tdic['reg'] = data['reg'];
		tdic['type'] = data['dtype'];
		if data.has_key('status'):
			tdic['status'] = data['status'];
		elif data.has_key('level'):
			tdic['level'] = data['level'];
		self.data['regs'].append(data);

	def _del(self,data):
		if not data.has_key('reg'):
			raise MyException('not found reg value');
		istr = data['reg'];
		for item in self.data['regs']:
			if item['reg'] == istr:
				self.data['regs'].remove(item);
				break;
