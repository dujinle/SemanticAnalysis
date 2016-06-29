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
		"1":os.path.join(abspath,'data','timer','UT.txt'),
		"2":os.path.join(abspath,'data','timer','NT.txt'),
		"3":os.path.join(abspath,'data','timer','WT.txt'),
		"4":os.path.join(abspath,'data','timer','QT.txt'),
		"5":os.path.join(abspath,'data','timer','UTE.txt'),
		"6":os.path.join(abspath,'data','timer','NTE.txt'),
		"7":os.path.join(abspath,'data','timer','WTE.txt'),
		"8":None,
		"9":None,
		"10":None,
		"11":None,
		"12":None,
		"13":None,
		"14":os.path.join(abspath,'data','timer','TM.txt'),
		"15":os.path.join(abspath,'data','timer','TS.txt'),
		"16":os.path.join(abspath,'data','timer','AS.txt')
	},
	'Local':{
		"1":os.path.join(abspath,'data','location','HD')
	},
	'Catering':{
		"1":os.path.join(abspath,'data','catering','CTR.txt'),
		"2":os.path.join(abspath,'data','catering','CAT.txt')
	},
	'Flight':{
		"1":os.path.join(abspath,'data','flight','FT.txt')
	},
	'Music':{
		"1":os.path.join(abspath,'data','music','MT.txt'),
		"2":os.path.join(abspath,'data','music','MSR.txt')
	}
};
