#!/usr/bin/python
# -*- coding:utf-8 -*-

import os, io, sys, re, time, datetime
import time_common

class LunarDate(object):
	_startDate = datetime.date(1900, 1, 31)

	def __init__(self, year, month, day, isLeapMonth=False):
		self.year = year
		self.month = month
		self.day = day
		self.isLeapMonth = bool(isLeapMonth)

	@staticmethod
	def fromSolarDate(year, month, day):
		solarDate = datetime.date(year, month, day)
		offset = (solarDate - LunarDate._startDate).days
		return LunarDate._fromOffset(offset)

	@staticmethod
	def toSolarDate(year, month, day,isLeapMonth):
		def _calcDays(yearInfo, month, day, isLeapMonth):
			isLeapMonth = int(isLeapMonth)
			res = 0
			for _month, _days, _isLeapMonth in LunarDate._enumMonth(yearInfo):
				if (_month, _isLeapMonth) == (month, isLeapMonth):
					if 1 <= day <= _days:
						res += day - 1
						return res
					else:
						raise ValueError('day out of range')
				res += _days
			raise ValueError('month out of range')

		offset = 0
		if year < 1900 or year >= 2050:
			raise ValueError('year out of range [1900, 2050)')
		yearIdx = year - 1900
		for i in range(yearIdx):
			offset += Info.yearDays()[i]
		offset += _calcDays(Info.yearInfos[yearIdx], month, day, isLeapMonth)
		return LunarDate._startDate + datetime.timedelta(days=offset)

	@staticmethod
	def _enumMonth(yearInfo):
		months = [(i, 0) for i in range(1, 13)]
		leapMonth = yearInfo % 16
		if leapMonth == 0: pass
		elif leapMonth <= 12:
			months.insert(leapMonth, (leapMonth, 1))
		else:
			raise ValueError('yearInfo %r mod 16 should in [0, 12]' % yearInfo)

		for month, isLeapMonth in months:
			if isLeapMonth:
				days = (yearInfo >> 16) % 2 + 29
			else:
				days = (yearInfo >> (16 - month)) % 2 + 29
			yield month, days, isLeapMonth

	@classmethod
	def _fromOffset(cls, offset):
		def _calcMonthDay(yearInfo, offset):
			for month, days, isLeapMonth in cls._enumMonth(yearInfo):
				if offset < days: break
				offset -= days
			return (month, offset + 1, isLeapMonth)
		offset = int(offset)
		for idx, yearDay in enumerate(Info.yearDays()):
			if offset < yearDay: break
			offset -= yearDay
		year = 1900 + idx
		yearInfo = Info.yearInfos[idx]
		month, day, isLeapMonth = _calcMonthDay(yearInfo, offset)
		return LunarDate(year, month, day, isLeapMonth)

