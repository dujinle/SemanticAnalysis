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
		if myinterval['scope'] == 'day' or myinterval['scope'] == 'month' \
			or myinterval['scope'] == 'year':
			tdic = dict();
			tdic['date'] = str(times[0]) + '/' + str(times[1]) + '/' + str(times[2]);
			tdic['type'] = myinterval['type'];
			struct['ck_date'] = tdic;
		if times[3] <> 0:
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

def _find_ck_name(struct):
	ttag = struct['ttag'];
	if ttag.find('_clock') <> -1:
		idx = len(struct['clocks']) - 1;
		tag = False;
		name = '';
		while True:
			if idx < 0: break;
			cl = struct['clocks'][idx];
			if tag == True and isinstance(cl,dict): break;
			if isinstance(cl,dict) and cl['type'] == '_clock':
				tag = True;
			elif tag == True and cl == u'的':
				pass;
			elif tag == True:
				name = cl + name;
			idx = idx - 1;
		return name;
	if ttag.find('_remind') <> -1:
		idx = len(struct['clocks']) - 1;
		tag = False;
		name = '';
		while True:
			if idx < 0: break;
			cl = struct['clocks'][idx];
			if tag == True and isinstance(cl,dict): break;
			if isinstance(cl,dict) and cl['type'] == '_remind':
				tag = True;
			elif tag == True and cl == u'的':
				pass;
			elif tag == True:
				name = cl + name;
			idx = idx - 1;
		return name;
	return None;
	return None;

def _find_tag_name(struct):
	ttag = struct['ttag'];
	if ttag.find('_clock') <> -1:
		idx = len(struct['clocks']) - 1;
		tag = False;
		name = '';
		while True:
			if idx < 0: break;
			cl = struct['clocks'][idx];
			if tag == True and isinstance(cl,dict): break;
			if isinstance(cl,dict) and cl['type'] == '_clock':
				tag = True;
			elif tag == True and cl == u'的':
				pass;
			elif tag == True:
				name = cl + name;
			idx = idx - 1;
		return name;
	if ttag.find('_remind') <> -1:
		idx = len(struct['remind']) - 1;
		tag = False;
		name = '';
		while True:
			if idx < 0: break;
			cl = struct['clocks'][idx];
			if tag == True and isinstance(cl,dict): break;
			if isinstance(cl,dict) and cl['type'] == '_remind':
				tag = True;
			elif tag == True and cl == u'的':
				pass;
			elif tag == True:
				name = cl + name;
			idx = idx - 1;
		return name;
	return None;
	return None;

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
		if start[hid] == 0 and end[hid] == 0:
			if clock.has_key('able') and int(clock['able']['able']) & int(able) > 0:
				cks.append(ck);
		elif start[0] == 'null':
			if hour < end[hid] or (hour == end[hid] and mins <= end[mid]):
				if clock.has_key('able') and int(clock['able']['able']) & int(able) > 0:
					cks.append(ck);
		elif end[0] == 'null':
			if hour > start[hid] or (hour == start[hid] and mins >= start[mid]):
				if clock.has_key('able') and int(clock['able']['able']) & int(able) > 0:
					cks.append(ck);
		else:
			if hour > start[hid] or (hour == start[hid] and start[mid] <= mins):
				if hour < end[hid] or (hour == end[hid] and mins <= end[mid]):
					if clock.has_key('able') and int(clock['able']['able']) & int(able) > 0:
						cks.append(ck);
	return cks;

def _find_cks_byinfo(struct,super_b):
	cks = list();
	common.print_dic(struct);
	if struct.has_key('ck_name'):
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
	elif len(re.findall('_and.*_relate',struct['ttag'])) > 0:
		startid = struct['text'].find(data['and']);
		endid = struct['text'].find(data['relate']);
		cinfo = struct['text'][startid + 1:endid];
		for ck in super_b.clocks.keys():
			clock = super_b.clocks[ck];
			if clock.has_key('info') and clock['info'].find(cinfo) > 0:
				cks.append(ck);
	if struct['ttag'].find('_moveto') <> -1:
		tstr =_get_match_str(struct,'_moveto');
		if tstr is None: return cks;
		cinfo_id = struct['text'].find(tstr);
		if cinfo_id == 0 or cinfo_id == -1: return cks;
		cinfo = struct['text'][:cinfo_id];
		if super_b.clocks.has_key(cinfo):
			cks.append(cinfo);
	elif struct['ttag'].find('_ahead') <> -1:
		tstr =_get_match_str(struct,'_ahead');
		if tstr is None: return cks;
		cinfo_id = struct['text'].find(tstr);
		if cinfo_id == 0 or cinfo_id == -1: return cks;
		cinfo = struct['text'][:cinfo_id];
		if super_b.clocks.has_key(cinfo):
			cks.append(cinfo);
	elif struct['ttag'].find('_clock') <> -1:
		tstr =_get_match_str(struct,'_clock');
		if tstr is None: return cks;
		cinfo_id = struct['text'].find(tstr);
		if cinfo_id == 0 or cinfo_id == -1: return cks;
		cinfo = struct['text'][:cinfo_id];
		if super_b.clocks.has_key(cinfo):
			cks.append(cinfo);
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
		left_able = math.pow(2,7) - math.pow(2,week - 1);
	mtime = _get_cur_time();
	for ck in super_b.clocks:
		clock = super_b.clocks[ck];
		hour = int(clock['time'].split(':')[0]);
		mins = int(clock['time'].split(':')[1]);
		if int(left_able) & int(clock['able']['able']) > 1:
			cks.append(ck);
		elif int(left_able) & int(clock['able']['able']) == 1:
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
			num = data['num'][s];
			cks.append(super_b.clocks.keys()[num - 1]);
	return cks;

def _get_match_str(struct,tag):
	comp = re.compile(data[tag]['str']);
	match = comp.search(struct['text']);
	if match is None: return None;
	tstr = match.group(0);
	return tstr;

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

