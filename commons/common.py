#!/usr/bin/python
#-*- coding:utf-8 -*-
import json

#global params
PASS = 1;

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
		raise Exception(all_test + ' load failed');

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
			self.body_json = json.loads(self.request.body);
		except Exception, e:
			raise e;
		return func(self, *args, **kwargs);
	return wrapper;
