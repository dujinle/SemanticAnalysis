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

class UT(Base):

	def encode(self,struct):
		try:
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
		tdic['type'] = 'time_ut';
		tdic['num'] = tmat.replace(key,'');
		struct['taglist'].append(tdic);
		struct['text'] = text.replace(tdic['value'],'UT',1);

	def _link_tag(self,struct):
		taglist = struct['taglist'];
		text = struct['text'];
		comp = re.compile('(UT){1,}');
		match = comp.finditer(text);
		idx = 0;
		for m in match:
			ut = m.group();
			num = len(ut) / 2;
			tdic = dict();
			tdic['times'] = list();
			tdic['type'] = 'time_ut';
			tdic['ntimes'] = num;
			first_idx = idx;
			while num > 0:
				tdic['times'].append(taglist[idx]);
				taglist[idx]['filter'] = 'true';
				num = num - 1;
				idx = idx + 1;
			taglist[first_idx] = tdic;
		idx = 0;
		while True:
			if idx >= len(taglist): break;
			tag = taglist[idx];
			if tag.has_key('filter') and tag['filter'] == 'true':
				del taglist[idx];
				idx = idx - 1;
			if tag.has_key('times'):
				if len(tag['times']) > 1:
					tag['attr'] = ['date'];
				if len(tag['times']) == 1:
					tag['attr'] = tag['times'][0]['attr'];
			idx = idx + 1;

	def _add(self,data):
		try:
			scope = data['scope'];
			attr = data['attr'];
			value = data['value'];
			reg = data['reg'];
			mdata = self.data;
			print data
			if value in mdata['keys']:
				for tt in mdata['regs']:
					if value in tt['same']:
						tt['scope'] = scope;
						tt['reg'] = reg;
						tt['attr'] = attr;
						break;
			else:
				mdata['keys'].append(value);
				flag = False;
				for tt in mdata['regs']:
					if scope == tt['scope']:
						tt['reg'] = reg;
						tt['attr'] = attr;
						tt['reg'] = reg;
						tt['same'].append(value);
						flag = True;
						break;
				if flag == False:
					tdic = dict();
					tdic['same'] = [value];
					tdic['scope'] = scope;
					tdic['attr'] = attr;
					tdic['reg'] = reg;
					mdata['regs'].append(tdic);
		except Exception as e:
			raise MyException(format(e));

	def _del(self,data):
		try:
			value = data['value'];
			mdata = self.data;
			if value in mdata['keys']:
				for tt in mdata['regs']:
					if value in tt['same']:
						tt['same'].remove(value);
						if len(tt['same']) == 0:
							mdata['regs'].remove(tt);
							mdata['keys'].remove(value);
						break;
		except Exception as e:
			raise MyException(format(e));


class UTE(Base):

	def encode(self,struct):
		try:
			intext = struct['text'];
			rlist = time_common._if_has_key(intext,self.data['keys']);
			regs = self.data['regs'];
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
		tdic['value'] = key;
		tdic['type'] = 'time_ute';
		self._insert_taglist(struct,tdic,tmat,key);
		ut_num = len(re.findall('UT',tmat));
		struct['text'] = text.replace(tmat,'UTE' * ut_num,1);

	def _insert_taglist(self,struct,tdic,tmat,key):
		taglist = struct['taglist'];
		text = struct['text'];
		idx = text.find(tmat);
		strs = text[:idx + len(tmat)];
		ut_num = len(re.findall('UT',strs));
		for tag in taglist:
			if tag['type'].find('time_ut') <> -1:
				time_num = tag['ntimes'];
				if ut_num > time_num:
					ut_num = ut_num - time_num;
				else:
					if tdic['position'] == 'left':
						tag['times'].insert(ut_num - 1,tdic);
					elif tdic['position'] == 'right':
						tag['times'].insert(ut_num,tdic);
					tag['type'] = 'time_ute';
					break;

	# 找到一个扩展的修饰时间词组 则可以进行区间的计算 为后续使用 #
	def _make_interval(self,struct):
		if not struct.has_key('taglist'): return None;
		taglist = struct['taglist'];
		for tag in taglist:
			if tag['type'] == 'time_ute':
				times = tag['times'];
				first_tag = times[0];
				if first_tag['type'] == 'time_ute':
					#如果 是 前UTUT 模式则不处理#
					if tag['ntimes'] > 1: del times[0];
					mytime = times[1];
					if first_tag['dir'] == '-':
						mytime['interval'] = [-1 * int(mytime['num']),0];
					elif first_tag['dir'] == '+':
						mytime['interval'] = [1,int(mytime['num'])];
				else:
					ut_num = tag['ntimes'];
					ute_tag = times[ut_num];
					mytime = times[ut_num - 1];
					if len(tag['attr']) == 1 and tag['attr'][0] == 'num':
						if ute_tag['dir'] == '-':
							mytime['interval'] = ['<',-1 * int(mytime['num'])];
						elif ute_tag['dir'] == '+':
							mytime['interval'] = [int(mytime['num']),'>'];
					elif len(tag['attr']) == 1 and tag['attr'][0] == 'date':
						if ute_tag['dir'] == '-':
							mytime['interval'] = ['<',int(mytime['num'])];
						elif ute_tag['dir'] == '+':
							mytime['interval'] = [int(mytime['num']),'>'];

