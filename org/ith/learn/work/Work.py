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
                if down_thread <= approximately_equal_to(kce.key, search) <= up_threshold:
                    # if kce.key == search:
                    return kce
            elif compare_by == 'en':
                if down_thread <= approximately_equal_to(kce.en, search) <= up_threshold:
                    # if kce.en == search:
                    return kce
            else:  # 比cn默认
                if down_thread <= approximately_equal_to(kce.cn, search) <= up_threshold:
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


def gener_diff(new_path, old_path, diff_path='./diff_old_new_2.xml'):
    kce_list_new = read_xml_as_kce_list(new_path)
    kce_list_old = read_xml_as_kce_list(old_path)
    key_olds = []
    for kce in kce_list_old:
        key_olds.append(kce.key)

    diff_kce = set()
    count = 0

    for new in kce_list_new:
        if new.key not in key_olds:
            # if not str(new.key).__contains__('autogen'):
            #     if not str(new.key).__contains__('takeout_'):
            if not str(new.key).__contains__('leak_canary_'):
                diff_kce.add(new)

        for old in kce_list_old:
            if old.key == new.key and old.cn != new.cn:
                diff_kce.add(new)

    print('old len ', len(kce_list_old), ',new len ', len(kce_list_new))
    print(', diff count ', count)
    write_kce_to_path(diff_kce, diff_path)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    # new_path = '/Users/toutouhiroshidaiou/tmp/new_535_/res/values/strings.xml'
    # old_path = '/Users/toutouhiroshidaiou/tmp/old_534.apk/res/values/strings.xml'
    # gener_diff(new_path, old_path)

    # diff_list = read_xml_as_kce_list('diff_old_new_2.xml')
    # count = 0
    # for diff in diff_list:
    #     ret = search_kce(diff.cn, down_thread=1.0)
    #     if ret is not None:
    #         count += 1
    #         print('search ', highlight(diff.cn, 3), ',return ' + ret.hl())
    # print('total diff ', len(diff_list), ',find ', count)

    gener_dict_by_excel('/Users/toutouhiroshidaiou/Desktop/i18n/0421_i18n.xlsx')


def gener_dict_by_excel(path_of_excel):
    excel_to_xml(path_of_excel)


if __name__ == '__main__':
    main()
