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
import common
import time_common
from myexception import MyException
from base import Base

class WT(Base):

	def encode(self,struct):
		try:
			curtime = time.localtime();
			intext = struct['text'];
			rlist = time_common._if_has_key(intext,self.data['keys']);
			regs = self.data['regs'];
			for key in rlist:
				self._match_reg(struct,key);
			self._link_tag(struct);
		except MyException as e: raise e;

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
		mykey = time_common._make_only_one(matchs);
		match = matchs[mykey];
		reg = tregs[mykey];

		tmat = match.group(0);
		tdic = dict();
		tdic.update(reg);
		tdic['value'] = tmat;
		tdic['type'] = 'time_wt';
		if tdic['vtype'] == 'num': tdic['num'] = tmat.replace(key,'');
		elif tdic['vtype'] == 'word': tdic['num'] = '7';
		elif tdic['vtype'] == 'words': tdic['num'] = '6';

		idx = time_common._find_idx(text,tmat,'null');
		struct['taglist'].insert(idx,tdic);
		struct['text'] = text.replace(tdic['value'],'WT',1);

	def _link_tag(self,struct):
		if not struct.has_key('taglist'): return None;
		taglist = struct['taglist'];
		text = struct['text'];
		comp = re.compile('(WT){1,}');
		match = comp.finditer(text);
		for m in match:
			wt = m.group();
			num = len(wt) / 2;
			tdic = dict();
			tdic['times'] = list();
			tdic['type'] = 'time_wt';
			tdic['ntimes'] = num;
			first_idx = wtidx = time_common._find_idx(text,wt,'WA');
			while num > 0:
				tdic['times'].append(taglist[wtidx]);
				del taglist[wtidx];
				num = num - 1;
			taglist.insert(first_idx,tdic);
			text = text.replace(wt,'WA',1);
			struct['text'] = struct['text'].replace(wt,'WT',1);
		idx = 0;
		while True:
			if idx >= len(taglist): break;
			tag = taglist[idx];
			if tag['type'].find('time_wt') <> -1:
				if tag.has_key('times'):
					if len(tag['times']) > 1:
						tag['attr'] = ['date'];
					if len(tag['times']) == 1:
						tag['attr'] = tag['times'][0]['attr'];
			idx = idx + 1;

