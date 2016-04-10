#!/usr/bin/python
#-*- coding:utf-8 -*-
from base import Base
class Z(Base):
	def __init__(self):
		pass;

	def encode(self,struct):
		try:
			self.check_input(struct);
			keys = self.data.keys();
			values = self.data[keys[0]];
			for v in values:
				self.__match(keys[0],v,struct);
		except Exception as e:
			raise e;
	def __match(self,key,value,struct):
		strv = value.split(' ');
		inlist = struct['inlist'];
		first = strv[0];
		diclist = dict();
		if first in inlist:
			idx = inlist.index(first);
			reg = 'Z';
			tdic = dict();
			tdic['type'] = key;
			diclist[first] = tdic;
			sid = 1;
			while True:
				if sid >= len(strv) or idx >= len(inlist):
					break;
				if strv[sid] == inlist[idx]:
					tdic = dict();
					tdic['type'] = key;
					diclist[strv[sid]] = tdic;
					reg = reg + 'Z';
					sid = sid + 1;
					idx = idx + 1;
					continue;
				elif strv[sid] == '*' and idx < len(inlist):
					reg = reg + strv[sid];
					sid = sid + 1;
					idx = idx + 1;
					continue;
				else:
					tt = inlist[idx];
					if struct.has_key(tt):
						ddic = struct[tt];
						if ddic['type'] == strv[sid]:
							sid = sid + 1;
							idx = idx + 1;
							reg = reg + ddic['type'];
							continue;
				idx = idx + 1;
			if sid == len(strv):
				if struct.has_key('T'):
					raise Exception('the words has one more T [' + value + ' ' + struct['T'] + ']');
				struct['Z'] = dict();
				struct['Z']['value'] = value;
				struct['Z']['reg'] = reg;
				for kk in diclist:
					struct[kk] = diclist[kk];


#m = F();
#m.load_data('../data/voice/F.txt');
#print m.data;
