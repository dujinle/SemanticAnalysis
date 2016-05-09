#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,re


comp = re.compile('(?:BA3)(.*)DEACLOCK');
match = comp.findall('BA3参ADD年会DEACLOCKDELETE:q');
for it in match:
	print it;
