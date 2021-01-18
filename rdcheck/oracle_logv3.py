#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""'10.1.0.100': {'tab': {'ARCHIVED': {'date': '18-JAN-21', 'size': '6655.31494'}, 'table': [{'name': 'TMP', 'max': '0', 'used': '0'}, {'name': 'TMP', 'max': '0', 'used': '0'}, {'name': 'TMP', 'max': '0', 'used': '0'}, {'name': 'XLINK', 'max': '5120', 'used': '20'}, {'name': 'TEMP', 'max': '0', 'used': '0'}, {'name': 'USERS', 'max': '500', 'used': '19'}, {'name': 'INDEX', 'max': '30720', 'used': '4089'}, {'name': 'SPACE', 'max': '2048', 'used': '368'}, {'name': 'TS', 'max': '76800', 'used': '15065'}, {'name': 'LOGSPACE', 'max': '2048', 'used': '566'}, {'name': 'IDXSPACE', 'max': '6144', 'used': '2282'}, {'name': 'SPACE', 'max': '51200', 'used': '26684'}, {'name': 'DATASPACE', 'max': '24576', 'used': '16317'}, {'name': 'SPACE', 'max': '6144', 'used': '4302'}, {'name': 'SYSAUX', 'max': '32768', 'used': '796'}, {'name': 'SYSTEM', 'max': '32768', 'used': '571'}]}, 'asm': {'asm': [{'name': 'ZJATMDATA/', 'state': 'MOUNTED', 'max': '307200', 'free': '53503', 'off_disk': '0'}, {'name': 'ZJATMFRA/', 'state': 'MOUNTED', 'max': '102400', 'free': '80039', 'off_disk': '0'}]}, 'adg': {'adg': 'now_rows'}}, '"""
import os, sys
import platform
import re
from datetime import datetime, date


datetime = datetime.now()


