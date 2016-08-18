#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,re,json
reload(sys);
sys.setdefaultencoding('utf-8');
import common,config
from myexception import MyException

class MT:
	def __init__(self):
		self.data = None;

	def init(self,dfile):
		try:
			self.data = common.read_json(dfile);
		except MyException as e: raise e

	def encode(self,struct):
		self._match_mt(struct,'MS');
		self._match_mt(struct,'MT');
		self._match_mt(struct,'ML');
		self._match_mt(struct,'MO');

	def _match_mt(self,struct,mtype):
		mdata = self.data[mtype];
		keys = mdata.keys();
		taglist = struct['music'];
		for key in keys:
			same = mdata[key]['same'];
			for tag in taglist:
				if type(tag) == dict: continue;
				if tag in same:
					idx = taglist.index(tag);
					tdic = dict();
					tdic['value'] = key;
					tdic['type'] = mtype;
					tdic['scope'] = mdata[key]['scope'];
					taglist[idx] = tdic;

	def _add(self,data):
		try:
			mtype = data['type'];
			mdata = data['value'];
			if not self.data.has_key(mtype):
				tdic = dict();
				tdic['same'] = [mdata];
				tdic['scope'] = 'mu';
				self.mt[mtype] = tdic;
			else:
				kdata = self.data[mtype];
				key = mdata[:mdata.find(':')];
				value = mdata[mdata.find(':') + 1:];

				if kdata.has_key(key):
					kdata[key]['same'].append(value);
				else:
					tdic = dict();
					tdic['scope'] = 'mu';
					if key == value:
						tdic['same'] = [value];
					else:
						tdic['same'] = [value,key];
					kdata[key] = tdic;
		except Exception as e:
			raise MyException(format(e));

	def _del(self,data):
		try:
			value = data['value'];
			keys = self.data.keys();
			for key in keys:
				kdata = self.data[key];
				for k1 in kdata.keys():
					if k1 == value:
						del kdata[k1];
						return None;
		except Exception as e:
			raise MyException(format(e));

	def _get(self,data):
		return self.data[data['type']];

	def write_file(self,dfile):
		try:
			if dfile is None: return None;
			os.rename(dfile,dfile + '.1');
			data = json.dumps(self.data,indent = 2,ensure_ascii = False);
			fd = open(dfile,'w');
			fd.write(data);
			fd.close();
		except Exception as e:
			raise MyException(format(e));
