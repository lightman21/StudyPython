import time

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
    gener_dict(pull_ios_trans())


def gener_dict(ios_kce_list):
    now_date = time.strftime("%Y_%m_%d", time.localtime())
    to_write_lines = []
    kv_list = dict()
    for kce in ios_kce_list:
        kv_list[kce.cn] = kce.en
    # d[0] key d[1] value
    kv_list = sorted(kv_list.items(), key=lambda d: d[0], reverse=True)

    ios_kce_list.clear()
    for kv in kv_list:
        bean = KCEBean(key=md5(kv[0]), cn=kv[0], en=kv[1])
        ios_kce_list.append(bean)

    for kce in ios_kce_list:
        if len(kce.key) > 0 and len(kce.cn) > 0 and len(kce.en) > 0:
            v_cn = auto_escape(kce.cn).strip()
            v_en = auto_escape(kce.en).strip()
            line = '<kce key="{}" cn="{}" en="{}"/>\n'.format(kce.key, v_cn, v_en)
            to_write_lines.append(line)

    with open('./{}_ios_kce_dict_puc.xml'.format(now_date), 'w') as out:
        out.writelines(to_write_lines)


def pull_ios_trans():
    command = 'git archive develop --remote=ssh://git@gitlab.shishike.com:38401/c_iphone/OnMobile.git  ' \
              'OnMobile/Resource/en.lproj/OnMobileLocalizable.strings | tar -x && cp ' \
              'OnMobile/Resource/en.lproj/OnMobileLocalizable.strings ../../../../docs/i18n/ && rm -rf OnMobile '
    exec_cmd(command)
    return read_ios_as_kce('../../../../docs/i18n/OnMobileLocalizable.strings')


def read_ios_as_kce(path=ios_path):
    # os.chdir(os.path.dirname(path))
    # exec_cmd('git pull -r')
    # "+ 添加收款银行卡" = " + add bank card to collect money";
    pattern = r'"(.*)" = "(.*)"'
    key_start = '_ios_key_'
    kce_list = []
    with open(path, 'r') as rin:
        content = rin.read()
        rets = re.findall(pattern, content)
        for ret in rets:
            b = KCEBean(key=key_start + md5(ret[0]), cn=remove_punctuation(auto_escape(ret[0])),
                        en=remove_punctuation(auto_escape(ret[1])))
            kce_list.append(b)
    return kce_list


if __name__ == '__main__':
    main()
