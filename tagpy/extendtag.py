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

def insert(d1data,indata,typec):
	try:
		if indata.has_key('reg') and indata.has_key('dir'):
			reg = data.get('reg');
			dirs = data.get('dir');
			for rdata in d1data:
				if reg == rdata['reg']:
					return;
			tdic = dict();
			tdic['type'] = typec;
			tdic.update(indata);
			x1data.append(tdic);
		else:
			raise ValueError('%s data has no key [dir | reg]' % typec);
	except Exception as e:
		raise e;

def remove(d1data,indata):
	try:
		for rdata in d1data:
			reg = rdata.get('reg');
			if reg.find(indata) != -1:
				del x1data[rdata];
				break;
	except Exception as e:
		raise e;

class X1(Base):

	def encode(self,struct):
		try:
			self.check_input(struct);
			x1data = self.data['X1'];
			match(x1data,struct,'X1');
		except Exception as e:
			raise e;

	def _add(self,data):
		try:
			x1data = self.data['X1'];
			insert(x1data,data,'X1');
		except Exception as e:
			raise e;

	def _del(self,data):
		try:
			x1data = self.data['X1'];
			remove(x1data,data);
		except Exception as e:
			raise e;

class F1(Base):

	def encode(self,struct):
		try:
			self.check_input(struct);
			f1data = self.data['F1'];
			match(f1data,struct,'F1');
		except Exception as e:
			raise e;

	def _add(self,data):
		try:
			x1data = self.data['F1'];
			insert(x1data,data,'F1');
		except Exception as e:
			raise e;

	def _del(self,data):
		try:
			x1data = self.data['F1'];
			remove(x1data,data);
		except Exception as e:
			raise e;

class M1(Base):

	def encode(self,struct):
		try:
			self.check_input(struct);
			m1data = self.data['M1'];
			match(m1data,struct,'M1');
		except Exception as e:
			raise e;

	def _add(self,data):
		try:
			x1data = self.data['M1'];
			insert(x1data,data,'M1');
		except Exception as e:
			raise e;

	def _del(self,data):
		try:
			x1data = self.data['M1'];
			remove(x1data,data);
		except Exception as e:
			raise e;
