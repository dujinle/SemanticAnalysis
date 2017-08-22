#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,re,common
from myexception import MyException

from database import Connect

def _merge_some_words(struct,words,sid,flg = False):
	pid = struct['text'][sid:].find(words) + sid;
	if pid == -1: return -1;
	wlist = list(u'|'.join(struct['inlist']));
	wid = tid = fid = 0;
	while True:
		if tid >= len(wlist): break;
		pw = wlist[tid];
		if wid == pid and fid == 0:
			fid = 1;
			if pid <> 0 and pw <> u'|':
				wlist.insert(tid,u'|');
				tid = tid + 1;
			if pw <> u'|': wid = wid + 1;
		elif wid == pid + len(words):
			if pw <> u'|':
				wlist.insert(tid,u'|');
			break;
		elif wid > pid and wid < pid + len(words):
			if pw == u'|':
				del wlist[tid];
				continue;
			else:
				wid = wid + 1;
		elif pw <> u'|':
			wid = wid + 1;
		tid = tid + 1;
	struct['inlist'] = ''.join(wlist).split('|');
	return tid;

#合并相连的同属性词组
def _merge_cont_tag(struct,kname,data = None):
	pid = tid = 0;
	while True:
		if tid >= len(struct[kname]): break;
		lprep = struct[kname][tid];
		pprep = struct[kname][pid];
		tstr = pprep['str'] + lprep['str'];
		if (struct['text'].find(tstr) <> -1 and data is None) \
			or (struct['text'].find(tstr) <> -1 and data.has_key(tstr)):
			tdic = dict();
			tdic['str'] = tstr;
			if pprep.has_key('type'):
				tdic['type'] = pprep['type'];
				tdic['stype'] = pprep['stype'] + '_' + lprep['stype'];
			else:
				tdic['stype'] = pprep['stype'];
			struct[kname][pid] = tdic;
			del struct[kname][tid];
			continue;
		else:
			pid = tid;
		tid = tid + 1;

#按照出现的先后顺序排序
def _sort_by_apper(struct,kname):
	ilist = struct[kname];
	idx = 0;
	while True:
		if idx >= len(ilist): break;
		istr = ilist[idx]['str'];
		pid = idx + 1;
		while True:
			if pid >= len(ilist): break;
			pitem = ilist[pid];
			pstr = pitem['str'];
			pfid = struct['text'].find(pstr);
			ifid = struct['text'].find(istr);
			if pfid < ifid:
				ilist[pid] = ilist[idx];
				ilist[idx] = pitem;
			pid = pid + 1;
		idx = idx + 1;

def _link_split_words(struct,key):
	for dic in struct[key]:
		tstr = dic['str'];
		if len(tstr) > 1:
			_merge_some_words(struct,tstr,0,False);

def _filter_type(stype,etype):
	if stype[0] == '^':
		if etype == stype[1:]:
			return False;
		else:
			return True;
	elif stype <> '*' and stype <> etype:
		return False;
	return True;
