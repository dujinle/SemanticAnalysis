#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,random
from common import logging
from myexception import MyException


def _get_num_cks(struct):
	num = 0;
	for s in struct['inlist']:
		if data['num'].has_key(s):
			num = int(data['num'][s]);
			return num;
	return num;


def _get_random_id(total):
	ret = random.randint(0,total);
	if ret == total:
		ret = ret - 1;
	return ret;

def _set_msg(struct,datamsg,*args):
	msg_id = _get_random_id(len(datamsg));
	if len(args) <= 0:
		struct['result']['msg'] = datamsg[msg_id];
	else:
		struct['result']['msg'] = (datamsg[msg_id] %args);
