#!/usr/bin/python
# -*- coding:utf8 -*-
# Email:chenwx716@163.com
__author__ = 'chenwx'
 
import paramiko
import re
from time import sleep
 
linux_info=(
            ['ub-pydev','192.168.18.181'],
            ['ub-developer','192.168.18.188'],
            ['ct-developer','192.168.18.189']
            )
 
server_user='root'
server_pw='oyj7766'
server_info={}
 
def cpu_r(cpu_stat):
    # 返回CPU当前的总时间片和空闲时间片信息的数据
    sys_cpu_info_t = re.findall(r'cpu .*\d',cpu_stat)
    cpu_z_str = ' '.join(sys_cpu_info_t)
    cpu_z_list = list(cpu_z_str.split())
    cpu_z_list.remove("cpu")
 
    f_line_a=[]
    for i in cpu_z_list:
        i=int(i)
        f_line_a.append(i)
    total = sum(f_line_a)
    idle = f_line_a[3]
    return total,idle
 
def meminfo_disc(meminfo_r):
    # 返回内存使用信息的一个字典，取值需要 /proc/meminfo 的内容
    aa = re.sub(r' kB','',meminfo_r)
    bb = re.sub(r' +','',aa)
    cc = re.sub(r'\n',':',bb)
    dd = cc.split(":")
    meminfo_d = {}
 
    while len(dd)>1:
        meminfo_d[dd[0]]=dd[1]
        del dd[0:2]
    return meminfo_d
 
for i in linux_info:
    server_id=i[0]
    server_ip=i[1]
    ss = paramiko.SSHClient()
    ss.set_missing_host_key_policy(paramiko.AutoAddPolicy())
 
    ss.connect(server_ip,22,server_user,server_pw)
    stdin,stdout,stderr=ss.exec_command('cat /proc/stat')
    sys_cpu_stat = stdout.read()
 
    stdin,stdout,stderr=ss.exec_command('cat /proc/meminfo')
    meminfo_r = stdout.read()
 
    total_a,idle_a=cpu_r(sys_cpu_stat)
    sleep(3)
    stdin,stdout,stderr=ss.exec_command('cat /proc/stat')
    sys_cpu_stat = stdout.read()
    total_b,idle_b=cpu_r(sys_cpu_stat)
    ss.close()
 
    sys_idle = idle_b - idle_a
    sys_total = total_b - total_a
    sys_us = sys_total - sys_idle
    cpu_a = (float(sys_us)/sys_total)*100
    cpu_b = str(round(cpu_a,2))+'%'
 
    meminfo_key = meminfo_disc(meminfo_r)
 
    mem_kx = int(meminfo_key.get('MemTotal'))-int(meminfo_key.get('MemFree'))-int(meminfo_key.get('Buffers'))-int(meminfo_key.get('Cached'))
    mem_kx_l = (float(mem_kx)/int(meminfo_key.get('MemTotal')))*100
    mem_kx_lv = str(round(mem_kx_l))+'%'
 
    swap_user = float(meminfo_key.get('SwapTotal'))-int(meminfo_key.get('SwapFree'))/float(meminfo_key.get('SwapTotal'))
    swap_user_l = (float(meminfo_key.get('SwapTotal'))-int(meminfo_key.get('SwapFree')))/int(meminfo_key.get('SwapTotal'))*100
    swap_user_lv = str(round(swap_user_l))+'%'
 
    server_info_list=[server_id,server_ip,cpu_b,mem_kx_lv,swap_user_lv]
    server_info[server_id]=server_info_list
    # 输出一个字典
 
print server_info