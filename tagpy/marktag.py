#!/usr/bin/python
#-*- coding:utf-8 -*-
from base import Base

class X(Base):
	def __init__(self):
		pass;

	def encode(self,struct):
		try:
			self.check_input(struct);
			xdata = self.data['X'];
			self.__match_x(xdata,struct);
		except Exception as e:
			raise e;

	def __match_x(self,xdata,struct):
		inlist = struct['inlist'];
		taglist = struct['taglist'];
		keys = xdata.keys();
		for tt in inlist:
			for key in keys:
				data = xdata[key];
				if tt in data and tt in taglist:
					idx = taglist.index(tt);
					del taglist[idx];
					tdic = dict();
					tdic['type'] = 'X';
					tdic['dir'] = key;
					tdic['value'] = tt;
					taglist.insert(idx,tdic);

class M(Base):
	def __init__(self):
		pass;

	def encode(self,struct):
		try:
			self.check_input(struct);
			inlist = struct['inlist'];
			mdata = self.data['M'];
			taglist = struct['taglist'];
			for st in inlist:
				if st in mdata:
					tdic = dict();
					tdic['type'] = 'M';
					tdic['value'] = st;

					taglist.append(tdic);
				else:
					taglist.append(st);
		except Exception as e:
			raise Exception(__file__ + format(e));

class C(Base):
	def __init__(self):
		pass;

	def encode(self,struct):
		try:
			self.check_input(struct);
			inlist = struct['inlist'];
			keys = self.data.keys();
			taglist = struct['taglist'];
			#foreach inlist
			for tt in inlist:
				#foreach self.data.keys
				for key in keys:
					data = self.data[key];
					#if the dic self.data contain tt
					if tt in data and tt in taglist:
						idx = taglist.index(tt);
						del taglist[idx];
						tdic = dict();
						tdic['type'] = 'C';
						tdic['value'] = tt;
						tdic['level'] = key;
						taglist.insert(idx,tdic);
						break;
		except Exception as e:
			raise e;

class F(Base):
	def __init__(self):
		pass;

	def encode(self,struct):
		try:
			self.check_input(struct);
			inlist = struct['inlist'];
			taglist = struct['taglist'];
			keys = self.data.keys();
			for tt in inlist:
				if tt in keys and tt in taglist:
					idx = taglist.index(tt);
					del taglist[idx];
					data = self.data[tt];
					tdic = dict();
					tdic['type'] = 'F';
					tdic['value'] = tt;
					tdic.update(data);
					taglist.insert(idx,tdic);
		except Exception as e:
			raise e;
