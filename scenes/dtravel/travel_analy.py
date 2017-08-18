#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys,os,common,re
from common import logging
from myexception import MyException
from scene_base import SceneBase
import com_funcs as ComFuncs

#处理预定 航班 酒店 信息
class TravelAnaly(SceneBase):

	def encode(self,struct,super_b):
		try:
			logging.info('go into travel analysis......');
			if not struct.has_key('step'): struct['step'] = 'start';

			func = self._fetch_func(struct);
			print 'func:',func,'.......';
			if struct['step'] == 'start':
				if func == 'set_trip':
					self._fetch_flight(struct,super_b);
					return None;
			elif struct['step'] == 'set_trip'\
				or struct['step'] == 'set_trip_time' \
				or struct['step'] == 'set_trip_start'\
				or struct['step'] == 'set_trip_end':
				self._fetch_flight(struct,super_b);
				return None;
			elif struct['step'] == 'sel_flight':
				if func == 'book':
					self._book_flight(struct,super_b);
			elif struct['step'] == 'set_hotel':
				self._fetch_hotel(struct,super_b);
				return None;
			elif struct['step'] == 'sel_hotel':
				self._book_hotel(struct,super_b);
				return None;
			elif struct['step'] == 'set_room':
				self._set_room(struct,super_b);
			struct['step'] = 'end';
		except Exception as e:
			raise MyException(sys.exc_info());


#-----------flight functions ------------
	def _fetch_flight(self,struct,super_b):
		self._get_flight_info(struct,super_b);
		self._check_flight(struct,super_b);

	def _get_flight_info(self,struct,super_b):
		if super_b.flight is None: super_b.flight = dict();
		to = False;
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item.has_key('stype') and item['stype'] == 'TIME':
				super_b.flight['time'] = item;
			if item.has_key('type') and item['type'] == 'NP':
				if to == True:
					super_b.flight['end'] = item['str'];
				else:
					super_b.flight['start'] = item['str'];
			if item.has_key('stype') and item['stype'] == 'TO':
				to = True;
			elif item.has_key('stype') and item['stype'] == 'FLY':
				to = True;
		if super_b.flight.has_key('start') and super_b.flight.has_key('end'):
			if super_b.flight['start'] == super_b.flight['end']:
				super_b.flight['start'] = 'local';

	def _check_flight(self,struct,super_b):
		if super_b.flight is None:
			struct['step'] = 'set_trip';
			ComFuncs._set_msg(struct,self.data['msg']['set_trip']);
		elif not super_b.flight.has_key('start'):
			struct['step'] = 'set_trip_start';
			ComFuncs._set_msg(struct,self.data['msg']['set_trip_start']);
		elif not super_b.flight.has_key('end'):
			struct['step'] = 'set_trip_end';
			ComFuncs._set_msg(struct,self.data['msg']['set_trip_end']);
		elif not super_b.flight.has_key('time'):
			struct['step'] = 'set_trip_time';
			ComFuncs._set_msg(struct,self.data['msg']['set_trip_time']);
		else:
			ComFuncs._set_msg(struct,self.data['msg']['flight_succ']);
			super_b.get_flight_info();
			struct['step'] = 'sel_flight';
			struct['result']['flight'] = super_b.flight;
		return None;

	def _book_flight(self,struct,super_b):
		if super_b.flight is None:
			self._check_flight(struct,super_b);
			return None;

		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item.has_key('stype') and item['stype'] == 'TIME':
				super_b.book_flight_time(item);
				break;
			if item.has_key('type') and item['type'] == 'NUM':
				super_b.book_flight_fno(item);
				break;

		if super_b.flight.has_key('book'):
			struct['result']['flight'] = super_b.flight;
			ComFuncs._set_msg(struct,self.data['msg']['book_succ']);
		else:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);

#-----------hotel functions-------------
	def _fetch_hotel(self,struct,super_b):
		self._get_hotel_info(struct,super_b);

	def _get_hotel_info(self,struct,super_b):
		if super_b.hotel is None: super_b.hotel = dict();
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item.has_key('stype') and item['stype'] == 'NUNIT':
				level = 3;
				for un in item['stc']:
					if un['stype'] == 'STAR':
						super_b.hotel['level'] = level;
						break;
					if un['stype'] == 'NUM':
						level = int(un['str']);
			if item.has_key('type') and item['type'] == 'NP':
				super_b.hotel['addr'] = item['str'];
			if item.has_key('stype') and item['stype'] == 'NEAR':
				super_b.hotel['atype'] = item['stype'];
		super_b.get_hotel_info();
		if super_b.hotel.has_key('name'):
			struct['result']['hotel'] = super_b.hotel;
			struct['step'] = 'sel_hotel';
			ComFuncs._set_msg(struct,self.data['msg']['sel_hotel']);
		else:
			ComFuncs._set_msg(struct,self.data['msg']['unknow']);
		return None;

	def _book_hotel(self,struct,super_b):
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item.has_key('stype') and item['stype'] == 'NO':
				struct['step'] = 'end';
				ComFuncs._set_msg(struct,self.data['msg']['unknow']);
				return None;

		struct['step'] = 'set_room';
		struct['result']['hotel'] = super_b.hotel;
		ComFuncs._set_msg(struct,self.data['msg']['hotel_pnum']);
		return None;

	def _set_room(self,struct,super_b):
		room = dict();
		num = -1;
		for istr in struct['stseg']:
			if not struct['stc'].has_key(istr): continue;
			item = struct['stc'][istr];
			if item.has_key('type') and item['type'] == 'NUNIT':
				for nit in item['stc']:
					if nit['type'] == 'NUM':
						num = int(nit['str']);
						break;
			elif item.has_key('stype') and item['stype'] == 'PEOPLE':
				if num > 0: room['pum'] = num;
			elif item.has_key('stype') and item['stype'] == 'LIVE':
				num = -1;
		if num > 0:
			room['day'] = num;
			super_b.hotel['room'] = room;
		struct['result']['hotel'] = super_b.hotel;
		ComFuncs._set_msg(struct,self.data['msg']['hotel_succ']);
		return None;
