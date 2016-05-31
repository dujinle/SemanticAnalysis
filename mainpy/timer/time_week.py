#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json
import re,time
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import common,config
from myexception import MyException
from base import Base

class TW(Base):
	def load_data(self,dfile):
		try:
			if dfile is None: return;
			self.data = common.read_json(dfile);
		except Exception as e:
			raise MyException(format(e));

	def encode(self,struct):
		try:
			curtime = time.localtime();
			intext = struct['text'];
			rlist = self._if_has_key(intext);
			regs = self.data['regs'];
			for key in rlist:
				self._match_reg(struct,key);
			taglist = struct['taglist'];

			for tag in taglist:
				if type(tag) == dict and tag['type'] == 'time_week':
					attr = tag['attr'];
					if len(attr) == 1 and attr[0] == 'date':
						num = int(tag['num']);
						diff = num - curtime[6] - 1;
						tag['interval'] = [diff,diff + 1];
						tag['scope'] = 'day';
						tag['func'] = 'add';

		except MyException as e: raise e;

	def _if_has_key(self,intext):
		keys = self.data['keys'];
		rlist = [x for x in intext for y in keys if x == y];
		return rlist;

	def _match_reg(self,struct,key):
		if not struct.has_key('taglist'): struct['taglist'] = list();
		text = struct['text'];
		regs = self.data['regs'];
		matchs = dict();
		tregs = dict();
		for reg in regs:
			regtr = '|'.join(reg['same']);
			myreg = reg['reg'].replace('K','(' + regtr + ')');
			comp = re.compile(myreg);
			match = comp.search(text);
			if match is None: continue;
			matchs[reg['reg']] = match;
			tregs[reg['reg']] = reg;
		if len(matchs) == 0: return None;
		mykey = self._make_only_one(matchs);
		match = matchs[mykey];
		reg = tregs[mykey];

		tmat = match.group(0);
		tdic = dict();
		tdic.update(reg);
		tdic['value'] = tmat;
		tdic['type'] = 'time_week';
		if tdic['vtype'] == 'num': tdic['num'] = tmat.replace(key,'');
		elif tdic['vtype'] == 'word': tdic['num'] = '7';
		struct['taglist'].append(tdic);
		struct['text'] = text.replace(tdic['value'],'TW',1);

	def _make_only_one(self,matchs):
		best_id = 0x20;
		mykey = None;
		for key in matchs.keys():
			match = matchs[key];
			if match.start() < best_id:
				best_id = match.start();
				mykey = key;
		return mykey;

class TWE(Base):
	def load_data(self,dfile):
		try:
			if dfile is None: return;
			self.data = common.read_json(dfile);
		except Exception as e:
			raise MyException(format(e));

	def encode(self,struct):
		try:
			curtime = time.localtime();
			intext = struct['text'];
			rlist = self._if_has_key(intext);
			for key in rlist:
				self._match_reg(struct,key);
			taglist = struct['taglist'];

			for tag in taglist:
				if type(tag) == dict and tag['type'] == 'time_weeke':
					attr = tag['attr'];
					if len(attr) == 1 and attr[0] == 'date':
						num = int(tag['num']);
						diff = 8 - num + curtime[6];
						if tag['dir'] == '-':
							tag['interval'] = [-1 * diff,-1 * diff + 1];
						elif tag['dir'] == '+':
							tag['interval'] = [diff,diff + 1];
						tag['scope'] = 'day';
					elif len(attr) == 1 and attr[0] == 'num':
						num = int(tag['num']);
						if tag.has_key('repeat') and tag['repeat'] == 'true':
							value = tag['value'];
							comp = re.compile(value[0]);
							repall = comp.findall(value);
							num = num * len(repall);
						num = int(tag['num']);
						diff = curtime[6] + 1;
						if tag['dir'] == '-':
							end = -1 * diff;
							start = end - num * 7;
							tag['interval'] = [start,end];
						elif tag['dir'] == '+':
							start = 8 - diff;
							end = start + 7 * num;
							tag['interval'] = [start,end];
		except MyException as e: raise e;

	def _if_has_key(self,intext):
		keys = self.data['keys'];
		rlist = [x for x in intext for y in keys if x == y];
		return rlist;

	def _match_reg(self,struct,key):
		if not struct.has_key('taglist'): struct['taglist'] = list();
		taglist = struct['taglist'];
		text = struct['text'];
		matchs = dict();
		tregs = dict();
		regs = self.data['regs'];
		for reg in regs:
			regtr = '|'.join(reg['same']);
			myreg = reg['reg'].replace('K','(' + regtr + ')');
			comp = re.compile(myreg);
			match = comp.search(text);
			if match is None: continue;
			matchs[reg['reg']] = match;
			tregs[reg['reg']] = reg;
		if len(matchs) == 0: return None;
		mykey = self._make_only_one(matchs);
		match = matchs[mykey];
		reg = tregs[mykey];

		tdic = dict();
		tdic.update(reg);
		tdic['type'] = 'time_weeke';
		tdic['num'] = '1';
		tdic['attr'] = ['num'];

		tmat = match.group(0);
		if tmat.find('TW') <> -1:
			tw_num = 0;
			idx = text.find(tmat);
			while idx >= 0:
				strs = text[:idx];
				if strs.rfind('TW') <> -1:
					idx = strs.rfind('TW');
					tw_num = tw_num + 1;
				else: break;
			twtag = taglist[tw_num];
			tdic['value'] = tmat.replace('TW',twtag['value']);
			tdic['num'] = twtag['num'];
			tdic['attr'] = twtag['attr'];
			struct['text'] = text.replace(tmat,'TWE',1);
			taglist[tw_num] = tdic;
		else:
			struct['text'] = text.replace(tmat,'TWE',1);
			tdic['value'] = tmat;
			taglist.append(tdic);

	def _make_only_one(self,matchs):
		best_id = 0x20;
		mykey = None;
		for key in matchs.keys():
			match = matchs[key];
			if match.start() < best_id:
				best_id = match.start();
				mykey = key;
		return mykey;
