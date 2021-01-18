#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ************************************************************************#
# File Name   : linux_roundcheck.py
# Funtion     : get linux host metric
# Description : get host metric and output a toml file
#    for compatibility in lower release python, use os.popen
#    for reduce external dependency library, not import json/toml
#
#    低版本python不支持列表表达式,要用循环.python 2.3不支付set
#    使用说明： linux_roundcheck.py 192.168.1.1(ip地址)
#    如果不加ip,会自取一个ipv4地址
# ************************************************************************#

import os, sys
import platform
import re
from datetime import datetime

last_worktime = 0
last_idletime = 0


def usage_percent(use, total):
    """ 计算使用率百分比
    @param use: float; use value
    @param total: float
    @return: float
    """
    try:
        ret = (use / total) * 100
    except ZeroDivisionError:
        ret = 0.0
    return round(ret, 2)


def get_dist():
    # ('redhat', '7.7', 'Maipo')
    return platform.dist()


def get_service_state(service_name):
    """ check server status
    @param service_name: str
    @return status: int; Y 成功, N 失败
    """
    cmd = ""
    status = ""

    dist = get_dist()
    if dist[0].lower() in ("redhat", "centos"):
        if int(dist[1].split(".")[0]) >= 7:
            cmd = "systemctl status %s 2>/dev/null" % service_name
        else:
            cmd = "service %s status 2>/dev/null" % service_name

    elif dist[0].lower() == "suse":
        cmd = "ps -eo cmd|grep %s|grep -v grep" % service_name  # TODO
    elif dist[0].lower() == "ubuntu":
        cmd = ""  # TODO
    else:
        cmd = "xxx"

    if cmd:
        result = os.popen(cmd).read().strip()
        if dist[0].lower() in ("redhat", "centos") and "running" in result:
            status = "Y"
        elif dist[0].lower() == "suse" and result:
            status = "Y"
        else:
            status = "N"
    return status


def get_cpu():
    """ get cpu usage
    @return: float
    """
    global last_worktime, last_idletime
    f = open("/proc/stat", "r")
    line = ""
    while not "cpu" in line:
        line = f.readline()
    f.close()
    spl = line.split(" ")
    worktime = int(spl[2]) + int(spl[3]) + int(spl[4])
    idletime = int(spl[5])
    dworktime = (worktime - last_worktime)
    didletime = (idletime - last_idletime)
    rate = float(dworktime) / (didletime + dworktime)
    last_worktime = worktime
    last_idletime = idletime
    if (last_worktime == 0):
        return 0
    return round(rate * 100, 2)


def check_ntp_config():
    """ 检查ntp.conf里的配置是否符合标准
    @return: str; E abnormal, Y config correct, N config error
    """
    ntp_config = "N"

    if not os.path.exists("/etc/ntp.conf"):
        return "E"

    ntp_server = [
        'ntp1.bocd.com.cn',
        'ntp2.bocd.com.cn',
    ]

    # 检查ntp.conf里配置的server是否ntp_server, 在则正常
    cmd = ("egrep '%s' /etc/ntp.conf" % "|".join(ntp_server))
    result = os.popen(cmd).readlines()
    if result:
        for line in result:
            if line.strip().split()[1] in ntp_server:
                return "Y"
    else:
        return "N"

    return ntp_config


def get_ntp():
    """"""
    ntp = {"ntp_status": "",
           "ntp_config": check_ntp_config(),
           "ntp_offset": ""
           }

    # check ntp_status
    if get_service_state("ntpd") == "Y" or get_service_state("chronyd") == "Y":
        ntp["ntp_status"] = "Y"
    else:
        ntp["ntp_status"] = "N"
    # check ntp_relay
    cmd = "ntpq -p 2>/dev/null|grep '^*'|awk '{print $9}'"
    result = os.popen(cmd).read().strip()
    if len(result) > 0:
        ntp["ntp_offset"] = float(result)
    else:
        ntp["ntp_offset"] = 999.0  # 异常值
    return ntp

