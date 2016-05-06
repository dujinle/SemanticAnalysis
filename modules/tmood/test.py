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
sys.path.append(os.path.join(base_path,'../wordsegs'));
#============================================
import common,config
from wordseg import WordSeg
from tmood_mager import TMoodMager

wd = WordSeg();
nmager = TMoodMager();
nmager.init('TMood');

struct = dict();
struct['text'] = u'现今';
struct['inlist'] = wd.tokens(struct['text']);
nmager.encode(struct);
common.print_dic(struct);
