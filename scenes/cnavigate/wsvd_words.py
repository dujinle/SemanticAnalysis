#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,common,re
from myexception import MyException

def encode(struct):
	try:
		text = _wsvd(struct);
		struct['stseg'] = text.split(' ');
	except Exception:
		raise MyException(sys.exc_info());

#重新对分词的结果进行整理 处理分错的问题 最长匹配原则
def _wsvd(struct):
	text = ' '.join(list(struct['text']));
	slen = len(struct['text']);
	sid = 0;eid = slen;
	while True:
		if sid > slen: break;
		istr = struct['text'][sid:eid];
		if struct['stc'].has_key(istr):
			ostr = ' '.join(list(istr));
			text = text.replace(ostr,istr);
			sid = eid;
			eid = slen;
		else:
			eid = eid - 1;
		if eid == 0:
			eid = slen;
			sid = sid + 1;
	return text;
