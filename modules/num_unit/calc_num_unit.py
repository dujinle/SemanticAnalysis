#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,re,common
from myexception import MyException

class CalcNumUnit():
	def __init__(self):
		self.data = dict();

	def load_data(self,dfile):
		try:
			if dfile is None: return None;
			self.data = common.read_json(dfile);
		except Exception:
			raise MyException(sys.exc_info());

	def encode(self,struct):
		try:
			if not struct.has_key('nunit_dict'): struct['nunit_dict'] = dict();
			self._calc_num_unit(struct);
			self._inlist_reset(struct);
		except Exception:
			raise MyException(sys.exc_info());

	def _calc_num_unit(self,struct):
		nlist = struct['num_list'];
		ulist = struct['unit_list'];
		renum = list();
		reunit = list();
		for num in nlist:
			for unit in ulist:
				ustr = num['str'] + unit['str'];
				if struct['text'].find(ustr) <> -1:
					tdic = dict();
					tdic['type'] = 'NUNIT';
					tdic['stc'] = list();
					tdic['stc'].append(num);
					tdic['stc'].append(unit);
					renum.append(num);
					reunit.append(unit);
					struct['nunit_dict'][ustr] = tdic;
		for ri in renum:
			if ri in nlist: nlist.remove(ri);
		if len(struct['num_list']) == 0: del struct['num_list'];
		for ri in reunit:
			if ri in ulist: ulist.remove(ri);
		if len(struct['unit_list']) == 0: del struct['unit_list'];

	def _inlist_reset(self,struct):
		for key in struct['nunit_dict']:
			self._merge_some_words(struct,key);

	def _merge_some_words(self,struct,words):

		pid = struct['text'].find(words);
		wlist = list(u'|'.join(struct['inlist']));
		wid = tid = fid = 0;
		while True:
			if tid >= len(wlist): break;
			pw = wlist[tid];
			if wid == pid and fid == 0:
				fid = 1;
				if pid <> 0 and pw <> u'|': wlist.insert(tid,u'|');
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
