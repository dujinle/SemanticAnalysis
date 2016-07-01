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

class QT(Base):

	def encode(self,struct):
		try:
			curtime = time.localtime();
			intext = struct['text'];
			rlist = time_common._if_has_key(intext,self.data['keys']);
			regs = self.data['regs'];
			for key in rlist:
				self._match_reg(struct,key);
			self._link_tag(struct);
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
		tdic['value'] = tmat;
		tdic['type'] = 'time_qt';
		tdic['num'] = tmat.replace(key,'').replace(u'第','');
		idx = time_common._find_idx(text,tmat,'null')
		struct['taglist'].insert(idx,tdic);
		struct['text'] = text.replace(tdic['value'],'QT',1);

	def _link_tag(self,struct):
		if not struct.has_key('taglist'): return None;
		taglist = struct['taglist'];
		text = struct['text'];
		comp = re.compile('(QT){1,}');
		match = comp.finditer(text);
		for m in match:
			wt = m.group();
			num = len(wt) / 2;
			tdic = dict();
			tdic['times'] = list();
			tdic['type'] = 'time_qt';
			tdic['ntimes'] = num;
			first_idx = wtidx = time_common._find_idx(text,wt,'QA');
			while num > 0:
				tdic['times'].append(taglist[wtidx]);
				del taglist[wtidx];
				num = num - 1;
			taglist.insert(first_idx,tdic);
			text = text.replace(wt,'QA',1);
			struct['text'] = struct['text'].replace(wt,'QT',1);
		idx = 0;
		while True:
			if idx >= len(taglist): break;
			tag = taglist[idx];
			if tag['type'] == 'time_qt':
				if tag.has_key('times'):
					if len(tag['times']) > 1:
						tag['attr'] = ['date'];
					if len(tag['times']) == 1:
						tag['attr'] = tag['times'][0]['attr'];
			idx = idx + 1;

	def _make_interval(self,struct):
		if not struct.has_key('taglist'): return None;
		taglist = struct['taglist'];
		for tag in taglist:
			if tag['type'] == 'time_qt':
				attr = tag['attr'];
				times = tag['times'];
				if tag['ntimes'] > 1: continue;
				mytime = times[0];
				if mytime['type'] <> 'time_qt': continue;
				if len(attr) == 1 and attr[0] == 'date':
					if mytime['scope'] == 'jd':
						num = int(mytime['num']);
						start = (num - 1) * 3 + 2;
						end = start + 3;
						mytime['interval'] = [start,end];
						mytime['func'] = 'equal';
						mytime['scope'] = 'month';
					elif mytime['scope'] == 'xun':
						mytime['scope'] = 'day';
						mytime['func'] = 'equal';
					elif mytime['scope'] == 'bmon':
						mytime['scope'] = 'day';
						mytime['func'] = 'equal';
				elif len(attr) == 1 and attr[0] == 'num':
					continue;

#计算QT模式下的时间区间包括CQT模式
class CQT(Base):
	def encode(self,struct):
		try:
			if not struct.has_key('taglist'): return None;
			curtime = time.localtime();
			taglist = struct['taglist'];
			for tag in taglist:
				if tag['type'] == 'time_qt':
					self._calc_qt_time(curtime,tag);
		except MyException as e: raise e;

	def _calc_qt_time(self,curtime,tag):
		times = tag['times'];
		start_time = list(curtime);
		end_time = list(curtime);
		for tt in times:
			if tt['type'] == 'time_qt':
				if not tt.has_key('interval'): continue;
				idx = time_common.tmenu[tt['scope']];
				interval = tt['interval'];
				if tt['func'] == 'add':
					start_time[idx] = interval[0] + start_time[idx];
					end_time[idx] = interval[1] + end_time[idx];
					start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
					end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);
					time_common._make_sure_time(start_time,idx);
					time_common._make_sure_time(end_time,idx);
				elif tt['func'] == 'equal':
					start_time[idx] = interval[0];
					end_time[idx] = interval[1];

					start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
					end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);
					time_common._make_sure_time(start_time,idx);
					time_common._make_sure_time(end_time,idx);
			tag['interval'] = [start_time,end_time];
