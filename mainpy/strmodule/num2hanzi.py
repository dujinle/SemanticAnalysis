#!/usr/bin/python
#-*- coding:utf-8 -*-

import math
units=["", "十", "百", "千", "万", "十", "百", "千", "亿", "十", "百", "千"];
nums=["零","一", "二", "三", "四", "五","六", "七", "八", "九"];

def translate(num):
	num=str(num);
	res='';
	for p in xrange(len(num)-1,-1,-1):
		r = int(int(num) / math.pow(10,p));
		res += nums[r%10] + units[p];
	for (i,j) in [('零十','零'), ('零百','零'), ('零千','零')]:
		res = res.replace(i,j);
	while res.find('零零')!=-1:
		res = res.replace('零零','零');
	for (i,j) in [('零万','万'),('零亿','亿')]:
		res = res.replace(i,j);
	res = res.replace('亿万','亿');
	if res.startswith('一十'):
		res = res[2:];
	if res.endswith('零'):
		res = res[:-2]

	return res;

print(translate('1023'));
