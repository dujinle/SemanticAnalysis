#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json
import re,time
reload(sys);
sys.setdefaultencoding('utf8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
sys.path.append(os.path.join(base_path,'../'));
#============================================
import common,config
from MT import MT
from MSR import MSR
from MSN import MSN
mt = MT();
msr = MSR();
msn = MSN();
mt.load_data('./tdata/MT.txt');
msr.load_data('./tdata/MSR.txt');
msn.load_data('./tdata/MSN.txt');
struct = dict();
#struct['text'] = u'来一首纯音乐'
#struct['inlist'] = [u'来一首','纯音乐']
#struct['music'] = [u'来一首','纯音乐']
struct['text'] = u'来一首王菲的歌'
struct['inlist'] = [u'来一首',u'王菲',u'的',u'歌']
struct['music'] = [u'来一首',u'王菲',u'的',u'歌']
mt.encode(struct);
msr.encode(struct);
msn.encode(struct);
common.print_dic(struct);