#计算UT模式下的时间区间包括UTE模式
class CUTE(Base):
	def encode(self,struct):
		try:
			curtime = time.localtime();
			taglist = struct['taglist'];
			for tag in taglist:
				if tag['type'] == 'time_ute':
					if tag['ntimes'] == 1:
						if tag['attr'][0] == 'num':
							self._calc_ute_num_time(curtime,tag);
						elif tag['attr'][0] == 'date':
							self._calc_ute_date_time(curtime,tag);
					elif tag['ntimes'] > 1:
						self._calc_ute_date_times(curtime,tag);
				elif tag['type'] == 'time_ut':
					if tag['attr'][0] == 'date':
						self._calc_ut_date_times(curtime,tag);
		except MyException as e: raise e;

	def _calc_ute_num_time(self,curtime,tag):
		times = tag['times'];
		first_tag = times[0];
		if first_tag['type'] == 'time_ute': first_tag = times[1];
		start_time = list(curtime);
		end_time = list(curtime);
		idx = time_common.tmenu[first_tag['scope']];
		interval = first_tag['interval'];
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
		time_common._make_sure_time(start_time);
		time_common._make_sure_time(end_time);
		tag['interval'] = [start_time,end_time];

	def _calc_ute_date_time(self,curtime,tag):
		times = tag['times'];z
		first_tag = times[0];
		if first_tag['type'] == 'time_ute': first_tag = times[1];
		start_time = list(curtime);
		end_time = list(curtime);
		idx = time_common.tmenu[first_tag['scope']];
		interval = first_tag['interval'];
		if interval[0] == '<': start_time[0] = 'null';
		elif interval[0] <> '<': start_time[idx] = interval[0];
		if interval[1] == '>': end_time[0] = 'null';
		elif interval[1] <> '>': end_time[idx] = interval[1];

		start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
		end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);
		time_common._make_sure_time(start_time);
		time_common._make_sure_time(end_time);
		tag['interval'] = [start_time,end_time];

	def _calc_ute_date_times(self,curtime,tag):
		times = tag['times'];
		first_tag = times[0];
		if first_tag['type'] == 'time_ute': return None;
		start_time = list(curtime);
		end_time = list(curtime);
		tidx = 0;
		while True:
			if tidx >= len(times): break;
			tm = times[tidx];
			if tm['type'] == 'time_ute':
				if tm['dir'] == '-': start_time[0] = 'null';
				elif tm['dir'] == '+': end_time[0] = 'null';
			else:
				idx = time_common.tmenu[tm['scope']];
				start_time[idx] = int(tm['num']);
				end_time[idx] = int(tm['num']);

				start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
				end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);
			tidx = tidx + 1;
		tag['interval'] = [start_time,end_time];

	def _calc_ut_date_times(self,curtime,tag):
		times = tag['times'];
		start_time = list(curtime);
		end_time = list(curtime);
		tidx = 0;
		while True:
			if tidx >= len(times): break;
			tm = times[tidx];
			idx = time_common.tmenu[tm['scope']];
			start_time[idx] = int(tm['num']);
			end_time[idx] = int(tm['num']);

			start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
			end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);
			tidx = tidx + 1;
		tm = times[tidx - 1];
		idx = time_common.tmenu[tm['scope']];
		end_time[idx] = end_time[idx] + 1;
		time_common._make_sure_time(start_time);
		time_common._make_sure_time(end_time);
		tag['interval'] = [start_time,end_time];
