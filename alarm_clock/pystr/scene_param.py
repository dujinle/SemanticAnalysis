#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,copy
import re,time,random
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import common,pgsql
import math,datetime
from common import logging
from myexception import MyException
dfile = os.path.join(base_path,'../tdata/scene_param.txt')
data = common.read_json(dfile);

def _if_exist(struct,super_b):
	if struct.has_key('ck_name'):
		ck_name = struct['ck_name'];
		if super_b.clocks.has_key(ck_name): return True;
	if struct.has_key('ck_time'):
		ck_time = struct['ck_time']['time'];
		if super_b.clocks.has_key(ck_time): return True;
	return False;

def _find_time(struct):
	if struct.has_key('intervals') and len(struct['intervals']) > 0:
		myinterval = struct['intervals'][0]
		times = myinterval['start'];
		if myinterval['scope'] == 'day' or myinterval['scope'] == 'hour'\
			or myinterval['scope'] == 'min' or myinterval['scope'] == 'sec':
			tdic = dict();
			tdic['date'] = str(times[0]) + '/' + str(times[1]) + '/' + str(times[2]);
			struct['ck_date'] = tdic;
		if times[3] <> 'null':
			tdic = dict();
			if times[4] == 'null':
				tdic['time'] = str(times[3]) + ':0';
			else:
				tdic['time'] = str(times[3]) + ':' + str(times[4]);
			tdic['str'] = myinterval['str'];
			struct['ck_time'] = tdic;
		elif myinterval.has_key('mvalue'):
			times = time.localtime(myinterval['mvalue']);
			tdic = dict();
			tdic['time'] = str(times[3]) + ':' + str(times[4]);
			tdic['str'] = myinterval['str'];
			struct['ck_time'] = tdic;

def _calc_able(struct):
	if struct.has_key('ck_date'):
		date = struct['ck_date'];
		tdic = dict();
		dates = date['date'].split('/');
		dat = datetime.date(int(dates[0]),int(dates[1]),int(dates[2]));
		week = dat.weekday();
		able = math.pow(2,week);
		tdic['type'] = 'week';
		tdic['repeat'] = 'repeat';
		tdic['able'] = able;
		del struct['ck_date'];
		struct['ck_able'] = tdic;

def _save_tag(super_b):
	try:
		mydic = dict();
		mydic['value'] = super_b.myclock['time'];
		mydic['type'] = 'time';
		mydic['name'] = super_b.myclock['name'];
		sql = 'insert into mytags (tag,creat_time) values (' \
			+ '\'' + json.dumps(mydic) + '\',' \
			+ '\'now\'' + ')';
		cur = pgsql.pg_cursor(super_b.p_conn);
		pgsql.pg_query(cur,sql,None);
		pgsql.pg_commit(super_b.p_conn);
		pgsql.pg_close_cursor(cur);
	except Exception as e:
		raise e;

def _find_ck_name(struct,stag):
	ttag = struct['ttag'];
	if ttag.find(stag) <> -1:
		idx = len(struct['clocks']) - 1;
		tag = False;
		name = '';
		while True:
			if idx < 0: break;
			cl = struct['clocks'][idx];
			if tag == True:
				if isinstance(cl,dict) and idx == 0: break;
				if isinstance(cl,dict) == False and cl == u'的':
					pass;
				elif isinstance(cl,dict) == False:
					name = cl + name;
				else:
					cn = struct['clocks'][idx - 1];
					if isinstance(cn,dict): break;
					else: name = cl['mystr'] + name;
			if isinstance(cl,dict) and cl['type'] == stag:
				tag = True;
				if idx == 0: break;
				cn = struct['clocks'][idx - 1];
				if isinstance(cn,dict): break;
				if cn <> u'的': break;
			idx = idx - 1;
		return name;
	return None;

