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
#============================================
import common,config
from time_ut import UT
from time_ut import UTE
from time_ut import CUTE
from time_nt import NT
from time_nt import NTE
from time_nt import CNTE
from time_wt import WT
from time_wt import WTE
from time_wt import CWTE
from time_qt import QT
from time_qt import CQT
from time_allt import ALLT
from time_allt import CALLT
from time_mood import TS
from time_mood import TM
from time_mood import AS
from time_decade import DT
from time_decade import DTE
from time_decade import CDTE

qt = QT();
cqt = CQT();
ut = UT();
ute = UTE();
cute = CUTE();
nt = NT();
nte = NTE();
cnte = CNTE();
wt = WT();
wte = WTE();
allt = ALLT();
callt = CALLT();
cwte = CWTE();
ts = TS();
tm = TM();
ass = AS();
dt = DT();
dte = DTE();
cdte = CDTE();
#tw.load_data('./TQ.txt');
ut.load_data('./tdata/UT.txt');
ute.load_data('./tdata/UTE.txt');
nt.load_data('./tdata/NT.txt');
nte.load_data('./tdata/NTE.txt');
wt.load_data('./tdata/WT.txt');
wte.load_data('./tdata/WTE.txt');
qt.load_data('./tdata/QT.txt');
ts.load_data('./tdata/TS.txt');
tm.load_data('./tdata/TM.txt');
ass.load_data('./tdata/AS.txt');
dt.load_data('./tdata/DT.txt');
dte.load_data('./tdata/DTE.txt');
struct = dict();
struct['text'] = u'古代'#19世纪30年代的21世纪前期的21世纪初期的21世纪30年代前的30年代前'#3日前的4月3号上午的5时6分钟的后天上午上周3的周4前的5时3刻的第4季度的2月上旬后天17时';
struct['inlist'] = [u'有时']
#struct['inlist'] = [u'上',u'周','3',u'周','1'];
#struct['taglist'] = [u'上',u'周','3',u'周','1'];
#tw.encode(struct);
ut.encode(struct);
ute.encode(struct);
dte.encode(struct);
nt.encode(struct);
#common.print_dic(struct);
nte.encode(struct);
dt.encode(struct);

wt.encode(struct);
#common.print_dic(struct);
wte.encode(struct);
qt.encode(struct);
allt.encode(struct);
#common.print_dic(struct);
callt.encode(struct);
cqt.encode(struct);
ts.encode(struct);
tm.encode(struct);
ass.encode(struct);

cdte.encode(struct);
cute.encode(struct);
cnte.encode(struct);
cwte.encode(struct);
common.print_dic(struct);
