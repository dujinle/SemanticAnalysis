#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,copy
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

class NT(Base):

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
			comp = re.compile(regtr);
			match = comp.search(text);
			if match is None: continue;
			matchs[key] = match;
			tregs[key] = reg;
		if len(matchs) == 0: return None;
		mykey = time_common._make_only_one(matchs);
		match = matchs[mykey];
		reg = tregs[mykey];

		tmat = match.group(0);
		idx = time_common._find_idx(text,tmat,'null');
		tdic = copy.deepcopy(reg);
		tdic['value'] = tmat;
		tdic['type'] = 'time_nt';
		tdic['num'] = tmat.replace(key,'');
		struct['taglist'].insert(idx,tdic);
		struct['text'] = text.replace(tdic['value'],'NT',1);

	def _link_tag(self,struct):
		if not struct.has_key('taglist'): return None;
		taglist = struct['taglist'];
		text = struct['text'];
		comp = re.compile('(NT){1,}');
		match = comp.finditer(text);
		for m in match:
			nt = m.group();
			num = len(nt) / 2;
			tdic = dict();
			tdic['times'] = list();
			tdic['type'] = 'time_nt';
			tdic['ntimes'] = num;
			first_idx = ntidx = time_common._find_idx(text,nt,'NA');
			while num > 0:
				tdic['times'].append(taglist[ntidx]);
				del taglist[ntidx];
				num = num - 1;
			taglist.insert(first_idx,tdic);
			struct['text'] = struct['text'].replace(nt,'NT',1);
			text = text.replace(nt,'NA',1);
		idx = 0;
		while True:
			if idx >= len(taglist): break;
			tag = taglist[idx];
			if tag['type'] == 'time_nt':
				if tag.has_key('times'):
					tag['attr'] = ['date'];
			idx = idx + 1;

	def _add(self,data):
		try:
			scope = data['scope'];
			interval = json.loads(data['interval']);
			value = data['value'];
			func = data['func'];
			mdata = self.data;
			if value in mdata['keys']:
				for tt in mdata['regs']:
					if value in tt['same']:
						tt['scope'] = scope;
						tt['func'] = func;
						tt['interval'] = interval;
						break;
			else:
				mdata['keys'].append(value);
				tdic = dict();
				tdic['same'] = [value];
				tdic['scope'] = scope;
				tdic['func'] = func;
				tdic['interval'] = interval;
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


class NTE(Base):

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
		tdic['value'] = tmat.replace('NT','');
		tdic['type'] = 'time_nte';
		self._insert_taglist(struct,tdic,tmat,key);
		nt_num = len(re.findall('NT',tmat));
		struct['text'] = text.replace(tmat,('NTE') * nt_num,1);

	def _insert_taglist(self,struct,tdic,tmat,key):
		taglist = struct['taglist'];
		text = struct['text'];
		idx = text.find(tmat);
		strs = text[:idx + len(tmat)];
		nt_num = len(re.findall('NT',strs));
		for tag in taglist:
			if tag['type'].find('time_nt') <> -1:
				time_num = tag['ntimes'];
				if nt_num > time_num:
					nt_num = nt_num - time_num;
				else:
					if tdic['position'] == 'left':
						tag['times'].insert(nt_num - 1,tdic);
					elif tdic['position'] == 'right':
						tag['times'].insert(nt_num,tdic);
					tag['type'] = 'time_nte';
					break;

	# 找到一个扩展的修饰时间词组 则可以进行区间的计算 为后续使用 #
	def _make_interval(self,struct):
		if not struct.has_key('taglist'): return None;
		taglist = struct['taglist'];
		for tag in taglist:
			if tag['type'] == 'time_nte':
				times = tag['times'];
				t_num = len(times);
				nt_num = tag['ntimes'];
				nte_num = t_num - nt_num;
				while nte_num > 0:
					for tt in times:
						if tt['type'] == 'time_nte':
							#处理 『大大』NT的模型#
							if tt['position'] == 'left':
								if tt['dir'] == 'off':
									v_num = len(tt['value']);
									mytime = times[times.index(tt) + 1];
									interval = mytime['interval'];
									if int(interval[0]) > 0:
										mytime['interval'][0] = interval[0] + v_num;
										mytime['interval'][1] = interval[1] + v_num;
									elif int(interval[0]) < 0:
										mytime['interval'][0] = interval[0] - v_num;
										mytime['interval'][1] = interval[1] - v_num;
							elif tt['position'] == 'right':
								mytime = times[times.index(tt) - 1];
								if tt['dir'] == '-':
									mytime['interval'] = ['<',mytime['interval'][0]];
								elif tt['dir'] == '+':
									mytime['interval'] = [mytime['interval'][1],'>'];
							nte_num = nte_num - 1;

