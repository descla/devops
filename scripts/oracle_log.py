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
    talbe_pat = ck_day + " ORA_TAB"

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
                print(ip, "log文件有问题", e, self.talbe_pat)
        return content
        # 清洗table段的数据,返回表空间数据{ip:"表",....}

    def clean_tables_data(self):
        tables = {}
        data = self.get_content(self.talbe_pat)
        for ip, content in data.items():
            tables[ip] = self.clean_table(content)
        return tables

    def clean_table(self, content):
        '''表数据分有归档和归档,返回{'ARCHIVED':{'DATE':**,'SIZE':**},'table'{{"表名":**,'MAX':**,'USED':**},...}}'''
        table = {}
        log = {}
        data = []
        table_tmp = {}
        if "ARCHIVED" in content:
            tmp = content.strip().split('\n')
            log["DATE"] = tmp[-2].split('\t')[0].strip()
            log["SIZE"] = tmp[-2].split('\t')[1].strip()
        data = content.strip().split('\n')
        print(data)
        table["ARCHIVED"] = log
        # list删除,必须从后删除
        for i in range(len(data)-1, -1, -1):
            if '\t' not in data[i]:
                del data[i]
        for line in data[1:-2]:
            tmp = line.split('\t')
            table_tmp[tmp[0]] = {'MAX': tmp[-1].strip().split()[-1], 'USED': tmp[-4].strip()}
        table['table'] = table_tmp
        return table



    def get_metric(self):
        metric = {
        }
        return metric


test = Oracle_Log()
t = test.clean_tables_data()


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
