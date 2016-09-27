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
sys.path.append(os.path.join(base_path,'../../modules/timer'));
sys.path.append(os.path.join(base_path,'../../modules/wordsegs'));
sys.path.append(os.path.join(base_path,'../../modules/mytag'));
#============================================
import common,config
from time_mager import TimeMager
from tag_mager import MytagMager
from wordseg import WordSeg

from scene_engin import SEngin
from concept import Concept
from dist_scene import DistScene
from scene_add import SceneAdd
from prev_scene import PrevScene
from scene_tadd import SceneTadd
from scene_stop import SceneStop
from scene_close import SceneClose
from scene_getup import SceneGetup
from scene_agenda import SceneAgenda

wd = WordSeg();
timer = TimeMager(wd);
tag = MytagMager(wd);
se = SEngin(wd);

se.init('../tdata/');
timer.init('Timer');
tag.init('Mytag');

struct = dict();
struct['result'] = dict();
#'''
while True:
	mstr = raw_input('Enter your input: ');
	if mstr == 'q': break;
	struct['text'] = mstr.decode('utf-8');
	timer.encode(struct);
	tag.encode(struct);
	se.encode(struct);
	common.print_dic(struct);
#'''
