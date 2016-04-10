#!/usr/bin/python
#-*- coding:utf-8 -*-
from base import Base
class F(Base):
	def __init__(self):
		pass;

	def encode(self,struct):
		try:
			self.check_input(struct);
			inlist = struct['inlist'];
			keys = self.data.keys();
			for tt in inlist:
				if tt in keys:
					if not struct.has_key(tt):
						tdic = dict();
						tdic['type'] = 'F';
						tdic['value'] = self.data[tt];
						struct[tt] = tdic;
					else:
						raise Exception('the word has one more type' %tt);
		except Exception as e:
			raise e;
#m = F();
#m.load_data('../data/voice/F.txt');
#print m.data;
