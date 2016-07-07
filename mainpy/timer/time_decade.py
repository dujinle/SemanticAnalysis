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

class DT(Base):
	def encode(self,struct):
		try:
			intext = struct['text'];
			rlist = time_common._if_has_key(intext,self.data['keys']);
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
			if not key in reg['same']: continue;
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
		idx = time_common._find_idx(text,tmat,'null');
		tdic = dict();
		tdic.update(reg);
		tdic['value'] = tmat;
		tdic['type'] = 'time_dt';
		tdic['num'] = tmat.replace(key,'');
		struct['taglist'].insert(idx,tdic);
		struct['text'] = text.replace(tdic['value'],'DT',1);

	def _link_tag(self,struct):
		if not struct.has_key('taglist'): return None;
		taglist = struct['taglist'];
		text = struct['text'];
		comp = re.compile('(DT){1,}');
		match = comp.finditer(text);
		for m in match:
			ut = m.group();
			num = len(ut) / 2;
			tdic = dict();
			tdic['times'] = list();
			tdic['type'] = 'time_dt';
			tdic['ntimes'] = num;
			first_idx = idx = time_common._find_idx(text,ut,'DA');
			while num > 0:
				tdic['times'].append(taglist[idx]);
				del taglist[idx];
				num = num - 1;
			text = text.replace(ut,'DA',1);
			struct['text'] = struct['text'].replace(ut,'DT',1);
			taglist.insert(first_idx,tdic);

		idx = 0;
		while True:
			if idx >= len(taglist): break;
			tag = taglist[idx];
			if tag['type'] == 'time_dt':
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

class DTE(Base):
	def encode(self,struct):
		try:
			intext = struct['text'];
			rlist = time_common._if_has_key(intext,self.data['keys']);
			regs = self.data['regs'];
			for key in rlist:
				self._match_reg(struct,key);
			#self._make_interval(struct);
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
		tdic['type'] = 'time_dte';
		self._insert_taglist(struct,tdic,tmat,key);
		ut_num = len(re.findall('DT',tmat));
		struct['text'] = text.replace(tmat,'DTE' * ut_num,1);

	def _insert_taglist(self,struct,tdic,tmat,key):
		taglist = struct['taglist'];
		text = struct['text'];

		first_idx = time_common._find_idx(text,tmat,'null');
		print first_idx
		tag = taglist[first_idx];
		tag['times'].append(tdic);
		tag['type'] = 'time_dte';

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

#计算DT模式下的时间区间包括DTE模式
class CDTE(Base):
	def encode(self,struct):
		try:
			if not struct.has_key('taglist'): return None;
			curtime = time.localtime();
			taglist = struct['taglist'];
			for tag in taglist:
				if tag['type'] == 'time_dte':
					if tag['ntimes'] == 1:
						self._calc_dte_date_time(curtime,tag);
					elif tag['ntimes'] > 1:
						self._calc_dte_date_times(curtime,tag);
				elif tag['type'] == 'time_dt':
					if tag['attr'][0] == 'date':
						self._calc_dt_date_times(curtime,tag);
		except MyException as e: raise e;

	def _calc_dte_date_time(self,curtime,tag):
		times = tag['times'];
		ftag = times[0];
		etag = times[1];
		start_time = list(curtime);
		end_time = list(curtime);
		idx = time_common.tmenu['year'];
		if etag.has_key('interval'):
			ftag['num'] = str((int(ftag['num']) - 1) * 100);
			start_time[idx] = int(ftag['num']) + etag['interval'][0];
			end_time[idx] = int(ftag['num']) + etag['interval'][1];
		elif etag.has_key('dir'):
			if ftag['scope'] == 'sj':
				ftag['num'] = str((int(ftag['num']) - 1) * 100);
				if etag['dir'] == '-':
					start_time[0] = 'null';
					end_time[idx] = int(ftag['num']);
				elif etag['dir'] == '+':
					end_time[0] = 'null';
					start_time[idx] = int(ftag['num']) + 100;
			elif ftag['scope'] == 'nd':
				ftag['num'] = '20' + ftag['num'];
				if etag['dir'] == '-':
					start_time[0] = 'null';
					end_time[idx] = int(ftag['num']);
				elif etag['dir'] == '+':
					end_time[0] = 'null';
					start_time[idx] = int(ftag['num']) + 10;

		start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
		end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);
		time_common._make_sure_time(start_time,idx);
		time_common._make_sure_time(end_time,idx);
		tag['interval'] = [start_time,end_time];

	def _calc_dte_date_times(self,curtime,tag):
		times = tag['times'];
		start_time = list(curtime);
		end_time = list(curtime);
		tidx = 0;
		while True:
			if tidx >= len(times): break;
			tm = times[tidx];
			if tm['type'] == 'time_dte':
				if tm['dir'] == '-': start_time[0] = 'null';
				elif tm['dir'] == '+':
					end_time[0] = 'null';
					start_time[idx] = start_time[idx] + 10;
			else:
				idx = time_common.tmenu['year'];
				if tm['scope'] == 'sj':
					start_time[idx] = (int(tm['num']) - 1) * 100;
					end_time[idx] = (int(tm['num']) - 1) * 100;
				elif tm['scope'] == 'nd':
					start_time[idx] = start_time[idx] + int(tm['num']);
					end_time[idx] = end_time[idx] + int(tm['num']);

				start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
				end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);
			tidx = tidx + 1;
		tag['interval'] = [start_time,end_time];

	def _calc_dt_date_times(self,curtime,tag):
		times = tag['times'];
		start_time = list(curtime);
		end_time = list(curtime);
		tidx = 0;
		while True:
			if tidx >= len(times): break;
			tm = times[tidx];
			if tm['scope'] == 'sj':
				tm['num'] = str((int(tm['num']) - 1) * 100);
			elif tm['scope'] == 'nd':
				tidx = tidx + 1;
				continue;
			idx = time_common.tmenu['year'];
			start_time[idx] = int(tm['num']);
			end_time[idx] = int(tm['num']);

			start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
			end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);
			tidx = tidx + 1;
		tm = times[tidx - 1];
		idx = time_common.tmenu['year'];
		if tm['scope'] == 'nd' and tidx == 1:
			tm['num'] = '20' + tm['num'];
			start_time[idx] = int(tm['num']);
			end_time[idx] = int(tm['num']) + 10;
		elif tm['scope'] == 'nd':
			start_time[idx] = start_time[idx] + int(tm['num']);
			end_time[idx] = end_time[idx] + int(tm['num']) + 10;
		elif tm['scope'] == 'sj':
			start_time[idx] = int(tm['num']);
			end_time[idx] = int(tm['num']) + 100;
		time_common._make_sure_time(start_time,idx);
		time_common._make_sure_time(end_time,idx);
		tag['interval'] = [start_time,end_time];
