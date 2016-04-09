#!/usr/bin/python
#-*- coding:utf-8 -*-
import Base
class F(Base):

	def encode(self,struct):
		try:
			self.check_input(struct);
			inlist = struct['inlist'];
			keys = self.data.keys();
			for tt in inlist:
				if tt in keys:
					if not struct.has_key('F'):
						struct['F'] = list();
					struct.append(self.data[tt]);
		except Exception as e:
			raise e;
