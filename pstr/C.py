#!/usr/bin/python
#-*- coding:utf-8 -*-
import Base
class C(Base):

	def encode(self,struct):
		try:
			self.check_input(struct);
			inlist = struct['inlist'];
			keys = self.data.keys();
			#foreach inlist
			for tt in inlist:
				#foreach self.data.keys
				for key in keys:
					data = self.data[key];
					#if the dic self.data contain tt
					if tt in data:
						if struct.has_key(tt):
							raise Exception('the word %s has one more type' %tt);
						tdic = dict();
						tdic['type'] = 'C';
						tdic['c'] = key;
						struct[tt]= tdic;
						break;
		except Exception as e:
			raise e;
