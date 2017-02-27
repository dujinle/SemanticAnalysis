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
	"Fetch":{
		"1":os.path.join(abspath,'modules','fetch_stc','tdata','fetch_before.json'),
		"2":os.path.join(abspath,'modules','fetch_stc','tdata','fetch_01layer.json'),
		"3":os.path.join(abspath,'modules','fetch_stc','tdata','fetch_02layer.json'),
		"4":os.path.join(abspath,'modules','fetch_stc','tdata','fetch_03layer.json'),
		"5":os.path.join(abspath,'modules','fetch_stc','tdata','fetch_math.json'),
		"6":os.path.join(abspath,'modules','fetch_stc','tdata','fetch_10layer.json'),
		"7":os.path.join(abspath,'modules','fetch_stc','tdata','fetch_11layer.json')
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
	'Alarm':os.path.join(abspath,'scenes','alarm_clock','tdata'),
	'Music':{
		"1":os.path.join(abspath,'scenes','dmusic','tdata','music_data.txt'),
		"2":os.path.join(abspath,'scenes','dmusic','tdata','under_music.txt'),
		"3":os.path.join(abspath,'data','music','MT.txt'),
		"4":os.path.join(abspath,'data','music','MSR.txt'),
		"5":os.path.join(abspath,'data','music','MSN.txt')
	},
	'Mytag':{
		"1":os.path.join(abspath,'modules','mytag','tdata','mytag.txt')
	},
	"PDeal":{
		"1":os.path.join(abspath,'modules','prev_deal','tdata','pdeal_replace.txt'),
		"2":os.path.join(abspath,'modules','prev_deal','tdata','pdeal_nunit.json')
	},
	"Shop":{
		"1":os.path.join(abspath,'scenes','shopping','tdata','shop_data.txt'),
		"2":os.path.join(abspath,'scenes','shopping','tdata','under_shop.txt')
	},
	"Nav":{
		"1":os.path.join(abspath,'scenes','navigation','tdata','nav_data.txt'),
		"2":os.path.join(abspath,'scenes','navigation','tdata','under_nav.txt')
	},
	"O2O":{
		"1":os.path.join(abspath,'scenes','on_off_line','tdata','o2o_data.txt'),
		"2":os.path.join(abspath,'scenes','on_off_line','tdata','under_o2o.txt')
	},
	"Phone":{
		"1":os.path.join(abspath,'scenes','send_message','tdata','phone_data.txt'),
		"2":os.path.join(abspath,'scenes','send_message','tdata','phone_users.txt'),
		"3":os.path.join(abspath,'scenes','send_message','tdata','under_phone.txt')
	},
	"Flight":{
		"1":os.path.join(abspath,'scenes','flight','tdata','flight_data.txt'),
		"2":os.path.join(abspath,'scenes','flight','tdata','under_flight.txt')
	},
	"News":{
		"1":os.path.join(abspath,'scenes','push_news','tdata','pnews.txt'),
		"2":os.path.join(abspath,'scenes','push_news','tdata','under_model.txt')
	},
	"Calendar":{
		"1":os.path.join(abspath,'scenes','calendar','tdata','cal_data.txt'),
		"2":os.path.join(abspath,'scenes','calendar','tdata','under_cal.txt')
	},
	"Traffic":{
		"1":os.path.join(abspath,'scenes','traffic','tdata','guide_data.txt'),
		"2":os.path.join(abspath,'scenes','traffic','tdata','traffic.txt')
	},
	"Math":{
		"1":os.path.join(abspath,'scenes','math','tdata','under_math.txt')
	},
	"Food":{
		"1":os.path.join(abspath,'scenes','foodspot','tdata','food_data.txt'),
		"2":os.path.join(abspath,'scenes','foodspot','tdata','under_food.txt')
	},
	"Trans":{
		"1":os.path.join(abspath,'scenes','translation','tdata','trans_data.txt'),
		"2":os.path.join(abspath,'scenes','translation','tdata','under_trans.txt')
	}
};
