# !/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from xml.dom.minidom import parse
import xml.dom.minidom

import sys
from lxml import etree
import html
from org.ith.learn.util.TUtils import KCEBean, XmlStdin, highlight, auto_escape
path_of_android = "../../../../docs/i18n/merge.xml"


def main():
    _list_kce_ = parse_string_as_kce(path_of_android)
    list.sort(_list_kce_)
    write_kce_to_path(_list_kce_, "./thhhhhhh.xml")


def parse_string_as_kce(path_of_string, kce_value='cn'):
    """
    这里很奇怪 如果读取string.xml格式的时候 有CDATA的 访问到是None
    但是如果是merge以后的values.xml 过滤出string的tag再去读,这时的CDATA并不是None
    有命名空间的不行  CDATA不是None
    <resources xmlns:ns1="http://schemas.android.com/tools">
    """
    with open(path_of_string, 'r') as fobj:
        bxml = fobj.read()
        bxml = bytes(bxml, encoding='utf-8')

    parser = etree.XMLParser(strip_cdata=False)
    root = etree.fromstring(bxml, parser=parser)

    list_kce = []

    try:
        for item in root:
            key = item.get("name")
            value = item.text
            # 特殊处理CDATA的情况
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

            # print("{:<50s}".format(key), '\t', value)
            list_kce.append(kce)

    except ValueError as e:
        # print(key, e)
        raise

    return list_kce


def write_kce_to_path(list_of_kce, path, sort=False, key='cn'):
    print('write_kce_to_path: ', highlight(path, 1))

    for kce in list_of_kce:
        kce.cn = auto_escape(kce.cn)
        kce.en = auto_escape(kce.en)

    list_of_kce = sorted(list_of_kce)

    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'resources', None)
    resources_root = dom.documentElement
    try:
        for kce in list_of_kce:
            string_node = dom.createElement('string')
            string_node.setAttribute("name", str(kce.key))
            str_key_value = str(kce.cn)
            if key != 'cn':
                str_key_value = str(kce.en)
            value = dom.createTextNode(str_key_value)
            string_node.appendChild(value)
            resources_root.appendChild(string_node)

        txmlstdin = XmlStdin()
        sys.stdin = txmlstdin
        dom.writexml(sys.stdin, addindent='\t', newl='\n', encoding='utf-8')
        transed_str = txmlstdin.toString()

        if not os.path.exists(path):
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))

        with open(path, 'w') as f:
            f.write(transed_str)

        if not sort:
            return

        lines = list()
        with open(path, 'r') as f:
            for line in f:
                lines.append(line)
        lines = sorted(lines)
        last = lines[len(lines) - 2:]
        lines.insert(0, last[0])
        lines.insert(1, last[1])
        lines = lines[:- 2]
        outer = ''
        for line in lines:
            outer += line
        with open(path, 'w') as f:
            f.write(outer)

    except Exception as err:
        print("==================", path, err)
        raise


if __name__ == "__main__":
    sys.exit(main())
