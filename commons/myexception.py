#!/usr/bin/python
#-*- coding:utf-8 -*-
import traceback,sys
class MyException(Exception):

	def __init__(self,info):
		self.etype = info[0];
		self.msg = info[1];
		self.trace = traceback.extract_tb(info[2]);

	def __str__(self):
		infos = list();
		infos.append('Traceback (most recent call last):');
		for trace in self.trace:
			allinfo = '  File' + ' \"' + str(trace[0]) + '\",'\
					+ ' line ' + str(trace[1]) + ', in <' + str(trace[2]) + '>';
			infos.append(allinfo);
			allinfo = '    ' + str(trace[3]);
			infos.append(allinfo);
		stype = str(self.etype.__name__) + ': ' + str(self.msg);
		infos.append(stype)
		return '\n'.join(infos);
