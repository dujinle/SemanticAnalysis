#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,re
reload(sys);
sys.setdefaultencoding('utf-8');
import common,config
from myexception import MyException

class Flight:
	def __init__(self): self.flight = None;

	def init(self,dfile):
		try:
			self.flight = common.read_json(dfile);
		except MyException as e:
			raise e;

	def encode(self,struct):
		self._make_addr(struct);
		self._make_time(struct);
		self._make_flight(struct);
		self._make_way(struct);
		self._make_banci(struct);

	def _make_addr(self,struct):
		if not struct.has_key('locals'): return None;
		taglist = struct['locals'];
		mylocal = list();
		for tag in taglist:
			if type(tag) == dict and tag['type'] == 'locals':
				mylocal.append(tag);
			if len(mylocal) >= 2: break;
		if len(mylocal) <= 0: return None;
		tdic = dict();
		if len(mylocal) == 1:
			tdic['add_start'] = 'local';
			tdic['add_end'] = mylocal[0];
		else:
			tdic['add_start'] = mylocal[0];
			tdic['add_end'] = mylocal[1];
		del struct['locals'];
		struct['flight'] = tdic;

	def _make_time(self,struct):
		if not struct.has_key('taglist'): return None;
		taglist = struct['taglist'];
		mylocal = list();
		for tag in taglist:
			if type(tag) == dict and tag['type'].find('time') <> -1:
				mylocal.append(tag);
			if len(mylocal) >= 2: break;
		if not struct.has_key('flight'): return None;
		tdic = struct['flight'];
		if len(mylocal) == 1:
			tdic['time_start'] = common.list_join('-',mylocal[0]['interval'][0]);
			tdic['time_end'] = common.list_join('-',mylocal[0]['interval'][1]);
		elif len(mylocal) == 2:
			tdic['time_start'] = common.list_join('-',mylocal[0]['interval'][0]);
			tdic['time_end'] = common.list_join('-',mylocal[1]['interval'][1]);
		del struct['taglist'];

	def _make_flight(self,struct):
		if not struct.has_key('flight'): return None;
		for key in self.flight.keys():
			kdata = self.flight[key];
			for d in kdata:
				if d in struct['inlist']:
					struct['flight']['travel'] = {'key':key,'value':d};
					break;
			if struct['flight'].has_key('travel'): break;

	def _make_way(self,struct):
		if not struct.has_key('flight'): return None;
		way = self.flight['way'];
		for key in way.keys():
			kdata = way[key];
			for d in kdata:
				if d in struct['inlist']:
					struct['flight']['way'] = {'key':key,'value':d};
					break;
			if struct['flight'].has_key('way'): break;

	def _make_banci(self,struct):
		if not struct.has_key('flight'): return None;
		reg = '[a-zA-Z]{1,2}[0-9]{3,}';
		com = re.compile(reg);
		for strs in struct['inlist']:
			match = com.match(strs);
			if not match is None:
				struct['flight']['banci'] = match.group();
				break;
