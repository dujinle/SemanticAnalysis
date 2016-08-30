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
from mytag_encode import MyTagEncode
me = MyTagEncode();
me.init('./tdata/mytag.txt');
struct = dict();
#struct['text'] = u'来一首纯音乐'
#struct['inlist'] = [u'来一首','纯音乐']
#struct['music'] = [u'来一首','纯音乐']
struct['text'] = u'来一首王菲的歌'
me.encode(struct);
common.print_dic(struct);