# 获取所有网卡ip, 用于文件命名
def get_allip():
    """ get all ip in host, contain netmask
    @return: list, eg: [ ip1/24, ip2/22,...], if null, return []
    """
    cmd = "ip -family inet -oneline addr|egrep 'em|ens|eno|virbr|eth|bond|team'|awk '{print $4}' "
    all_ip = os.popen(cmd).readlines()
    all_ip = [ip.strip() for ip in all_ip]
    return all_ip


def get_mem():
    try:
        f = open('/proc/meminfo', 'r')
        for line in f:
            if line.startswith('MemTotal:'):
                mem_total = float(line.split()[1])
            elif line.startswith('MemFree:'):
                mem_free = float(line.split()[1])
            elif line.startswith('Buffers:'):
                mem_buffer = float(line.split()[1])
            elif line.startswith('Cached:'):
                mem_cache = float(line.split()[1])
            elif line.startswith('SwapTotal:'):
                vmem_total = float(line.split()[1])
            elif line.startswith('SwapFree:'):
                vmem_free = float(line.split()[1])
            else:
                continue
        f.close()
    except:
        return None
    physical_percent = usage_percent(mem_total - (mem_free + mem_buffer + mem_cache), mem_total)
    virtual_percent = 0.0
    if vmem_total > 0:
        virtual_percent = usage_percent((vmem_total - vmem_free), vmem_total)
    return physical_percent, virtual_percent


# 取本地使用率最大的分区
def get_fs_used():
    fs_data_used = -1
    cmd = "df -lkTP|egrep  'ext|xfs|vxfs|tmpfs'|awk '{print $NF,$(NF-1)}'"
    fs_data = []
    result = os.popen(cmd).readlines()
    for line in result:
        fs, used = line.strip().split()
        if used == '100%':
            fs_used = 99
        else:
            fs_used = int(used.rstrip('%'))
        fs_data.append(fs_used)
    if fs_data:
        fs_data_used = max(fs_data)  # 取所有数据分区中使用率最大的一个

    return fs_data_used


def get_fs():
    """获取文件系统状态"""
    filesystem = []
    cmd = "df --block-size=1 -lTP|egrep 'ext|xfs|vxfs|tmpfs'|awk '{print $NF,$(NF-1),$(NF-2),$2}'"
    result = os.popen(cmd).readlines()
    for line in result:
        fs, used, free, fs_type = line.strip().split()
        if used == '100%':
            fs_used = 99
        else:
            fs_used = int(used.rstrip('%'))
        filesystem.append({"fs": fs, "fs_type": fs_type, "used": fs_used, "free": int(free)})
    return filesystem


def get_inode_used():
    cmd = "df -iTP|egrep 'ext|xfs|tmpfs|nfs'|awk '{print $NF,$(NF-1)}'"
    result = os.popen(cmd).readlines()
    inode_used = []
    for line in result:
        iused = line.strip().split()[1]
        iused = int(iused.replace('%', ''))
        inode_used.append(iused)
    return max(inode_used)


def get_nfs():
    """如果有nfs返回最大的分区, 如果无返回N"""
    cmd = "df -kTP|grep nfs|awk '{print $NF,$(NF-1)}'"
    nfs_data = []
    result = os.popen(cmd).readlines()
    if result:
        for line in result:
            fs, used = line.strip().split()
            if used == '100%':
                fs_used = 99
            else:
                fs_used = int(used.rstrip('%'))
            nfs_data.append(fs_used)
        nfs_flag = max(nfs_data)  # 取所有数据分区中使用率最大的一个
    else:
        nfs_flag = 'N'

    return nfs_flag


def get_zabbix():
    return get_service_state("zabbix-agent")


