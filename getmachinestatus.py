#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# machine_status.py  »ñ¾»úʹÓÐϢ¡¢½ø̬ºÍ¬½Óé
# created by vince67 (nuovince@gmail.com)
# May 2014
  
  
import datetime
import os
import psutil as ps                       # psutil¿âèÏ°²װ
from pymongo import Connection
import time
import socket
import uuid
  
  
class MachineStatus(object):
  
    #   ³õ¯
    def __init__(self):
        self.MAC = None
        self.IP = None
        self.cpu = {}
        self.mem = {}
        self.process = {}
        self.network = {}
        self.status = []                    #  [cpuʹÓÂ£¬ Ä´æÓÂ£¬ ½øĿ£¬ establishedl½Óý     self.get_init_info()
        self.get_status_info()
  
    #  ËÖ»ú״̬
    def run(self):
        self.get_status_info()
        self.save_status_to_db()
  
    def save_status_to_db(self):
        print self.status
  
    #  Ê¾Ýռ¯
    def get_init_info(self):
        self.cpu = {'cores' : 0,            #  cpuÂ¼­ºËý                'percent' : 0,          #  cpuʹÓÂ
                    'system_time' : 0,      #  ÄºË¬ϵͳʱ¼ä                   'user_time' : 0,        #  Ó»§̬ʱ¼ä                   'idle_time' : 0,        #  ¿ÕÐ±¼ä                   'nice_time' : 0,        #  niceʱ¼ä»¨·Ñڵ÷øÏ¼¶ÉµÄ±¼ä                    'softirq' : 0,          #  È¼þÖ¶Ï±¼ä                   'irq' : 0,              #  Ö¶Ï±¼ä                   'iowait' : 0}           #  IOµȴý        self.mem = {'percent' : 0,
                    'total' : 0,
                    'vailable' : 0,
                    'used' : 0,
                    'free' : 0,
                    'active' : 0}
        self.process = {'count' : 0,        #  ½øĿ
                        'pids' : 0}         #  ½ø±ð        self.network = {'count' : 0,        #  l½ÓÜý                    'established' : 0}  #  establishedl½Óý    self.status = [0, 0, 0, 0]          #  cpuʹÓÂ£¬Ä´æÓÂ£¬ ½ø£¬ establishedl½Óý    self.get_mac_address()
        self.get_ip_address()
  
    #  »ñ´̬Á±í   def get_status_info(self):
        self.get_cpu_info()
        self.get_mem_info()
        self.get_process_info()
        self.get_network_info()
        self.status[0] = self.cpu['percent']
        self.status[1] = self.mem['percent']
        self.status[2] = self.process['count']
        self.status[3] = self.network['established']
  
    #  »ñac
    def get_mac_address(self):
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        self.MAC = ":".join([mac[e : e+2] for e in range(0, 11, 2)])
  
    #  »ñp
    def get_ip_address(self):
        tempSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tempSock.connect(('8.8.8.8', 80))
        addr = tempSock.getsockname()[0]
        tempSock.close()
        self.IP = addr
  
    #  »ñpuÐϢ
    def get_cpu_info(self):
        self.cpu['cores'] = ps.cpu_count()
        self.cpu['percent'] = ps.cpu_percent(interval=2)
        cpu_times = ps.cpu_times()
        self.cpu['system_time'] = cpu_times.system
        self.cpu['user_time'] = cpu_times.user
        self.cpu['idle_time'] = cpu_times.idle
        self.cpu['nice_time'] = cpu_times.nice
        self.cpu['softirq'] = cpu_times.softirq
        self.cpu['irq'] = cpu_times.irq
        self.cpu['iowait'] = cpu_times.iowait
  
    #  »ñemoryÐϢ
    def get_mem_info(self):
        mem_info = ps.virtual_memory()
        self.mem['percent'] = mem_info.percent
        self.mem['total'] = mem_info.total
        self.mem['vailable'] = mem_info.available
        self.mem['used'] = mem_info.used
        self.mem['free'] = mem_info.free
        self.mem['active'] = mem_info.active
  
    #  »ñøϢ
    def get_process_info(self):
       pids = ps.pids()
       self.process['pids'] = pids
       self.process['count'] = len(pids)
  
    #  »ñø¾Ý    def get_network_info(self):
        conns = ps.net_connections()
        self.network['count'] = len(conns)
        count = 0
        for conn in conns:
           if conn.status is 'ESTABLISHED':
               count = count + 1
        self.network['established'] = count
  
if __name__ == '__main__':
    MS = MachineStatus()
    print MS.IP, '\n', MS.MAC, '\n', MS.cpu, '\n', MS.mem, '\n', MS.status
