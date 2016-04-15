#!/usr/bin/python
#-*- coding:utf-8 -*-
from base import Base

class X(Base):

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

	def _add(self,data):
		try:
			xdata = self.data['X'];
			if data.has_key('dir') and data.has_key('value'):
				tdir = data.get('dir');
				value = data.get('value');
				if not xdata.has_key(tdir):
					xdata[tdir] = list();
				if value in xdata[tdir]:
					pass;
				else:
					xdata[tdir].append(value);
			else:
				raise ValueError('X: input data has no key [dir|value]');
		except Exception as e:
			raise e;

	def _del(self,data):
		try:
			xdata = self.data['X'];
			invalue = data.get('value');
			for key in xdata.keys():
				tdata = xdata[key];
				if invalue in tdata:
					idx = tdata.index(invalue);
					del tdata[idx];
					break;
		except Exception as e:
			raise e;

class M(Base):

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

	def _add(self,data):
		try:
			word = data.get('value');
			mdata = self.data['M'];
			if word in mdata:
				return;
			mdata.append(word);
		except Exception as e:
			raise e;

	def _del(self,data):
		try:
			mdata = self.data['M'];
			invalue = data.get('value');
			if invalue in mdata:
				idx = mdata.index(invalue);
				del mdata[idx];
				return;
		except Exception as e:
			raise e;

class C(Base):

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

	def _add(self,data):
		try:
			xdata = self.data;
			if data.has_key('dir') and data.has_key('value'):
				tdir = data.get('dir');
				value = data.get('value');
				if not xdata.has_key(tdir):
					xdata[tdir] = list();
				if value in xdata[tdir]:
					pass;
				else:
					xdata[tdir].append(value);
			else:
				raise ValueError('C: input data has no key [dir|value]');
		except Exception as e:
			raise e;
	def _del(self,data):
		try:
			xdata = self.data;
			invalue = data.get('value');
			for key in xdata.keys():
				tdata = xdata[key];
				if invalue in tdata:
					idx = tdata.index(invalue);
					del tdata[idx];
					break;
		except Exception as e:
			raise e;


class F(Base):

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
					tdic['dir'] = data['dir'];
					#tdic.update(data);
					taglist.insert(idx,tdic);
		except Exception as e:
			raise e;

	def _add(self,data):
		try:
			fdata = self.data;
			if data.has_key('dir') and data.has_key('value'):
				dirs = data.get('dir');
				value = data.get('value');
				if value in fdata.keys():
					return;
				tdic = dict();
				tdic['name'] = value;
				tdic['nickname'] = value;
				if dirs == u'有' or dirs == u'无':
					tdic['dimension'] = u'二元';
				else:
					tdic['dimension'] = u'一维';
				tdic['dir'] = dirs;
				fdata[value] = tdic;
		except Exception as e:
			raise e;
	def _del(self,data):
		try:
			fdata = self.data;
			fkeys = fdata.keys();
			invalue = data.get('value');
			if invalue in fkeys:
				del fdata[invalue];
		except Exception as e:
			raise e;
