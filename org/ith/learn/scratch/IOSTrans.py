from org.ith.learn.OhMyEXCEL import excel_to_xml, xml_to_excel
from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import open_excel_as_list, read_xml_as_kce_list, KCEBean, highlight, modify_time, md5, \
    auto_escape, extra_chinese, remove_punctuation, is_contains_chinese, exec_cmd

import re
import difflib
import os

ios_path = '/Users/toutouhiroshidaiou/keruyun/proj/ios_proj/OnMobile/OnMobile/Resource/en.lproj/OnMobileLocalizable' \
           '.strings '


def main():
    print(os.path.dirname(ios_path.strip()))
    read_ios_as_kce(ios_path.strip())


def read_ios_as_kce(path=ios_path):
    os.chdir(os.path.dirname(path))
    exec_cmd('git pull -r')
    # "+ 添加收款银行卡" = " + add bank card to collect money";
    pattern = r'"(.*)" = "(.*)"'
    key_start = '_ios_key_'
    kce_list = []
    with open(path, 'r') as rin:
        content = rin.read()
        rets = re.findall(pattern, content)
        for ret in rets:
            b = KCEBean(key=key_start + md5(ret[0]), cn=auto_escape(ret[0]), en=auto_escape(ret[1]))
            kce_list.append(b)

    return kce_list


if __name__ == '__main__':
    main()
