#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,re


comp = re.compile('TIME.*(?:GO)(.*)');
match = comp.findall('TIMEGOHITGOLF');
for it in match:
	print it;
