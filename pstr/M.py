#!/usr/bin/python
#-*- coding:utf-8 -*-
from base import Base
class M(Base):
	def __init__(self):
		pass;

	def encode(self,struct):
		try:
			self.check_input(struct);
			inlist = struct['inlist'];
			mdata = self.data['M'];
			m1data = self.data["M!"];
			m1keys = m1data.keys();
			for st in inlist:
				if st in mdata:
					if not struct.has_key(st):
						tdic = dict();
						tdic['type'] = 'M';
						struct[st] = tdic;
					else:
						raise Exception('the word has one more type' %st);
				elif st in m1keys:
					if not struct.has_key(st):
						m1 = m1data[st];
						tdic = dict();
						tdic['type'] = 'M!';
						tdic['dir'] = m1['dir'];
						tdic['level'] = m1['level'];
						struct[st] = tdic;
					else:
						raise Exception('the word has one more type' %st);
		except Exception as e:
			raise Exception(__file__ + format(e));

#m = M();
#m.load_data('../data/voice/M.txt');
#print m.data;
