#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
import re
#============================================
''' import MyException module '''

base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
from base import Base
import common

from myexception import MyException

class Nt(Base):

	def encode(self,struct):
		try:
			self.check_input(struct);
			xdata = self.data['Nt'];
			self.__label_num(struct);
			self.__match(xdata,struct);
		except Exception as e:
			raise MyException(format(e));

	def __match(self,xdata,struct):
		try:
			inlist = struct['inlist'];
			taglist = struct['taglist'];
			keys = xdata.keys();
			for key in keys:
				item = xdata.get(key);
				if key in inlist:
					idx = taglist.index(key);
					if idx == 0: continue;
					nt = taglist[idx - 1];
					if nt.has_key('type') and nt['type'] == 'Nt':
						del taglist[idx];
						if item.get('type') == 'bnum':
							nt['value'] = nt['value'] + key;
						else:
							nt['value'] = nt['value'];
						struct['Nt'] = dict();
						struct['Nt'].update(nt);
						struct['Nt']['type'] = item.get('type');
						break;
		except MyException as e:
			raise e;

	def __label_num(self,struct):
		try:
			inlist = struct['inlist'];
			taglist = struct['taglist'];
			for lstr in inlist:
				if self.__isnum(lstr):
					if lstr in taglist:
						idx = taglist.index(lstr);
						del taglist[idx];
						tdic = dict();
						tdic['value'] = lstr;
						tdic['type'] = 'Nt';
						taglist.insert(idx,tdic);
		except MyException as e:
			raise e;

	def __isnum(self,bbytes):
		try:
			step = 0;
			for b in bbytes:
				if b >= '0' and b <= '9':
					step = step + 1;
				elif b == '.' and step != 0:
					step = step + 1;
				else:
					return False;
			return True;
		except Exception as e:
			raise MyException(format(e));

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
				raise MyException('X: input data has no key [dir|value]');
		except Exception as e:
			raise MyException(format(e));

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
			raise MyException(format(e));

#nt = Nt();
#struct = dict();
#struct['inlist'] = [u'温度',u'上',u'调','30','%'];
#struct['taglist'] = [u'温度',u'上',u'调','30','%'];
#nt.load_data('../../data/temperature/Nt.txt');
#nt.encode(struct);
#common.print_dic(struct);
