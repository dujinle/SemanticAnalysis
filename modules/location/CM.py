#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,re
reload(sys);
sys.setdefaultencoding('utf-8');
import common,config,localmm
from myexception import MyException

class CM:
	def __init__(self):
		self.reg = u'LD[0-9]{1,}米';
		self.dirs = dict();

	def init(self,fdir):
		try:
			dfile = fdir + '/CM.txt';
			self.dirs = common.read_json(dfile);
		except MyException as e: raise e

	def encode(self,struct):
		self._calc_them(struct);

	def _calc_them(self,struct):
		taglist = struct['locals'];
		strs = '';
		for tag in taglist:
			if type(tag) == dict and tag['type'].find('local') <> -1:
				strs = strs + 'L';
			else:
				strs = strs + tag;
		compass = self.dirs['compass'];
		for key in compass.keys():
			if strs.find(key) <> -1:
				sames = compass[key]['same'];
				match = self._match_cm(sames,strs);
				if match is None: continue;
				mt = match.group(0);
				idx = strs.find(mt);
				first = self._num_tag(strs,idx);
				idx = 0;
				while True:
					if first <= 0: break;
					tag = taglist[idx];
					if type(tag) == dict and tag['type'].find('local') <> -1:
						first = first - 1;
					idx = idx + 1;
				first = idx - 1;
				tdic = dict();
				tdic['type'] = 'local_cm';
				tdic['ad'] = taglist[first];
				tdic['dir'] = taglist[first + 1];
				tdic['dist'] = taglist[first + 2];
				taglist[first] = tdic;
				del taglist[first + 1];
				del taglist[first + 1];
				del taglist[first + 1];
				break;

	def _match_cm(self,sames,strs):
		for m in sames:
			mystr = strs;
			mystr = mystr.replace(m,'D',1);
			print m,mystr
			comp = re.compile(self.reg);
			match = comp.search(mystr);
			if not match is None: return match;
		return None;


	def _num_tag(self,strs,idx):
		mystr = strs[:idx];
		ms = re.findall('L',mystr);
		return len(ms);

