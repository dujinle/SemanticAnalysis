#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,json,re
reload(sys);
sys.setdefaultencoding('utf-8');
#============================================
''' import MyException module '''
base_path = os.path.dirname(__file__);
sys.path.append(os.path.join(base_path,'../../commons'));
#============================================
import config
ALARM_TAG = True;
#u'对闹钟进行时间段划分建立索引,方便搜索'
ALARM_CATES = [u'早上',u'上午',u'中午',u'下午',u'晚上'];
