#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json
import re
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import common
from common import MyException
REGS = {
	'f':'[1-9][0-9]{0,}[.][0-9]{0,}',
	'd':'[1-9][0-9]{0,}'
};

class LabelUnits():

	def __init__(self):
		self.data = None;

	def load_data(self,lfile):
		try:
			self.data = common.read_json(lfile);
		except MyException as e:
			print e.value;

	def paser_units(self,struct):
		try:
			inlist = struct['inlist'];
			keys = self.data.keys();
			for key in keys:
				item = self.data.get(key);
				for reg in item['reg']:
					tdic = dict();
					tdic['reg'] = reg;
					tdic['attr'] = item['attr'];
					match = self.__paser_unit(inlist,tdic);
					if match is None:
						continue;
					if not struct.has_key('match'):
						struct['match'] = list();
					struct['match'].append(match);
					break;
		except MyException as e:
			print e.value;

	def __paser_unit(self,inlist,reg_item):
		try:
			global REGS;
			regs = reg_item['reg'].split(' ');
			first = regs[0];
			second = regs[1];
			mdic = dict();
			regstr = '';
			if first[0] == '%':
				regstr = REGS[first[1:]];
			else:
				regstr = first;
			tcompile = re.compile(regstr);
			match = None;
			for tstr in inlist:
				match = tcompile.match(tstr);
				if match is None:
					continue;
				if match.end() - match.start() == len(tstr):
					mdic['match'] = tstr;
					break;
			if mdic.has_key('match'):
				idx = inlist.index(mdic['match']);
				if idx < len(inlist) - 1 and cmp(second,inlist[idx + 1]) == 0:
					del inlist[idx + 1];
					inlist[idx] = mdic['match'] + second;
					mdic['match'] = mdic['match'] + second;
					mdic['reg'] = reg_item['reg'];
					mdic['attr'] = reg_item['attr'];
					#common.print_dic(mdic);
					return mdic;
			return ;
		except MyException as e:
			raise e;


lu = LabelUnits();
lu.load_data('./units.txt');
struct = dict();
struct['inlist'] = [u'半',u'天'];
lu.paser_units(struct);
common.print_dic(struct);

