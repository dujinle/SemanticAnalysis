#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,json

#global params
PASS = 1;
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(base_path);
#============================================
from myexception import MyException

def read_json(dfile):
	fid = open(dfile,'r');
	ondata = list();
	while True:
		line = fid.readline();
		if not line:
			break;
		line = line.strip('\n');
		if len(line) <= 0 or line[0] == '#':
			continue;
		ondata.append(line);
	all_test = ''.join(ondata);
	try:
		ojson = json.loads(all_test);
		return ojson;
	except Exception as e:
		raise MyException('load json file failed[' + dfile + ']');

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
				self.body_json = json.loads(self.request.body);
		except Exception, e:
			raise MyException(format(e));
		return func(self, *args, **kwargs);
	return wrapper;
