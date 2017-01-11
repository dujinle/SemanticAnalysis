#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,json
from collections import OrderedDict

#global params
PASS = 1;
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(base_path);

#============================================
from myexception import MyException
from logger import *

def read_json(dfile):
	fid = open(dfile,'r');
	ondata = list();
	while True:
		line = fid.readline();
		if not line:
			break;
		line = line.replace('\r','').replace('\n','').replace('\t','');
		if len(line) <= 0 or line[0] == '#':
			continue;
		if line[0] == '>' or line[0] == '<':
			continue;
		ondata.append(line);
	all_test = ''.join(ondata);
	#print dfile,all_test
	try:
		ojson = json.loads(all_test,object_pairs_hook=OrderedDict);
		return ojson;
	except Exception as e:
		raise e;

def readfile(dfile):
	fp = open(dfile,'r');
	if fp is None: raise Exception('fp is null');
	res = dict();
	while True:
		rline = fp.readline();
		if not rline: break;
		if len(rline) == 0 or rline[0] == '#': continue;
		rline = rline.strip('\n').strip('\r');
		res[rline.decode('utf-8')] = 1;
	fp.close();
	return res;

def print_dic(struct):
	value = json.dumps(struct,indent = 4,ensure_ascii=False);
	print value;

def get_dicstr(struct):
	value = json.dumps(struct,indent = 4,ensure_ascii=False);
	return value;

def singleton(cls,*args,**kw):
	instances = {};
	def __singleton():
		if cls not in instances:
			instances[cls] = cls(*args,**kw);
		return instances[cls];
	return __singleton;

def json_loads_body(func):
	def wrapper(self, *args, **kwargs):
		try:
			if not self.request.body is None:
				logging.info(self.request.body);
				self.body_json = json.loads(self.request.body);
		except Exception, e:
			raise MyException(format(e));
		return func(self, *args, **kwargs);
	return wrapper;

def list_join(dicm,mlist):
	strs = '';
	for s in mlist:
		m = s;
		if type(s) == int:
			m = str(s);
		strs = strs + m + dicm;
	return strs[:-1];
