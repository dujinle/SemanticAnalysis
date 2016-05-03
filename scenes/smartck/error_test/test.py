#!/usr/bin/python

import sys,os
import traceback
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
from myexception import MyException
a = [];
def printa():
	try:
		print a[0]
	except Exception as e:
		raise MyException(sys.exc_info());
try:
	printa();
except Exception as e:
	print e;
