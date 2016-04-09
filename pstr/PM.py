#!/usr/bin/python
#-*- coding:utf-8 -*-
from base import Base
class PM(Base):
	def encode(self,struct):
		try:
			self.check_input(struct);
			inlist = struct['inlist'];
			reg = '';
			for st in inlist:
				if struct.has_key(st) and struct[st].has_key('type'):
					reg = reg + struct[st].get('type');
			regs = self.data['reg'];
			if reg in regs:
				struct['reg'] = reg;
		except Exception as e:
			raise e;
