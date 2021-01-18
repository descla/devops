#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
                    reg = re.compile('%s[\s\S]*%s' % (pattern, pattern))
                    ret = re.findall(reg, f.read())
                    if ret:
                        content[ip] = ret[0]
            except Exception as  e:
                print(ip, "log文件有问题", e, self.p_ora_tab)
        return content

    def get_orc_tab(self):
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
            tmp = content.strip().split('\n')
            log["date"] = tmp[-2].split('\t')[0].strip()
            log["size"] = tmp[-2].split('\t')[1].strip()
        data = content.strip().split('\n')
        table["ARCHIVED"] = log
        # list删除,必须从后删除
        for i in range(len(data) - 1, -1, -1):
            if '\t' not in data[i]:
                del data[i]
        # content无表数据有错误数据会运行到这
        if not data:
            return {'table': {"name": "error"}}
        # 获取字段对应的位置
        for k, v in enumerate(data[0].split()):
            location[v] = k
        result = []
        for line in data[1:-2]:
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
            print(ip, "没有匹配的数据")
            return {}
        table = {}
        location = {}
        data = content.strip().split('\n')
        #print(data)
        # list删除,必须从后删除
        for i in range(len(data) - 1, -1, -1):
            if 'stty' in data[i] or 'INFO' in data[i] or 'CHECK RESULT' in data[i] or 'asmcmd' in data[i]:
                del data[i]
        # content无表数据有错误数据会运行到这
        if not data:
            print(ip, "有错误的数据")
            return {'asm': {"name": "error"}}
        # 获取字段对应的位置

        for k, v in enumerate(data[0].split()):
            location[v] = k
        result = []
        for line in data[1:]:
            tmp = line.split()
            table_tmp = {}
            table_tmp['name'] = tmp[location.get('Name')]
            table_tmp['max'] = tmp[location.get('Total_MB')]
            table_tmp['free'] = tmp[location.get('Free_MB')]
            table_tmp['off_disk'] = tmp[location.get('Offline_disks')]
            result.append(table_tmp)
        table['asm'] = result
        return table
    def get_metric(self):
        metric = {
        }
        return metric

t = Oracle_Log()
r = t.get_ora_asm()
for k,v in r.items():
    print(k,v)




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
