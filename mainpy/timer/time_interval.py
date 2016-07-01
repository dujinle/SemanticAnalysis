#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json
import re
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import common,config
from myexception import MyException
from base import Base
class UT(Base):

	def encode(self,struct):
		try:
			inlist = struct['inlist'];
			rlist = self.__check_unit(inlist);
			for key in rlist:
				item = self.data.get(key);
				if not item.has_key('same'): item['same'] = list();
				item['same'].append(key);
				self.__paser_unit(struct,item);
		except MyException as e: raise e;

	def __paser_unit(self,struct,reg_item):
		common.print_dic(reg_item);
		taglist = struct['taglist'];
		same = reg_item.get('same');
		myidx = -1;
		for value in same:
			try:
				myidx = taglist.index(value);
			except Exception as e:
				continue;
			if myidx == 0: return ;
			if myidx <> -1: break;
		if myidx == -1: return;

		mstr = taglist[myidx - 1];
		tcompile = re.compile(reg_item['reg']);
		match = tcompile.match(mstr);
		if match is None: return;
		if match.end() - match.start() == len(mstr):
			mdic = dict();
			mdic['num'] = mstr;
			mdic['type'] = 'num_time';
			mdic['scope'] = reg_item['type'];
			mdic['value'] = mstr + taglist[myidx];
			mdic['attr'] = reg_item['attr'];
			taglist[myidx - 1] = mdic;
			del taglist[myidx];

	def __check_unit(self,inlist):
		rlist = list();
		for x in inlist:
			for y in self.data.keys():
				if x == y: rlist.append(x);
				if self.data[y].has_key('same'):
					same = self.data[y]['same'];
					if x in same: rlist.append(y);
		return rlist;

	def _add(self,data):
		try:
			tdic = dict();
			tdic['reg'] = '[0-9]*[0-9]';
			tdic['type'] = data.get('ut_type');
			tdic['attr'] = data.get('attr');
			self.data[data['value']] = tdic;
		except Exception as e:
			raise MyException(format(e));

	def _del(self,data):
		try:
			if self.data.has_key(data['value']):
				del self.data[data['value']];
		except Exception as e:
			raise MyException(format(e));

class NT(Base):

	def encode(self,struct):
		try:
			inlist = struct.get('inlist');
			for dkey in self.data.keys():
				days = self.data.get(dkey);
				self._get_reg_tag(struct,days.get('notion'));
				self._get_reg_tag(struct,days.get('decorate'));
		except MyException as e: raise e;

	def _get_reg_tag(self,struct,data):
		inlist = struct.get('inlist');
		taglist = struct.get('taglist');
		for key in data.keys():
			for x in taglist:
				if type(x) == dict: continue;
				if x == key:
					idx = taglist.index(x);
					taglist[idx] = dict();
					taglist[idx]['value'] = key;
					taglist[idx]['type'] = 'ex_time';
					taglist[idx].update(data[key]);

	def _add(self,data):
		try:
			value = data['value'];
			scope = data['scope'];
			interval = data['interval'];
			ntype = data['nt_type'];
			func = data['func'];

			if type(interval) <> list: interval = json.loads(interval);

			tdata = self.data['day'];
			if not tdata.has_key(ntype): tdata[ntype] = dict();
			odata = tdata[ntype];

			tdic = dict();
			tdic['func'] = func;
			tdic['scope'] = scope;
			tdic['interval'] = interval;

			odata[value] = tdic;
		except Exception as e:
			raise MyException(format(e));

	def _del(self,data):
		try:
			for dt in self.data.keys():
				tdata = self.data[dt];
				for it in tdata.keys():
					idata = tdata[it];
					if idata.has_key(data['value']):
						del idata[data['value']];
						break;
		except Exception as e:
			raise MyException(format(e));

class CT(Base):

	def encode(self,struct):
		try:
			inlist = struct['inlist'];
			taglist = struct['taglist'];
			keys = self.data.keys();
			for key in inlist:
				if key in keys:
					self.__make_sure_interval(taglist,key);
		except MyException as e: raise e;

	def __make_sure_interval(self,taglist,key):
		kdata = self.data.get(key);
		strt = '';
		for tag in taglist:
			if type(tag) == dict and tag['type'].find('time') <> -1:
				strt = strt + 't';
			else: strt = strt + tag;

		reg = kdata['reg'];
		idx = strt.find(reg);
		if idx == -1: return None;
		if idx + 1 >= len(taglist): return None;
		taglist[idx + 1] = dict();
		taglist[idx + 1].update(kdata);
		taglist[idx + 1]['value'] = key;

class TF(Base):

	def __init__(self):
		self.data = None;

	def encode(self,struct):
		try:
			inlist = struct['inlist'];
			taglist = struct['taglist'];
			keys = self.data.keys();
			for key in inlist:
				if key in keys:
					self.__filter(taglist,key);
		except MyException as e: raise e;

	def __filter(self,taglist,key):
		kdata = self.data.get(key);
		strt = '';
		for tag in taglist:
			if type(tag) == dict and tag['type'].find('time') <> -1:
				strt = strt + 't';
			else: strt = strt + tag;
		reg = kdata['reg'];
		idx = strt.find(reg);
		if idx == -1: return None;
		if idx + 1 >= len(taglist): return None;
		if kdata['type'] == 'del':
			del taglist[idx + 1];