#get the name info after the label
def _find_tag_name(struct,tdic):
	name = None;
	idx = ftag = 0;
	first_tag = last_tag = -1;
	str_list = list();
	for ck in struct['clocks']:
		if tdic['start']['tag'] == '': ftag = 1;
		#break than go to the index of end
		if isinstance(ck,dict):
			if tdic['end']['tag'] <> '' and ck['type'] == tdic['end']['tag']:
				if tdic['end']['type'] == 'left':
					str_list.append(ck['mystr']);
					last_tag = idx;
				break;
			elif tdic['start']['tag'] <> '' and ck['type'] == tdic['start']['tag']:
				if tdic['start']['type'] == 'left':
					str_list.append(ck['mystr']);
					if first_tag == -1: first_tag = idx;
				ftag = 1;
			elif ftag == 1:
				last_tag = idx;
				str_list.append(ck['mystr']);
				if first_tag == -1: first_tag = idx;
		elif ftag == 1:
			last_tag = idx;
			str_list.append(ck);
			if first_tag == -1: first_tag = idx;
		idx = idx + 1;
	if len(str_list) == 0: return None;
	common.print_dic(str_list);
	print first_tag,last_tag

	if tdic['ftag'] == 'break':
		start = 0;
		end = len(str_list);
		while True:
			ck = struct['clocks'][first_tag];
			if isinstance(ck,dict):
				first_tag = first_tag + 1;
				start = start + 1;
			else:
				break;
		while True:
			ck = struct['clocks'][last_tag];
			if isinstance(ck,dict):
				last_tag = last_tag - 1;
				end = end - 1;
			else:
				break;
		name = ''.join(str_list[start:end]);
	else:
		name = ''.join(str_list);
	return name;

def _find_cks_bytime(struct,super_b):
	cks = list();
	if struct['ttag'].find('_time') == -1: return cks;
	inter = struct['intervals'][0];
	start = inter['start'];
	end = inter['end'];

	able = week = 0;
	hid = 3;
	mid = 4;
	if start[0] == 'null':
		week = _get_week(end[0],end[1],end[2]);
		able = math.pow(2,week);
	elif end[0] == 'null':
		week = _get_week(start[0],start[1],start[2]);
		able = math.pow(2,week);
	else:
		week = _get_week(start[0],start[1],start[2]);
		able = math.pow(2,week);
		eweek = _get_week(end[0],end[1],end[2]);
		if eweek - week > 1 or eweek - week < -1:
			able = able + math.pow(2,week + 1);
	for ck in super_b.clocks:
		clock = super_b.clocks[ck];
		hour = int(clock['time'].split(':')[0]);
		mins = int(clock['time'].split(':')[1]);
		#print hour,mins,able,start,end
		if start[hid] == 'null' and end[hid] == 'null':
			if clock.has_key('able') and int(clock['able']['able']) & int(able) > 0:
				cks.append(ck);
		elif start[0] == 'null':
			if end[hid] <> 'null' and hour > end[hid]: continue;
			elif end[mid] <> 'null' and hour == end[hid] and mins > end[mid]: continue;
			elif clock.has_key('able') and int(clock['able']['able']) & int(able) > 0:
				cks.append(ck);
		elif end[0] == 'null':
			if start[hid] <> 'null' and hour < start[hid]: continue;
			elif start[mid] <> 'null' and mins < start[mid]: continue;
			elif clock.has_key('able') and int(clock['able']['able']) & int(able) > 0:
				cks.append(ck);
		else:
			if start[hid] <> 'null' and hour < start[hid]: continue;
			if end[hid] <> 'null' and hour > end[hid]: continue;
			if start[mid] <> 'null' and start[mid] > mins: continue;
			if end[mid] <> 'null' and end[mid] < mins: continue;
			if clock.has_key('able') and int(clock['able']['able']) & int(able) > 0:
				cks.append(ck);
	return cks;

