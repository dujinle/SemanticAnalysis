#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,time,copy
reload(sys)
sys.setdefaultencoding('utf-8')
#=================================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#=================================================
import common
from myexception import MyException
from base import Base

#时间的状态 现在,过去,未来
class TS(Base):

	def encode(self,struct):
		try:
			inlist = struct['inlist'];
			if not struct.has_key('taglist'): struct['taglist'] = list();
			taglist = struct['taglist'];
			for key in self.data.keys():
				if key in inlist:
					kdata = self.data[key];
					mydic = copy.deepcopy(kdata);
					mydic['value'] = key;
					taglist.append(mydic);
		except MyException as e: raise e;

	def _add(self,data):
		try:
			value = data.get('value');
			status = data.get('status');
			kdata = self.data;
			if value in kdata.keys():
				tdata = kdata[value];
				tdata['status'] = status;
			else:
				tdic = dict();
				tdic['type'] = 'mood_ts';
				tdic['status'] = status;
				kdata[value] = tdic;
		except Exception as e:
			raise MyException(format(e));

	def _del(self,data):
		try:
			value = data.get('value');
			kdata = self.data;
			if value in kdata.keys():
				del kdata[value];
		except Exception as e:
			raise MyException(format(e));

#时间的情态 偶尔,经常,总是
class TM(Base):

	def encode(self,struct):
		try:
			inlist = struct['inlist'];
			if not struct.has_key('taglist'): struct['taglist'] = list();
			taglist = struct['taglist'];
			for key in self.data.keys():
				if key in inlist:
					kdata = self.data[key];
					mydic = copy.deepcopy(kdata);
					mydic['value'] = key;
					taglist.append(mydic);
		except MyException as e: raise e;

	def _add(self,data):
		try:
			value = data.get('value');
			level = data.get('level');
			kdata = self.data;
			if value in kdata.keys():
				tdata = kdata[value];
				tdata['level'] = level;
			else:
				tdic = dict();
				tdic['type'] = 'mood_tm';
				tdic['level'] = level;
				kdata[value] = tdic;
		except Exception as e:
			raise MyException(format(e));

	def _del(self,data):
		try:
			value = data.get('value');
			kdata = self.data;
			if value in kdata.keys():
				del kdata[value];
		except Exception as e:
			raise MyException(format(e));

#事情的状态 事前,事中,事后
class AS(Base):

	def encode(self,struct):
		try:
			inlist = struct['inlist'];
			if not struct.has_key('taglist'): struct['taglist'] = list();
			taglist = struct['taglist'];
			for key in self.data.keys():
				if key in inlist:
					kdata = self.data[key];
					mydic = copy.deepcopy(kdata);
					mydic['value'] = key;
					taglist.append(mydic);
		except MyException as e: raise e;

	def _add(self,data):
		try:
			value = data.get('value');
			status = data.get('status');
			kdata = self.data;
			if value in kdata.keys():
				tdata = kdata[value];
				tdata['status'] = status;
			else:
				tdic = dict();
				tdic['type'] = 'mood_as';
				tdic['status'] = status;
				kdata[value] = tdic;
		except Exception as e:
			raise MyException(format(e));

	def _del(self,data):
		try:
			value = data.get('value');
			kdata = self.data;
			if value in kdata.keys():
				del kdata[value];
		except Exception as e:
			raise MyException(format(e));
