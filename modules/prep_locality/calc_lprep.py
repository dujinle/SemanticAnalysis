#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,re,common
from myexception import MyException

#merge the same type lprepmark
class CalcLPrep():
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
			self._merge_lprep_tag(struct);
		except Exception as e:
			raise MyException(sys.exc_info());

	def _merge_lprep_tag(self,struct):
		pid = tid = 0;

		while True:
			if tid >= len(struct['lprep']): break;
			lprep = struct['lprep'][tid];
			pprep = struct['lprep'][pid];
			tstr = pprep['str'] + lprep['str'];
			if struct['text'].find(tstr) <> -1:
				tdic = dict();
				tdic['str'] = tstr;
				tdic['type'] = 'LPREP';
				tdic['stype'] = pprep['stype'] + '_' + lprep['stype'];
				struct['lprep'][pid] = tdic;
				del struct['lprep'][tid];
				continue;
			else:
				pid = tid;
			tid = tid + 1;
		for lprep in struct['lprep']:
			self._merge_inlist(struct,lprep['str']);


	def _merge_inlist(self,struct,words):
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
