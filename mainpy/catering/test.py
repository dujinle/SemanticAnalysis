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
from CTR import CTR
from CAT import CAT
cu = CTR();
cat = CAT();
cu.init('./CTR.txt');
cat.init('./CAT.txt');
struct = dict();
#struct['text'] = u'来一首纯音乐'
#struct['inlist'] = [u'来一首','纯音乐']
#struct['music'] = [u'来一首','纯音乐']
struct['text'] = u'附近可以约会的餐馆';
struct['inlist'] = [u'附近',u'可以',u'约会',u'的',u'餐馆'];
struct['catering'] = [u'附近',u'可以',u'约会',u'的',u'餐馆'];
cu.encode(struct);
cat.encode(struct);
common.print_dic(struct);

