import os
import sys
import time

from org.ith.learn.OhMyEXCEL import excel_to_xml, xml_to_excel
from org.ith.learn.scratch.Trans535 import big_dict
from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import open_excel_as_list, read_xml_as_kce_list, KCEBean, highlight, modify_time, md5, \
    auto_escape, extra_chinese, remove_punctuation, is_contains_chinese, exec_cmd
import re
import difflib


def search_kce(search, compare_by='cn', dict_path='../../../../docs/dicts/2020_04_20_kce_dict.xml',
               up_threshold=1.0,
               down_thread=0.9
               ):
    kce_list = list()
    with open(dict_path, 'r') as rin:
        lines = rin.readlines()
        pattern = r'<kce key="(.*)" cn="(.*)" en="(.*)"'
        for line in lines:
            rets = re.findall(pattern, line)
            rets = rets[0]
            kce = KCEBean(key=rets[0], cn=rets[1], en=rets[2])
            if compare_by == 'key':
                if down_thread < approximately_equal_to(kce.key, search) <= up_threshold:
                    # if kce.key == search:
                    return kce
            elif compare_by == 'en':
                if down_thread < approximately_equal_to(kce.en, search) <= up_threshold:
                    # if kce.en == search:
                    return kce
            else:  # 比cn默认
                if down_thread < approximately_equal_to(kce.cn, search) <= up_threshold:
                    # if kce.cn == search:
                    return kce


def approximately_equal_to(s1, s2):
    return difflib.SequenceMatcher(lambda x: x in ':：！!?。', s1, s2).quick_ratio()


def work():
    string = '<kce key="about_text" cn="关于" en="About" />'
    matcher = r'<kce key="(.*)" cn="(.*)" en="(.*)"'
    rets = re.findall(matcher, string)
    print(rets)

    big_kce_list = big_dict()
    cn_set = set()
    no_dup = list()
    for big in big_kce_list:
        print(big)
        if big.cn not in cn_set:
            cn_set.add(big.cn)
            no_dup.append(big)

    print('big size ', len(big_kce_list), ', cn size ', len(cn_set))
    now_date = time.strftime("%Y_%m_%d", time.localtime())
    to_write_lines = []
    for kce in no_dup:
        if len(kce.key) > 0 and len(kce.cn) > 0 and len(kce.en) > 0:
            v_cn = auto_escape(kce.cn).replace('please', 'pls').replace('Please', 'Pls').capitalize()
            v_en = auto_escape(kce.en).capitalize()
            line = '<kce key="{:<40}" cn="{}" en="{}"/>\n'.format(kce.key, v_cn, v_en)
            to_write_lines.append(line)

    with open('./{}_kce_dict.xml'.format(now_date), 'w') as out:
        out.writelines(to_write_lines)

    pass


def main(argv=None):
    if argv is None:
        argv = sys.argv

    print(search_kce("唐浩"))
    pass


if __name__ == '__main__':
    main()
