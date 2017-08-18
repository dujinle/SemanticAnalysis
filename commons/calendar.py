#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math,datetime,time

tian_gan = [u'癸',u"甲",u"乙",u"丙",u"丁",u"戊",u"己",u"庚",u"辛",u"壬",u"癸"]
di_zhi = [u'亥',u"子",u"丑",u"寅",u"卯",u"辰",u"巳",u"午",u"未",u"申",u"酉",u"戌",u"亥"]
#输入年份 输出对应的天干地支
def get_gan_zhi_year(date):

	year = date.year;
	gyear = tian_gan[(year - 3) % 10] + di_zhi[(year - 3) % 12]

	print gyear + u'年'

def get_gan_zhi_month(date):
	year = date.year;
	month = date.month;
	print year,month
	num = (year % 10 + 7) * 2 + month + 1;
	gmonth = tian_gan[num % 10] + di_zhi[(month + 3) % 12]
	print gmonth + u'月'

def get_gan_zhi_hour(date):

	gan_zhi_hour = {
		0:u"子时",1:u"丑时",2:u"丑时",3:u"寅时",4:u"寅时",5:u"卯时",6:u"卯时",7:u"辰时",8:u"辰时",9:u"巳时",10:u"巳时",11:u"午时",
		12:u"午时",13:u"未时",14:u"未时",15:u"申时",16:u"申时",17:u"酉时",18:u"酉时",19:u"戌时",20:u"戌时",21:u"亥时",22:u"亥时",23:u"子时",24:u"子时"
	}
	cur_time = time.localtime()
	start_date_time = datetime.datetime(year = 1900,month = 1,day = 1,hour = 1)
	#60干支乙丑是第二个，以0为起点，则编号为1
	startganzhi = 1
	if not isinstance(date,datetime.datetime):
		return ""
	#计算离基准时刻过去了多少时间
	delta = date - start_date_time
	if delta.seconds < 0: return ""
	#计算时刻的干支编号 
	hour = delta.days * 24 + delta.seconds/3600
	num = (startganzhi + hour / 2) % 10
	ghour = tian_gan[num] + gan_zhi_hour[date.hour]

	print ghour

	
def GetDayOf(st):
	#–天干名称
	tian_gan = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
	#–地支名称
	di_zhi = ["子","丑","寅","卯","辰","巳","午", "未","申","酉","戌","亥"]
	#–属相名称
	shu_xiang = ["鼠","牛","虎","兔","龙","蛇", "马","羊","猴","鸡","狗","猪"]
	#–农历日期名
	day_name =[
		"*","初一","初二","初三","初四","初五",
		"初六","初七","初八","初九","初十",
		"十一","十二","十三","十四","十五",
		"十六","十七","十八","十九","二十",
		"廿一","廿二","廿三","廿四","廿五",
		"廿六","廿七","廿八","廿九","三十"
	]
	#–农历月份名
	month_name = ["*","正","二","三","四","五","六", "七","八","九","十","十一","腊"]
	#–公历每月前面的天数
	month_add = [0,31,59,90,120,151,181,212,243,273,304,334]
	# 农历数据
	wNongliData = [2635,333387,1701,1748,267701,694,2391,133423,1175,396438
		,3402,3749,331177,1453,694,201326,2350,465197,3221,3402
		,400202,2901,1386,267611,605,2349,137515,2709,464533,1738
		,2901,330421,1242,2651,199255,1323,529706,3733,1706,398762
		,2741,1206,267438,2647,1318,204070,3477,461653,1386,2413
		,330077,1197,2637,268877,3365,531109,2900,2922,398042,2395
		,1179,267415,2635,661067,1701,1748,398772,2742,2391,330031
		,1175,1611,200010,3749,527717,1452,2742,332397,2350,3222
		,268949,3402,3493,133973,1386,464219,605,2349,334123,2709
		,2890,267946,2773,592565,1210,2651,395863,1323,2707,265877
	]
	#—取当前公历年、月、日—
	cur_year = st["year"]
	cur_month = st["mon"]
	cur_day = st["day"]
	#—计算到初始时间1921年2月8日的天数：1921-2-8(正月初一)—
	nTheDate = (cur_year - 1921) * 365 + (cur_year - 1921)/4 + cur_day + month_add[cur_month - 1] - 38
	if (((cur_year % 4) == 0) and (cur_month > 2)):
		nTheDate = nTheDate + 1
		#–计算农历天干、地支、月、日—
	nIsEnd = 0
	m = 0
	while nIsEnd != 1:
	#if wNongliData[m+1] < 4095:
		if wNongliData[m] < 4095:
			k = 11
		else:
			k = 12
		n = k
		while n>=0:
			nBit = wNongliData[m]
			for i in range(n):
				nBit = math.floor(nBit/2);
			nBit = nBit % 2
			if nTheDate <= (29 + nBit):
				nIsEnd = 1
				break
			nTheDate = nTheDate - 29 - nBit
			n = n - 1
		if nIsEnd != 0:
			break
		m = m + 1
	cur_year = 1921 + m
	cur_month = k - n + 1
	cur_day = int(math.floor(nTheDate))
	if k == 12:
		if cur_month == wNongliData[m] / 65536 + 1:
			cur_month = 1 - cur_month
		elif cur_month > wNongliData[m] / 65536 + 1:
			cur_month = cur_month - 1
	print '阳历', st["year"], st["mon"], st["day"]
	print '农历', cur_year, cur_month, cur_day
	#–生成农历天干、地支、属相 ==> wNongli–
	cur_sx = shu_xiang[(((cur_year - 4) % 60) % 12) + 1]
	get_gan_zhi_year(datetime.datetime(year = cur_year,month = cur_month,day = cur_day,hour = 3))
	get_gan_zhi_month(datetime.datetime(year = cur_year,month = cur_month,day = cur_day,hour = 3))
	get_gan_zhi_hour(datetime.datetime(year = cur_year,month = cur_month,day = cur_day,hour = 3))

	#–snong_li,"%s(%s%s)年",cur_sx,tian_gan[((cur_year - 4) % 60) % 10],di_zhi[((cur_year - 4) % 60) % 12]);
	#–生成农历月、日 ==> wNongliDay–*/
	if cur_month < 1:
		nong_li_day =  "闰" + month_name[(-1 * cur_month)]
	else:
		nong_li_day = month_name[cur_month]
	nong_li_day =  nong_li_day + "月" + day_name[cur_day]
	print nong_li_day
	#return snong_li .. nong_li_day
def main():
	st = {"year": 1989, "mon": 8, "day": 1}
	GetDayOf(st)
	st1 = {"year": 2013, "mon": 10, "day": 7}
	GetDayOf(st1)
	st1 = {"year": 2016, "mon": 11, "day": 21}
	GetDayOf(st1)
	#print("" .. GetDayOf(st))
main()
