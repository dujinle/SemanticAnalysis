#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
from base import Base
#============================================
''' import MyException module '''

base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
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
			raise MyException('%s data has no key [dir | value]' % typec);
	except Exception as e:
		raise MyException(format(e));

def remove(d1data,indata):
	try:
		data = indata.get('value');
		for rdata in d1data:
			reg = rdata.get('reg');
			idx = d1data.index(rdata);
			if reg.find(data) != -1:
				del d1data[idx];
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
			raise MyException(format(e));

	def _add(self,data):
		try:
			x1data = self.data['X1'];
			insert(x1data,data,'X1');
		except Exception as e:
			raise MyException(format(e));

	def _del(self,data):
		try:
			x1data = self.data['X1'];
			remove(x1data,data);
		except Exception as e:
			raise MyException(format(e));

class F1(Base):

	def encode(self,struct):
		try:
			self.check_input(struct);
			f1data = self.data['F1'];
			match(f1data,struct,'F1');
		except Exception as e:
			raise MyException(format(e));

	def _add(self,data):
		try:
			x1data = self.data['F1'];
			insert(x1data,data,'F1');
		except Exception as e:
			raise MyException(format(e));

	def _del(self,data):
		try:
			x1data = self.data['F1'];
			remove(x1data,data);
		except Exception as e:
			raise MyException(format(e));

class M1(Base):

	def encode(self,struct):
		try:
			self.check_input(struct);
			m1data = self.data['M1'];
			match(m1data,struct,'M1');
		except Exception as e:
			raise MyException(format(e));

	def _add(self,data):
		try:
			x1data = self.data['M1'];
			insert(x1data,data,'M1');
		except Exception as e:
			raise MyException(format(e));

	def _del(self,data):
		try:
			x1data = self.data['M1'];
			remove(x1data,data);
		except Exception as e:
			raise MyException(format(e));

class Z(Base):

	def encode(self,struct):
		return;
		try:
			self.check_input(struct);
			m1data = self.data['Z'];
			match(m1data,struct,'Z');
		except Exception as e:
			raise MyException(format(e));

	def _add(self,data):
		return ;
		try:
			x1data = self.data['Z'];
			insert(x1data,data,'Z');
		except Exception as e:
			raise MyException(format(e));

	def _del(self,data):
		return ;
		try:
			x1data = self.data['Z'];
			remove(x1data,data);
		except Exception as e:
			raise MyException(format(e));
