#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys
reload(sys);
sys.setdefaultencoding('utf-8');
import json

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
		raise Exception(__file__ + format(e));

def print_dic(struct):
	value = json.dumps(struct,indent = 4);#,ensure_ascii=False);
	print value;