class Info():
	yearInfos = [
		#    /* encoding:
		#               b bbbbbbbbbbbb bbbb
		#       bit#    1 111111000000 0000
		#               6 543210987654 3210
		#               . ............ ....
		#       month#    000000000111
		#               M 123456789012   L
		#
		#    b_j = 1 for long month, b_j = 0 for short month
		#    L is the leap month of the year if 1<=L<=12; NO leap month if L = 0.
		#    The leap month (if exists) is long one iff M = 1.
		#    */
		0x04bd8,                                    #   /* 1900 */
		0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950,#   /* 1905 */
		0x16554, 0x056a0, 0x09ad0, 0x055d2, 0x04ae0,#   /* 1910 */
		0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540,#   /* 1915 */
		0x0d6a0, 0x0ada2, 0x095b0, 0x14977, 0x04970,#   /* 1920 */
		0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54,#   /* 1925 */
		0x02b60, 0x09570, 0x052f2, 0x04970, 0x06566,#   /* 1930 */
		0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60,#   /* 1935 */
		0x186e3, 0x092e0, 0x1c8d7, 0x0c950, 0x0d4a0,#   /* 1940 */
		0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0,#   /* 1945 */
		0x092d0, 0x0d2b2, 0x0a950, 0x0b557, 0x06ca0,#   /* 1950 */
		0x0b550, 0x15355, 0x04da0, 0x0a5d0, 0x14573,#   /* 1955 */
		0x052d0, 0x0a9a8, 0x0e950, 0x06aa0, 0x0aea6,#   /* 1960 */
		0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260,#   /* 1965 */
		0x0f263, 0x0d950, 0x05b57, 0x056a0, 0x096d0,#   /* 1970 */
		0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250,#   /* 1975 */
		0x0d558, 0x0b540, 0x0b5a0, 0x195a6, 0x095b0,#   /* 1980 */
		0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50,#   /* 1985 */
		0x06d40, 0x0af46, 0x0ab60, 0x09570, 0x04af5,#   /* 1990 */
		0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58,#   /* 1995 */
		0x05ac0, 0x0ab60, 0x096d5, 0x092e0, 0x0c960,#   /* 2000 */
		0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0,#   /* 2005 */
		0x0abb7, 0x025d0, 0x092d0, 0x0cab5, 0x0a950,#   /* 2010 */
		0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0,#   /* 2015 */
		0x0a5b0, 0x15176, 0x052b0, 0x0a930, 0x07954,#   /* 2020 */
		0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6,#   /* 2025 */
		0x0a4e0, 0x0d260, 0x0ea65, 0x0d530, 0x05aa0,#   /* 2030 */
		0x076a3, 0x096d0, 0x04afb, 0x04ad0, 0x0a4d0,#   /* 2035 */
		0x1d0b6, 0x0d250, 0x0d520, 0x0dd45, 0x0b5a0,#   /* 2040 */
		0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0,#   /* 2045 */
		0x0aa50, 0x1b255, 0x06d20, 0x0ada0          #   /* 2049 */
	]

	@staticmethod
	def yearInfo2yearDay(yearInfo):
		yearInfo = int(yearInfo)
		res = 29 * 12
		leap = False
		if yearInfo % 16 != 0:
			leap = True
			res += 29
		yearInfo //= 16

		for i in range(12 + leap):
			if yearInfo % 2 == 1:
				res += 1
			yearInfo //= 2
		return res

	@staticmethod
	def yearDays():
		yearDays = [Info.yearInfo2yearDay(x) for x in Info.yearInfos]
		return yearDays

def ToSolarDate(year,month,day,isLeapMonth=False):
	solar = LunarDate.toSolarDate(year,month,day,isLeapMonth);
	return solar.year,solar.month,solar.day;

def TolunarDate(year,month,day):
	lundate = LunarDate.fromSolarDate(year,month,day);
	return (lundate.year,lundate.month,lundate.day,lundate.isLeapMonth);

def GetSolarWeek(year,month,idx,week):
	mon_day = time_common.month[month % 12];
	if time_common._is_leap_year(year):
		mon_day = time_common.leap_mon[month % 12];
	cur_day = 1;
	week_day = list();
	while True:
		if cur_day > mon_day: break;
		date_str = str(year) + str(month) + str(cur_day);
		time_st = time.strptime(date_str,'%Y%m%d');
		if time_st[6] == week - 1:
			week_day.append(cur_day);
		cur_day = cur_day + 1;
	return (year,month,week_day[idx - 1]);

def GetSolarFullWeek(year,month,idx,week):
	mon_day = time_common.month[month % 12];
	if time_common._is_leap_year(year):
		mon_day = time_common.leap_mon[month % 12];
	cur_day = 1;
	week_day = list();
	while True:
		if cur_day > mon_day: break;
		date_str = str(year) + str(month) + str(cur_day);
		time_st = time.strptime(date_str,'%Y%m%d');
		if time_st[6] == 0 and cur_day + 6 <= mon_day:
			week_day.append(cur_day);
			cur_day = cur_day + 6;
			continue;
		cur_day = cur_day + 1;
	cur_week = week_day[idx - 1];
	return (year,month,cur_week + week - 1);