class Oracle_Log(object):
    basedir = "/data/tmp"
    filename = "daycheck.txt"
    ck_day = date.strftime(datetime.now(), '%Y-%m-%d')
    p_ora_tab = ck_day + " ORA_TAB"
    p_ora_asm = ck_day + " ORA_ASM"
    p_ora_adg = ck_day + " ORA_ADG"

    def get_allfile(self):
        allfile = {}
        if os.path.exists(self.basedir):
            dir_list = os.listdir(self.basedir)
            for ip in dir_list:
                allfile[ip] = self.basedir + '/' + ip + '/' + self.filename
            return allfile
        print("目录不存在")

    # 获取文件中pattern间的内容,返回{ip:"内容",...}
    def get_content(self, pattern):
        content = {}
        for ip, file in self.get_allfile().items():
            try:
                with open(file) as f:
                    reg = re.compile('%s[\s\S]*%s.*?\n' % (pattern, pattern))
                    ret = re.findall(reg, f.read())
                    if ret:
                        content[ip] = ret[0]
            except Exception as  e:
                print(ip, "log文件有问题", e, self.p_ora_tab)
        return content

    def get_ora_tab(self):
        '''清洗table段的数据,返回表空间数据{ip:"表",....}'''
        tables = {}
        data = self.get_content(self.p_ora_tab)
        for ip, content in data.items():
            tables[ip] = self.clean_table(content, ip)
        return tables

    def clean_table(self, content, ip):
        '''表数据分有归档和归档,返回{'archived':{'date':**,'size':**},'table'{{"name":**,'max':**,'used':**},...}}, ip留着拍错用'''
        if not content:
            print(ip, '没有匹配的数据')
            return {}
        table = {}
        log = {}
        location = {}
        if "ARCHIVED" in content:
            # tmp = re.findall(r'^\d*?-.*?-.*/d*$', content)
            tmp = re.findall(r'\d{1,2}-.*-\d{1,2}.*\d\n', content)
            if tmp:
                log["date"] = tmp[0].split()[0].strip()
                log["size"] = tmp[0].split()[1].strip()
        table["ARCHIVED"] = log
        data = re.findall(r'[A-Z]+?\s+?\d+\D+?\d+?\D+?\d+?\D+?\d+?\D+?\d.*\n', content)
        if not data:
            return {'table': {"name": "error"}}
        # 获取字段对应的位置
        ret = re.findall(r'TABLESPACE.*?\n', content)
        for k, v in enumerate(ret[0].split()):
            location[v] = k
        result = []
        for line in data:
            tmp = line.split()
            table_tmp = {}
            table_tmp['name'] = tmp[location.get('TABLESPACE_NAME')]
            table_tmp['max'] = tmp[location.get('MAX')]
            table_tmp['used'] = tmp[location.get('MEGS_USED')]
            result.append(table_tmp)
        table['table'] = result
        return table

    def get_ora_asm(self):
        '''返回表空间数据{ip:"表",....}'''
        tables = {}
        data = self.get_content(self.p_ora_asm)
        for ip, content in data.items():
            tables[ip] = self.clean_asm(content, ip)
        return tables

    def clean_asm(self, content, ip):
        '''表数据分有归档和归档,返回{'asm':{{"name":**,'max':**,'used':**},...}}, ip留着拍错用'''
        if not content:
            print(ip, "asm没有匹配的数据")
            return []
        table = {}
        location = {}
        data = re.findall(r'\S+?.+\w+?.*?[YN]+.*?\d+.*?\n', content)
        # content无表数据有错误数据会运行到这
        if not data:
            print(ip, "asm有错误的数据")
            return {'asm': {"name": "error"}}
        # 获取字段对应的位置
        ret = re.findall(r'State.*?\n', content)
        for k, v in enumerate(ret[0].split()):
            location[v] = k
        # 获取字段对应的位置
        result = []
        for line in data:
            tmp = line.split()
            table_tmp = {}
            #print(tmp)
            table_tmp['name'] = tmp[location.get('Name')]
            table_tmp['state'] = tmp[location.get('State')]
            table_tmp['max'] = tmp[location.get('Total_MB')]
            table_tmp['free'] = tmp[location.get('Free_MB')]
            table_tmp['off_disk'] = tmp[location.get('Offline_disks')]
            result.append(table_tmp)
        table['asm'] = result
        return table

    def get_ora_adg(self):
        '''返回表空间数据{ip:{'adg':"num"}}'''
        tables = {}
        data = self.get_content(self.p_ora_adg)
        for ip, content in data.items():
            tables[ip] = self.clean_adg(content, ip)
        return tables

    def clean_adg(self,content,ip):
        if "Success" not in content:
            return {'adg': 'failed'}
        elif "no rows selected" in content:
            return {'adg': 'now_rows'}
        tmp = re.findall(r'THREAD# NOT[\s\S]*?(\d+).*?(\d+)(\W+(\d+)\W+?(\d+))?', content)
        if tmp[0][4]:
            return {'adg': max([tmp[0][1], tmp[0][4]])}
        else:
            return {'adg': tmp[0][1]}



    def get_metric(self):
        tab = self.get_ora_tab()
        asm = self.get_ora_asm()
        adg = self.get_ora_adg()
        metric = {}
        for ip , data in tab.items():
            metric[ip] = {
                'tab': data,
                'asm': asm.get(ip),
                'adg': adg.get(ip)
            }

        return metric

t = Oracle_Log()
r = t.get_metric()
print(r)



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

# def main():
#    curdate = datetime.today()
#    data = get_roundcheck()
#    rcfile = "linux_%s_%s.toml" % (data["global"]["ip"], curdate.strftime("%Y%m%d%H"))
#    abs_rcfile = os.path.join('/home/cx/rdcheck/result', rcfile)
#
#    try:
#        dict_dump_tomlfile(data, abs_rcfile)
#    except Exception as e:
#        print(e)
#
#
# if __name__ == "__main__":
#    main()
