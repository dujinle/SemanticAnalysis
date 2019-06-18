#!/usr/bin/python
import os
abspath = os.path.dirname(__file__);
abspath = os.path.join(abspath,'../');
dtype = 'Voice';

tm_year = 0;
tm_mon = 1;
tm_day = 2;
tm_hour = 3;
tm_min = 4;
tm_sec = 5;
mongodb = {
	'ip':'172.17.0.5',
	'user':'root',
	'pwd':'root',
	'database':'ChinaNet'
};
dfiles = {
	'Voice':{
		"1":os.path.join(abspath,'data','voice','M.txt'),
		"2":os.path.join(abspath,'data','voice','C.txt'),
		"3":os.path.join(abspath,'data','voice','F.txt'),
		"4":os.path.join(abspath,'data','voice','X.txt'),
		"5":os.path.join(abspath,'data','voice','X1.txt'),
		"6":os.path.join(abspath,'data','voice','M1.txt'),
		"7":os.path.join(abspath,'data','voice','F1.txt'),
		"8":os.path.join(abspath,'data','voice','Z.txt'),
		"9":os.path.join(abspath,'data','voice','PM.txt'),
		"10":os.path.join(abspath,'data','voice','Num.txt')
	},
	'Temp':{
		"1":os.path.join(abspath,'data','temperature','M.txt'),
		"2":os.path.join(abspath,'data','temperature','C.txt'),
		"3":os.path.join(abspath,'data','temperature','F.txt'),
		"4":os.path.join(abspath,'data','temperature','X.txt'),
		"5":os.path.join(abspath,'data','temperature','Nt.txt'),
		"6":os.path.join(abspath,'data','temperature','X1.txt'),
		"7":os.path.join(abspath,'data','temperature','M1.txt'),
		"8":os.path.join(abspath,'data','temperature','F1.txt'),
		"9":os.path.join(abspath,'data','temperature','Z.txt'),
		"10":os.path.join(abspath,'data','temperature','PM.txt'),
		"11":os.path.join(abspath,'data','temperature','Num.txt')
	},
	'Timer':{
		"1":os.path.join(abspath,'data','timer','TReplace.txt'),
		"2":os.path.join(abspath,'data','timer','TFront.txt'),
		"3":os.path.join(abspath,'data','timer','TNormal.txt'),
		"4":os.path.join(abspath,'data','timer','TBucket.txt'),
		"5":os.path.join(abspath,'data','timer','TWeek.txt'),
		"6":os.path.join(abspath,'data','timer','TFestival.txt'),
		"7":os.path.join(abspath,'data','timer','TEFestival.txt'),
		"8":os.path.join(abspath,'data','timer','TSolarterm.txt'),
		"9":os.path.join(abspath,'data','timer','TDecade.txt'),
		"10":os.path.join(abspath,'data','timer','TMood.txt')
	},
	"Concept":{
		"1":None
	},
	"Dist":{
		"1":os.path.join(abspath,'modules','dist_scene','tdata','mark_dist.json')
	},
	'Local':{
		"1":os.path.join(abspath,'data','location','HD')
	},
	'Catering':{
		"1":os.path.join(abspath,'data','catering','CTR.txt'),
		"2":os.path.join(abspath,'data','catering','CAT.txt')
	},
	'Alarm':os.path.join(abspath,'scenes','alarm_clock','tdata')
};
