#!/usr/bin/python
#-*- coding:utf-8 -*-
from base import Base
class M(Base):
	def encode(self,struct):
		try:
			self.check_input(struct);
			inlist = struct['inlist'];
			for st in inlist:
				if st in self.data:
					if not struct.has_key(st):
						tdic = dict();
						tdic['type'] = 'M';
						struct[st] = tdic;
						break;
					else:
						raise Exception('the word has one more type' %st);
		except Exception as e:
			raise Exception(__file__ + format(e));

#m = M();
#m.load_data('../data/voice/M.txt');
#print m.data;
