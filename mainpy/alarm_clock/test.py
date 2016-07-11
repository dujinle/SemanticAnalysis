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
sys.path.append(os.path.join(base_path,'../'));
sys.path.append(os.path.join(base_path,'../timer'));
sys.path.append(os.path.join(base_path,'../wordsegs'));
#============================================
import common,config
from alarm_engin import AEngin
from alarm_adjust import AAD
from alarm_fname import ACname
from time_mager import TimeMager
from wordseg import WordSeg
ae = AEngin();
aad = AAD();
aname = ACname();
wd = WordSeg();
timer = TimeMager(wd);
timer.init('Timer');
ae.load_data('./tdata/message.txt');
aad.load_data('./tdata/adjust.txt');
aname.load_data('./tdata/ck_name.txt');

#print wd.tokens(struct['text']);
#struct['inlist'] = [u'有时']
#struct = timer.encode(u'增加一个5点40闹钟,调晚一点');
#struct = timer.encode(u'7点50分的闹钟调晚一点,一直闹的');
struct = timer.encode(u'帮我设置一个闹钟');
aad.encode(struct);
aname.encode(struct);
ae.encode(struct);
common.print_dic(struct);

struct = timer.encode(u'8点50分');
aad.encode(struct);
aname.encode(struct);
ae.encode(struct);
common.print_dic(struct);

struct = timer.encode(u'要延迟响铃的');
aad.encode(struct);
aname.encode(struct);
ae.encode(struct);
common.print_dic(struct);

struct = timer.encode(u'除了周3');
aad.encode(struct);
aname.encode(struct);
ae.encode(struct);
common.print_dic(struct);
