# !/usr/bin/python
# -*- coding: UTF-8 -*-

import html
import sys

from lxml import etree

from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import KCEBean

# path_of_merge = '../../../docs/merge/merge_bk.xml'
"""
/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/app/build/intermediates/incremental/mergeOfficialEnvGrdResources/merged.dir
"""

path_of_merge = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/app/build/intermediates/incremental' \
                '/mergeOfficialEnvGrdResources/merged.dir/values/values.xml'


def remove_namespace(xml_line_list):
    """
    去除文件中的namespace相关 否则CDATA异常
    :param xml_line_list:
    :return:
    """
    lines = []
    ns = ''
    for line in xml_line_list:
        if line.__contains__('xmlns'):
            ns = line.split('=')[0].split(":")[1] + ':'
            start = line.index('xmlns')
            end = line.index('>')
            tmp_line = line[:start].strip() + line[end:]
            lines.append(tmp_line)
        else:
            lines.append(str(line))

    return ''.join(lines).replace(ns, '')


def extra_merged_xml(merged_path, out_path="./new_merged.xml"):
    with open(merged_path, 'r') as fobj:
        xml_str = remove_namespace(fobj.readlines())
        bxml = bytes(xml_str, encoding='utf-8')
        parser = etree.XMLParser(strip_cdata=False)
        root = etree.fromstring(bxml, parser=parser)

        kce_value = 'cn'

        try:
            list_kce = []

            for item in root:

                if item.tag != 'string':
                    continue

                key = item.get("name")
                value = item.text

                # 特殊处理CDATA 和 <string name="abc"/> 的情况
                if value is None:
                    ss = etree.tostring(item)
                    ss = str(ss, encoding='utf-8')
                    if ss.__contains__('>') and ss.__contains__('</string>'):
                        start = ss.index('>') + 1
                        end = ss.index('</string>')
                        html_str = ss[start:end]
                        txt = html.unescape(html_str)
                        value = txt
                    else:
                        value = ''

                if kce_value == 'cn':
                    kce = KCEBean(key, cn=value, en='')
                else:
                    kce = KCEBean(key, cn='', en=value)

                list_kce.append(kce)
        except ValueError as e:
            print(e, key)
            raise

        write_kce_to_path(list_kce, out_path, sort=False)


def main():
    extra_merged_xml(path_of_merge)


if __name__ == "__main__":
    sys.exit(main())
