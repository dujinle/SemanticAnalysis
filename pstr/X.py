#!/usr/bin/python
#-*- coding:utf-8 -*-
from base import Base
class X(Base):
	def __init__(self):
		pass;

	def encode(self,struct):
		try:
			self.check_input(struct);
			inlist = struct['inlist'];
			xdata = self.data['X'];
			keys = xdata.keys();
			#foreach inlist
			for tt in inlist:
				#foreach self.data.values
				for key in keys:
					data = xdata[key];
					#if the dic self.data contain tt
					if tt in data:
						if struct.has_key(tt):
							raise Exception('the word %s has one more type' %tt);
						tdic = dict();
						tdic['type'] = 'X';
						tdic['dir'] = key;
						struct[tt]= tdic;
						break;
		except Exception as e:
			raise e;
#m = C();
#m.load_data('../data/voice/C.txt');
#print m.data;
