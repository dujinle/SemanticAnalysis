#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
reload(sys);
sys.setdefaultencoding('utf-8');
import common,config,flight_com
from myexception import MyException
class AIR:
	def __init__(self):
		self.air = dict();

	def init(self,dfile):
		try:
			self.air.update(flight_com.readfile(dfile));
		except MyException as e:
			raise e;

	def encode(self,struct):
		self._paser_airline(struct);

	def _paser_airline(self,struct):
		inlist = struct['inlist'];
		if not struct.has_key('flight'): return None;
		flight = struct['flight'];
		for instr in inlist:
			if self.air.has_key(instr):
				tdic = dict();
				tdic['value'] = instr;
				tdic['scope'] = 'airline';
				flight['airline'] = tdic;
				break;
