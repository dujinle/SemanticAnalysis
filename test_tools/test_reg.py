#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,re


comp = re.compile('[^ANEW]*OPENACLOCK');
match = comp.search('ANEWOPENACLOCK');
print match.group()