def get_global(ip):
    cmd = "hostname"
    hostname = ""
    result = os.popen(cmd).readlines()
    if result:
        hostname = result[0].strip()
    rc_global = {
        "ip": ip,
        "hostname": hostname,
        "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return rc_global

# 读取fstab文件需要挂载的文件，根据df命令判断挂载状态，正确返回R，错误返回W
def get_mount_status():
    fs_mounted = []
    fs_fstab = []
    uuid = []
    cmd = "df -lkTP|egrep -v Filesystem|awk '{print $1}'"
    result = os.popen(cmd).readlines()
    for fs in result:
        fs_mounted.append(fs.strip())

    cmd = "egrep -v '^#|^$|swap' /etc/fstab | awk '{print $1}'"
    result = os.popen(cmd).readlines()
    # 如果fstab挂载使用的是UUID, 需要找到对应的分区
    for line in result:
        if "UUID" in line:
            uuid.append(line.strip().replace('UUID=', ''))
        else:
            fs_fstab.append(line.strip())
    if uuid:
        cmd = "/usr/bin/ls -l /dev/disk/by-uuid/| grep / | awk '{print $NF, $(NF-2)}'"
        result = os.popen(cmd).readlines()
        blkid = [id.strip().replace('../../', '/dev/').split() for id in result]
        print(uuid)
        print(blkid)
        for line in blkid:
            for id in uuid:
                if id in line[1]:
                    fs_fstab.append(line[0])
    # 判断挂载是否是包含关系, 没用set, 为了兼容
    for i in fs_fstab:
        if i not in fs_mounted:
            return "W"
    return "R"

def get_metric():
    mem_used, swap_used = get_mem()
    fs_data_used = get_fs_used()
    ntp = get_ntp()
    filesystem = get_fs()
    fs_data_free = -1
    data_free = []
    fs_nfs = get_nfs()

    for fs in filesystem:
        data_free.append((fs["used"], fs["free"]))
        if fs_data_used != -1:
            for u, f in data_free:
                if u == fs_data_used:
                    fs_data_free = f

    metric = {
        "cpu_used": get_cpu(),
        "mem_used": mem_used,
        "swap_used": swap_used,
        "fs_data_used": fs_data_used,
        "fs_nfs": fs_nfs,
        "fs_data_free": fs_data_free,
        "fs_mount_status": get_mount_status(),
        "inode_used": get_inode_used(),
        "ntp_offset": ntp["ntp_offset"],
        "ntp_config": ntp["ntp_config"],
        "ntp_status": ntp["ntp_status"],
        "zabbix_agent": get_zabbix(),
    }
    return metric


def get_roundcheck():
    if len(sys.argv) > 1:
        ip = str(sys.argv[1])
    else:
        cmd = "ip -family inet -oneline addr|egrep 'em|ens|eno|virbr|eth|bond|team'|awk '{print $4}' "
        all_ip = os.popen(cmd).readlines()
        all_ip = [ip.strip().split('/') for ip in all_ip]
        ip = all_ip[0][0]
    rc_data = {
        "global": get_global(ip=ip),
        "metric": get_metric(),
    }
    return rc_data


def dict_dump_tomlfile(data, tomlfile):
    """ write data to tomlfile
    @param data: dict
    @param tomlfile: str, toml style filename
    @return: boolean
    """
    operate_status = True
    try:
        f = open(tomlfile, 'w')
    except Exception as e:
        operate_status = False
    else:
        for k, v in data.items():
            f.write('[%s]\n' % k)
            for kk, vv in v.items():
                # 防止字符串内含单双引号干扰, 用三引号包围
                if kk == "msg":
                    wrapper_v = '"""%s"""' % vv
                elif isinstance(vv, str):
                    wrapper_v = '"%s"' % vv
                else:
                    wrapper_v = vv
                f.write('%s = %s\n' % (kk, wrapper_v))
            f.write('\n')
        f.close()

    return operate_status


def main():
    curdate = datetime.today()
    data = get_roundcheck()
    rcfile = "linux_%s_%s.toml" % (data["global"]["ip"], curdate.strftime("%Y%m%d%H"))
    abs_rcfile = os.path.join('/home/cx/rdcheck/result', rcfile)

    try:
        dict_dump_tomlfile(data, abs_rcfile)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