def _find_cks_byinfo(struct,super_b):
	cks = list();
	if len(re.findall('_and.*_relate',struct['ttag'])) > 0:
		startid = struct['text'].find(data['and']);
		endid = struct['text'].find(data['relate']);
		cinfo = struct['text'][startid + 1:endid];
		for ck in super_b.clocks.keys():
			clock = super_b.clocks[ck];
			if clock.has_key('info') and clock['info'].find(cinfo) >= 0:
				cks.append(ck);
	elif struct.has_key('ck_name'):
		cks.append(struct['ck_name']);
		del struct['ck_name'];
	elif struct['ttag'].find('_prev_prep_clock') <> -1:
		if super_b.myclock is None: return cks;
		cur_key = super_b.myclock['key'];
		mycks = super_b.clocks.keys();
		idx = mycks.index(cur_key);
		key = mycks[idx - 1];
		cks.append(key);
	elif struct['ttag'].find('_next_prep_clock') <> -1:
		if super_b.myclock is None: return cks;
		cur_key = super_b.myclock['key'];
		mycks = super_b.clocks.keys();
		idx = mycks.index(cur_key);
		if (idx + 1) >= len(mycks): idx = -1;
		key = mycks[idx + 1];
		cks.append(key);
	return cks;

def _find_cks_bytype(ttype,super_b):
	cks = list();
	for ck in super_b.clocks.keys():
		clock = super_b.clocks[ck];
		if clock.has_key('type') and clock['type'] == ttype:
			cks.append(ck);
	return cks;

def _find_cks_pastdue(super_b):
	cks = list();
	week = _get_cur_week();
	left_able = 127;
	if week > 0:
		left_able = math.pow(2,7) - math.pow(2,week);
	mtime = _get_cur_time();
	for ck in super_b.clocks:
		clock = super_b.clocks[ck];
		hour = int(clock['time'].split(':')[0]);
		mins = int(clock['time'].split(':')[1]);
		if int(left_able) & int(clock['able']['able']) == 0:
			cks.append(ck);
		elif int(left_able) & int(clock['able']['able']) == math.pow(2,week):
			if hour < mtime[3] or (hour == mtime[3] and mins < mtime[4]):
				cks.append(ck);
	return cks;

def _find_cks_nouse(super_b):
	cks = list();
	for ck in super_b.clocks.keys():
		clock = super_b.clocks[ck];
		if clock.has_key('status') and clock['status']['type'] == 'close':
			cks.append(ck);
	return cks;

def _find_cks_prep(struct,super_b):
	cks = list();
	for s in struct['inlist']:
		if data['num'].has_key(s):
			num = int(data['num'][s]);
			cks.append(super_b.clocks.keys()[num - 1]);
	return cks;

def _find_cks_after(struct,super_b):
	cks = list();
	curtime = _get_cur_time();
	week = _get_cur_week();
	able = math.pow(2,week);
	for ck in super_b.clocks.keys():
		clock = super_b.clocks[ck];
		hour = int(clock['time'].split(':')[0]);
		mins = int(clock['time'].split(':')[1]);
		if curtime[3] < hour or (curtime[3] == hour and curtime[4] <= mins):
			if clock['type'] == 'agenda' and int(clock['able']['able']) & int(able) > 0:
				cks.append(ck);
	return cks;

def _find_cks_tagtime(tag,super_b):
	cks = list();
	time = data[tag]['time'];
	tarray = time.split(':');
	week = _get_cur_week();
	able = math.pow(2,week);
	for ck in super_b.clocks.keys():
		clock = super_b.clocks[ck];
		hour = int(clock['time'].split(':')[0]);
		mins = int(clock['time'].split(':')[1]);
		if int(tarray[0]) < hour or (int(tarray[0]) == hour and int(tarray[1]) <= mins):
			if clock['type'] == 'agenda' and int(clock['able']['able']) & int(able) > 0:
				cks.append(ck);
	return cks;

