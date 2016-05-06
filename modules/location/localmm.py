#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os
reload(sys);
sys.setdefaultencoding('utf8');
#==============================================================
''' import commons modules '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
sys.path.append(os.path.join(base_path,'../'));
#==============================================================
from myexception import MyException

def readfile(dfile):
	fp = open(dfile,'r');
	if fp is None:
		raise MyException('open file ' + dfile + ' failed!');
	res = dict();
	while True:
		rline = fp.readline();
		if not rline: break;
		if len(rline) == 0 or rline[0] == '#': continue;
		rline = rline.strip('\n').strip('\r');
		res[rline.decode('utf-8')] = 1;
	fp.close();
	return res;

def edit_dist(str1,str2):
	x = len(str1) + 1;
	y = len(str2) + 1;
	mat = [[] for i in range(x)];
	del_num = in_num = sub_num = 0;


	for i in range(x):
		for j in range(y):
			mat[i].append(0);

	for i in range(x): mat[i][0] = i;
	for i in range(y): mat[0][i] = i;
	for i in range(x)[1:]:
		for j in range(y)[1:]:
			dels = mat[i-1][j] + 1;
			ins = mat[i][j-1] + 1;
			subs = mat[i-1][j-1] + 0;
			if str1[i - 1] <> str2[j - 1]:
				subs = subs + 1.0001;
			if dels < ins and dels < subs:
				del_num = del_num + 1;
				mat[i][j] = dels;
			elif ins < dels and ins < subs:
				in_num = in_num + 1;
				mat[i][j] = ins;
			elif subs < dels and subs < ins:
				sub_num = sub_num + 1;
				mat[i][j] = subs;
	print 'del',del_num;
	print 'ins',in_num;
	print 'sub',sub_num;
	print 'cost',mat[x-1][y-1];
	print 'rate',mat[x-1][y-1] * 1.0/(y-1);
	return mat[x-1][y-1] * 1.0/(y-1);