#计算nt模式下的时间区间包括ntE模式
class CNTE(Base):
	def encode(self,struct):
		try:
			if not struct.has_key('taglist'): return None;
			curtime = time.localtime();
			taglist = struct['taglist'];
			for tag in taglist:
				if tag['type'] == 'time_nte':
					if tag['ntimes'] == 1:
						self._calc_nte_date_time(curtime,tag);
					elif tag['ntimes'] > 1:
						self._calc_nte_date_times(curtime,tag);
				elif tag['type'] == 'time_nt':
					self._calc_nt_date_times(curtime,tag);
		except MyException as e: raise e;

	def _calc_nte_date_time(self,curtime,tag):
		times = tag['times'];
		first_tag = times[0];
		if first_tag['type'] == 'time_nte': first_tag = times[1];
		start_time = list(curtime);
		end_time = list(curtime);
		idx = time_common.tmenu[first_tag['scope']];
		interval = first_tag['interval'];
		if interval[0] == '<': start_time[0] = 'null';
		elif interval[0] <> '<':
			if first_tag['func'] == 'add':
				start_time[idx] = interval[0] + start_time[idx];
			elif first_tag['func'] == 'equal':
				start_time[idx] = interval[0];
		if interval[1] == '>': end_time[0] = 'null';
		elif interval[1] <> '>':
			if first_tag['func'] == 'add':
				end_time[idx] = interval[1] + end_time[idx];
			elif first_tag['func'] == 'equal':
				end_time[idx] = interval[1];

		start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
		end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);
		time_common._make_sure_time(start_time,idx);
		time_common._make_sure_time(end_time,idx);
		tag['interval'] = [start_time,end_time];

	def _calc_nte_date_times(self,curtime,tag):
		times = tag['times'];
		start_time = list(curtime);
		end_time = list(curtime);
		tidx = 0;
		while True:
			if tidx >= len(times): break;
			tm = times[tidx];
			if tm['type'] == 'time_nte':
				#计算 大大UT 模型 #
				if tm['position'] == 'left':
					ntm = times[tidx + 1];
					idx = time_common.tmenu[ntm['scope']];
					if ntm['interval'][0] > 0:
						start_time[idx] = start_time[idx] + ntm['interval'][0];
						end_time[idx] = end_time[idx] + ntm['interval'][0];
					elif ntm['interval'][0] < 0:
						start_time[idx] = start_time[idx] + ntm['interval'][1];
						end_time[idx] = end_time[idx] + ntm['interval'][1];
					start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
					end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);
					tidx = tidx + 1;
				elif tm['position'] == 'right':
					if tm['dir'] == '-': start_time[0] = 'null';
					elif tm['dir'] == '+': end_time[0] = 'null';
			else:
				idx = time_common.tmenu[tm['scope']];
				if tidx == len(times) - 1:
					self._filt_interval(start_time,end_time,tm,idx);
				elif tidx < len(times) - 1:
					self._fill_interval(start_time,end_time,tm,idx);
				start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
				end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);
			tidx = tidx + 1;
		tag['interval'] = [start_time,end_time];

	def _filt_interval(self,start_time,end_time,tm,idx):
		if tm['func'] == 'add':
			if tm['interval'][0] == '<':
				start_time[idx] = start_time[idx] + tm['interval'][1];
				end_time[idx] = end_time[idx] + tm['interval'][1];
			elif tm['interval'][1] == '>':
				start_time[idx] = start_time[idx] + tm['interval'][0];
				end_time[idx] = end_time[idx] + tm['interval'][0];
			else:
				start_time[idx] = start_time[idx] + tm['interval'][0];
				end_time[idx] = end_time[idx] + tm['interval'][1];
		elif tm['func'] == 'equal':
			if tm['interval'][0] == '<':
				start_time[idx] = tm['interval'][1];
				end_time[idx] = tm['interval'][1];
			elif tm['interval'][1] == '>':
				start_time[idx] = tm['interval'][0];
				end_time[idx] = tm['interval'][0];
			else:
				start_time[idx] = tm['interval'][0];
				end_time[idx] = tm['interval'][1];

	def _fill_interval(self,start_time,end_time,tm,idx):
		if tm['func'] == 'add':
			if tm['interval'][0] == '<':
				start_time[idx] = start_time[idx] + tm['interval'][1];
				end_time[idx] = end_time[idx] + tm['interval'][1];
			elif tm['interval'][1] == '>':
				start_time[idx] = start_time[idx] + tm['interval'][0];
				end_time[idx] = end_time[idx] + tm['interval'][0];
			elif tm['interval'][0] > 0:
				start_time[idx] = start_time[idx] + tm['interval'][0];
				end_time[idx] = end_time[idx] + tm['interval'][0];
			elif tm['interval'][0] < 0:
				start_time[idx] = start_time[idx] + tm['interval'][1];
				end_time[idx] = end_time[idx] + tm['interval'][1];
		elif tm['func'] == 'equal':
			if tm['interval'][0] == '<':
				start_time[idx] = tm['interval'][1];
				end_time[idx] = tm['interval'][1];
			elif tm['interval'][1] == '>':
				start_time[idx] = tm['interval'][0];
				end_time[idx] = tm['interval'][0];
			elif tm['interval'][0] > 0:
				start_time[idx] = tm['interval'][0];
				end_time[idx] = tm['interval'][0];
			elif tm['interval'][0] < 0:
				start_time[idx] = tm['interval'][1];
				end_time[idx] = tm['interval'][1];

	def _calc_nt_date_times(self,curtime,tag):
		times = tag['times'];
		start_time = list(curtime);
		end_time = list(curtime);
		tidx = dreal = 0;
		while True:
			if tidx >= len(times): break;
			tm = times[tidx];
			idx = time_common.tmenu[tm['scope']];
			if tidx == len(times) - 1:
				self._filt_interval(start_time,end_time,tm,idx);
			elif tidx < len(times) - 1:
				self._fill_interval(start_time,end_time,tm,idx);
			start_time[idx + 1:] = [0] * (len(start_time) - idx - 1);
			end_time[idx + 1:] = [0] * (len(end_time) - idx - 1);
			tidx = tidx + 1;
			time_common._make_sure_time(start_time,idx);
			time_common._make_sure_time(end_time,idx);
		tag['interval'] = [start_time,end_time];
