#!/usr/bin/python
#-*- coding:utf-8 -*-
import Base
class M(Base):
	def encode(self,struct):
		try:
			self.check_input(struct);
			inlist = struct['inlist'];
			for st in inlist:
				if st in self.m:
					if not struct.has_key(st):
						tdic = dict();
						tdic['type'] = 'M';
						struct[st] = tdic;
						break;
					else:
						raise Exception('the word has one more type' %st);
		except Exception as e:
			raise e;
