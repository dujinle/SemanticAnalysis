#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,re


comp = re.compile('((VOLUME))((BIG))((TIME)|(NUNIT)|(ALITTLE))');
match = comp.search('VOLUMEBIGALITTLE');
print match.group();
