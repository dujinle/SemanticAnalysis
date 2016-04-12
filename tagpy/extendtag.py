#!/usr/bin/python
#-*- coding:utf-8 -*-
from base import Base

def match(d1data,struct,typec):
	inlist = struct['inlist'];
	taglist = struct['taglist'];
	tagstr = '';
	for tag in taglist:
		if type(tag) == dict and tag.has_key('type'):
			tagstr = tagstr + tag['type'];
		else:
			tagstr = tagstr + tag;
	for data in d1data:
		value = data.get('reg');
		strreg = value.replace(' ','');
		if tagstr.find(strreg) == -1:
			continue;
		for tt in value.split(' '):
			if tt in taglist:
				idx = taglist.index(tt);
				del taglist[idx];
				tdic = dict();
				tdic['type'] = typec;
				tdic['value'] = tt;
				taglist.insert(idx,tdic);
		dics = dict();
		dics.update(data);
		struct[typec] = dics;

class X1(Base):
	def __init__(self):
		pass;

	def encode(self,struct):
		try:
			self.check_input(struct);
			x1data = self.data['X1'];
			match(x1data,struct,'X1');
		except Exception as e:
			raise e;

class F1(Base):
	def __init__(self):
		pass;

	def encode(self,struct):
		try:
			self.check_input(struct);
			f1data = self.data['F1'];
			match(f1data,struct,'F1');
		except Exception as e:
			raise e;

class M1(Base):
	def __init__(self):
		pass;

	def encode(self,struct):
		try:
			self.check_input(struct);
			m1data = self.data['M1'];
			match(m1data,struct,'M1');
		except Exception as e:
			raise e;