class WTE(Base):

	def encode(self,struct):
		try:
			curtime = time.localtime();
			intext = struct['text'];
			rlist = time_common._if_has_key(intext,self.data['keys']);
			for key in rlist:
				self._match_reg(struct,key);
			self._make_interval(struct);
		except MyException as e: raise e;

	def _match_reg(self,struct,key):
		if not struct.has_key('taglist'): struct['taglist'] = list();
		text = struct['text'];
		regs = self.data['regs'];
		matchs = dict();
		tregs = dict();
		for reg in regs:
			regtr = '|'.join(reg['same']);
			if regtr.find(key) == -1: continue;
			myreg = reg['reg'].replace('K','(' + regtr + ')');
			comp = re.compile(myreg);
			match = comp.search(text);
			if match is None: continue;
			matchs[reg['reg']] = match;
			tregs[reg['reg']] = reg;
		if len(matchs) == 0: return None;
		mykey = time_common._make_only_one(matchs);
		match = matchs[mykey];
		reg = tregs[mykey];

		tmat = match.group(0);
		tdic = dict();
		tdic.update(reg);
		tdic['value'] = tmat.replace('WT','');
		tdic['type'] = 'time_wte';
		self._insert_taglist(struct,tdic,tmat,key);
		wt_num = len(re.findall('WT',tmat));
		struct['text'] = text.replace(tmat,'(WTE)' * wt_num,1);

	def _insert_taglist(self,struct,tdic,tmat,key):
		taglist = struct['taglist'];
		text = struct['text'];
		idx = time_common._find_idx(text,tmat,'null');
		if tmat.find('WT') <> -1:
			mytag = taglist[idx];
			if tdic['position'] == 'left':
				mytag['times'].insert(0,tdic);
				mytag['type'] = 'time_wte';
			elif tdic['position'] == 'right':
				mytag['times'].insert(1,tdic);
				mytag['type'] = 'time_wte';

	# 找到一个扩展的修饰时间词组 则可以进行区间的计算 为后续使用 #
	def _make_interval(self,struct):
		if not struct.has_key('taglist'): return None;
		taglist = struct['taglist'];
		curtime = time.localtime();
		for tag in taglist:
			if tag['type'] == 'time_wte':
				times = tag['times'];
				t_num = len(times);
				wt_num = tag['ntimes'];
				wte_num = t_num - wt_num;
				while wte_num > 0:
					for tt in times:
						if tt['type'] == 'time_wte':
							if tt['position'] == 'left':
								mytime = times[times.index(tt) + 1]
								if len(mytime['attr']) == 1 and mytime['attr'][0] == 'num':
									num = int( mytime['num']);
									if tt['dir'] == '-':
										mytime['interval'] = [num * -7,0];
									elif tt['dir'] == '+':
										mytime['interval'] = [0,num * 7];
								if len(mytime['attr']) == 1 and mytime['attr'][0] == 'date':
									num = int(mytime['num']);
									e_num = len(tt['value']);
									if tt['dir'] == '-':
										diff = 8 - num + curtime[6];
										if e_num > 1:
											diff = diff + (e_num - 1) * 7;
										if mytime['vtype'] == 'words':
											mytime['interval'] = [-1 * diff,-1 * diff + 2];
										else:
											mytime['interval'] = [-1 * diff,-1 * diff + 1];
									elif tt['dir'] == '+':
										diff = 7 - (curtime[6] + 1) + num;
										if e_num > 1:
											diff = diff + (e_num - 1) * 7;
										if mytime['vtype'] == 'words':
											mytime['interval'] = [diff,diff + 2];
										else:
											mytime['interval'] = [diff,diff + 1];
								mytime['scope'] = 'day';
							elif tt['position'] == 'right':
								mytime = times[times.index(tt) - 1];
								if len(mytime['attr']) == 1 and mytime['attr'][0] == 'num':
									num = mytime['num'];
									if tt['dir'] == '-':
										mytime['interval'] = ['<',num * -7];
									elif tt['dir'] == '+':
										mytime['interval'] = [num * 7,'>'];
								if len(mytime['attr']) == 1 and mytime['attr'][0] == 'date':
									num = int(mytime['num']);
									if mytime.has_key('interval'):
										if tt['dir'] == '-':
											mytime['interval'] = ['<',mytime['interval'][0]];
										elif tt['dir'] == '+':
											mytime['interval'] = [mytime['interval'][1],'>'];
									else:
										diff = num - curtime[6] - 1;
										if tt['dir'] == '-':
											mytime['interval'] = ['<',diff];
										elif tt['dir'] == '+':
											if mytime['vtype'] == 'words':
												mytime['interval'] = [diff + 2,'>'];
											else:
												mytime['interval'] = [diff + 1,'>'];
								mytime['scope'] = 'day';
							wte_num = wte_num - 1;
			elif tag['type'] == 'time_wt':
				mytime = tag['times'][0];
				if len(mytime['attr']) == 1 and mytime['attr'][0] == 'num':
					continue;
				if len(mytime['attr']) == 1 and mytime['attr'][0] == 'date':
					num = int(mytime['num']);
					diff = num - curtime[6] - 1;
					mytime['scope'] = 'day';
					if mytime['vtype'] == 'words':
						mytime['interval'] = [diff,diff + 2];
					else:
						mytime['interval'] = [diff,diff + 1];

#计算WT模式下的时间区间包括WTE模式
class CWTE(Base):
	def encode(self,struct):
		try:
			if not struct.has_key('taglist'): return None;
			curtime = time.localtime();
			taglist = struct['taglist'];
			for tag in taglist:
				if tag['type'] == 'time_wte':
					self._calc_wte_time(curtime,tag);
				elif tag['type'] == 'time_wt':
					self._calc_wt_time(curtime,tag);
		except MyException as e: raise e;

	def _calc_wte_time(self,curtime,tag):
		times = tag['times'];
		start_time = list(curtime);
		end_time = list(curtime);
		for tt in times:
			if tt['type'] == 'time_wt':
				if not tt.has_key('interval'): continue;
				idx = time_common.tmenu[tt['scope']];
				interval = tt['interval'];
				if interval[0] == '<':
					start_time[0] = 'null';
				elif interval[0] <> '<':
						start_time[idx] = start_time[idx] + interval[0];
				if interval[1] == '>':
					end_time[0] = 'null';
				elif interval[1] <> '>':
					end_time[idx] = end_time[idx] + interval[1];
				start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
				end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);
				time_common._make_sure_time(start_time,idx);
				time_common._make_sure_time(end_time,idx);
		tag['interval'] = [start_time,end_time];

	def _calc_wt_time(self,curtime,tag):
		times = tag['times'];
		start_time = list(curtime);
		end_time = list(curtime);
		for tt in times:
			if tt['type'] == 'time_wt':
				if not tt.has_key('interval'): continue;
				idx = time_common.tmenu[tt['scope']];
				interval = tt['interval'];
				start_time[idx] = interval[0] + start_time[idx];
				end_time[idx] = interval[1] + end_time[idx];
				start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
				end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);
				time_common._make_sure_time(start_time,idx);
				time_common._make_sure_time(end_time,idx);

		tag['interval'] = [start_time,end_time];