def _find_cks_time_to_time(struct,super_b):
	cks = list();
	inter_1 = struct['intervals'][0];
	inter_2 = struct['intervals'][1];
	start = inter_1['start'];
	if start[0] == 'null': start = inter_1['end'];
	end = inter_2['start'];
	if end[0] == 'null': end = inter_2['end'];
	sweek = _get_week(start[0],start[1],start[2]);
	eweek = _get_week(end[0],end[1],end[2]);
	able = diff = 0;
	if sweek > eweek: eweek = eweek + 7;
	if sweek == eweek: diff = 1;
	able = 0;
	idx = sweek;
	while True:
		if sweek > eweek: break;
		able = able + math.pow(2,sweek);
		sweek = sweek + 1;

	if inter_1['scope'] == 'day' and inter_2['scope'] == 'day':
		for ck in super_b.clocks:
			clock = super_b.clocks[ck];
			if clock.has_key('able') and int(clock['able']['able']) & int(able) > 0:
				cks.append(ck);
	elif inter_1['scope'] <> 'day' and inter_2['scope'] == 'day':
		for ck in super_b.clocks:
			clock = super_b.clocks[ck];
			hour = int(clock['time'].split(':')[0]);
			mins = int(clock['time'].split(':')[1]);
			if hour < start[3] and int(clock['able']['able']) & int(math.pow(2,idx)) > 0:
				continue;
			elif int(clock['able']['able']) & int(able) <= 0:
				continue;
			cks.append(ck);
	elif inter_1['scope'] == 'day' and inter_2['scope'] <> 'day':
		for ck in super_b.clocks:
			clock = super_b.clocks[ck];
			hour = int(clock['time'].split(':')[0]);
			mins = int(clock['time'].split(':')[1]);
			if hour > end[3] and int(clock['able']['able']) & int(math.pow(2,eweek)) > 0:
				continue;
			elif hour == end[3] and int(clock['able']['able']) & int(math.pow(2,eweek)) > 0:
				if end[4] <> 'null' and end[4] < mins:
					continue;
			elif int(clock['able']['able']) & int(able) <= 0:
				continue;
			cks.append(ck);
	elif inter_1['scope'] <> 'day' and inter_2['scope'] <> 'day':
		for ck in super_b.clocks:
			clock = super_b.clocks[ck];
			hour = int(clock['time'].split(':')[0]);
			mins = int(clock['time'].split(':')[1]);
			if diff == 0:
				if hour < start[3] and int(clock['able']['able']) & int(math.pow(2,idx)) > 0:
					continue;
				if hour > end[3] and int(clock['able']['able']) & int(math.pow(2,eweek)) > 0:
					continue;
				if hour == end[3] and int(clock['able']['able']) & int(math.pow(2,eweek)) > 0:
					if end[4] <> 'null' and end[4] < mins:
						continue;
				if int(clock['able']['able']) & int(able) <= 0:
					continue;
			else:
				if hour < start[3]: continue;
				if start[4] <> 'null' and hour == start[3]:
					if start[4] > mins: continue;
				if hour > end[3]: continue;
				if end[4] <> 'null' and hour == end[3]:
					if mins > end[4]: continue;
			cks.append(ck);
	return cks;

def _get_cks_num(struct):
	inum = 0;
	global data;
	nums = data['num'].keys();
	for num in nums:
		if struct['text'].find(num) <> -1:
			inum = data['num'][num];
			break;
	return inum;

def _get_cur_week():
	times = time.localtime();
	return times[6];

def _get_cur_time(): return time.localtime();

def _get_week(year,month,day):
	dat = datetime.date(year,month,day);
	return dat.weekday();

def _get_random_id(total):
	ret = random.randint(0,total);
	if ret == total:
		ret = ret - 1;
	return ret;

def _set_msg(struct,datamsg):
	msg_id = _get_random_id(len(datamsg));
	struct['result']['msg'] = datamsg[msg_id];

def _degbu_info(struct):
	if struct.has_key('clocks'):
		debug_strs = ''
		for ck in struct['clocks']:
			if isinstance(ck,dict):
				debug_strs = debug_strs + '<' + ck['mystr'] + '>';
		struct['debug_strs'] = debug_strs;
	if struct.has_key('ttag'):
		debug_strs = ''
		tarray = struct['ttag'].split('_');
		for tag in tarray:
			if tag == '': continue;
			debug_strs = debug_strs + '<' + tag + '>';
		struct['debug_tag'] = debug_strs;
		del struct['ttag'];
	if struct.has_key('mcks'):
		cks = list();
		for ck in struct['mcks'].keys():
			clock = struct['mcks'][ck];
			cks.append(ck + '|' + clock['time']);
		struct['cks'] = cks;
	if struct.has_key('intervals'): del struct['intervals'];

