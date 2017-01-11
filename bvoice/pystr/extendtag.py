#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
from base import Base
from myexception import MyException

def match(d1data,struct,typec):
	inlist = struct['inlist'];
	taglist = struct['taglist'];
	tagstr = '';
	for tag in taglist:
		if type(tag) == dict and tag.has_key('type'):
			tagstr = tagstr + tag['type'];
		else:
			tagstr = tagstr + tag;
	maxlen = 0;
	idx = step = 0;
	candidate = None;
	for data in d1data:
		value = data.get('reg');
		strreg = value.replace(' ','');
		if tagstr.find(strreg) != -1 and maxlen <= len(strreg):
			candidate = value;
			maxlen = len(strreg);
			step = idx;
		idx = idx + 1;
	if candidate is None: return ;
	data = d1data[step];
	for tt in candidate.split(' '):
		if tt in taglist:
			idx = taglist.index(tt);
			del taglist[idx];
			tdic = dict();
			tdic['type'] = typec;
			tdic['value'] = tt;
			taglist.insert(idx,tdic);
	if data.has_key('attr'):
		struct['attr'] = data['attr'];
	dics = dict();
	dics.update(data);
	struct[typec] = dics;

def insert(d1data,data,typec):
	try:
		if data.has_key('value') and data.has_key('dir'):
			reg = data.get('value');
			dirs = data.get('dir');
			for rdata in d1data:
				if reg == rdata['reg']:
					return;
			tdic = dict();
			tdic['type'] = typec;
			tdic['reg'] = reg;
			tdic['dir'] = dirs;
			d1data.append(tdic);
		else:
			raise MyException(sys.exc_info());
	except Exception as e:
		raise MyException(sys.exc_info());

def remove(d1data,indata):
	try:
		data = indata.get('value');
		for rdata in d1data:
			reg = rdata.get('reg');
			idx = d1data.index(rdata);
			if cmp(reg,data) == 0:
				del d1data[idx];
				break;
	except Exception as e:
		raise MyException(sys.exc_info());

class X1(Base):

	def encode(self,struct):
		try:
			x1data = self.data['X1'];
			match(x1data,struct,'X1');
		except Exception as e:
			raise MyException(sys.exc_info());

	def _add(self,data):
		try:
			x1data = self.data['X1'];
			insert(x1data,data,'X1');
		except Exception as e:
			raise MyException(sys.exc_info());

	def _del(self,data):
		try:
			x1data = self.data['X1'];
			remove(x1data,data);
		except Exception as e:
			raise MyException(sys.exc_info());

class F1(Base):

	def encode(self,struct):
		try:
			f1data = self.data['F1'];
			match(f1data,struct,'F1');
		except Exception as e:
			raise MyException(sys.exc_info());

	def _add(self,data):
		try:
			x1data = self.data['F1'];
			insert(x1data,data,'F1');
		except Exception as e:
			raise MyException(sys.exc_info());

	def _del(self,data):
		try:
			x1data = self.data['F1'];
			remove(x1data,data);
		except Exception as e:
			raise MyException(sys.exc_info());

class M1(Base):

	def encode(self,struct):
		try:
			m1data = self.data['M1'];
			match(m1data,struct,'M1');
		except Exception as e:
			raise MyException(sys.exc_info());

	def _add(self,data):
		try:
			x1data = self.data['M1'];
			insert(x1data,data,'M1');
		except Exception as e:
			raise MyException(sys.exc_info());

	def _del(self,data):
		try:
			x1data = self.data['M1'];
			remove(x1data,data);
		except Exception as e:
			raise MyException(sys.exc_info());

class Z(Base):

	def encode(self,struct):
		try:
			if not struct.has_key('text'):
				raise MyException(sys.exc_info());
			text = struct['text'];
			Zdata = self.data['Z'];
			for data in Zdata:
				if data['reg'] == text:
					struct['Z'] = data;
					break;
		except Exception as e:
			raise MyException(sys.exc_info());

	def _add(self,data):
		try:
			x1data = self.data['Z'];
			insert(x1data,data,'Z');
		except Exception as e:
			raise MyException(sys.exc_info());

	def _del(self,data):
		try:
			x1data = self.data['Z'];
			remove(x1data,data);
		except Exception as e:
			raise MyException(sys.exc_info());
