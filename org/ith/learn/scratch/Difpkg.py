import difflib
import re

from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import open_excel_as_list, read_xml_as_kce_list, KCEBean, highlight, modify_time, md5, \
    auto_escape, extra_chinese, remove_punctuation, is_contains_chinese, exec_cmd, auto_transascii10
from org.ith.learn.work.Work import just_sort


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2)


def diff():
    just_sort('/Users/lightman_mac/company/keruyun/oh_my_python/StudyPython/docs/pure/all_english_53510.xml')
    en_path = '/Users/lightman_mac/company/keruyun/oh_my_python/StudyPython/docs/pure/all_english_53510.xml'
    ch_path = '/Users/lightman_mac/company/keruyun/oh_my_python/StudyPython/docs/pure/all_china_53510_apk_all_cn.xml'
    en_kce_list = read_xml_as_kce_list(en_path)
    ch_kce_list = read_xml_as_kce_list(ch_path)

    key_eng = set()
    key_china = set()

    for kce in en_kce_list:
        key_eng.add(kce.key)

    for kce in ch_kce_list:
        key_china.add(kce.key)

    diff = key_china - key_eng

    print('diff count ', len(diff))
    count = 0
    to_i18 = list()
    for kce in ch_kce_list:
        if kce.key in diff:
            if str(kce.key).startswith('key_liveness_') or str(kce.key).startswith('leak_canary_'):
                continue

            # if not is_contains_chinese(str(kce.cn)):
            #     continue

            print(kce.hl())
            to_i18.append(kce)
            count += 1

    print('remove shit diff count ', count)
    write_kce_to_path(to_i18, '/Users/lightman_mac/company/keruyun/oh_my_python/StudyPython/docs/pure/to_be_i18.xml')


def main():
    cn_path = 'tmp/remove_cn.xml'
    eng_path = 'tmp/remove_eng.xml'
    cn_list = read_xml_as_kce_list(cn_path)
    # <!--	-->
    left = '<!--'
    right = '-->'

    # <string name="report_target_complete_label">目标完成度：%1$d%</string>
    str_en_line = list()

    with open(eng_path, 'r') as rin:
        lines = rin.readlines()
        count = 0
        for line in lines:
            if count < 30000:
                match = r'<string name="(\w*)">(.*)</string>'
                rets = re.findall(match, line, re.DOTALL)
                if len(rets) > 0:
                    rets = rets[0]
                    key = rets[0]
                    value = rets[1]
                    count += 1
                    kce = findkce(key, cn_list)
                    if kce is None:
                        print(key)
                        continue
                    #     <!-- 赠送 --> 	<string name="kemember_zengsong">Give away</string>
                    ss = '{} {} {} {}'.format(left, kce.cn.replace('--', '__'), right, line)
                    str_en_line.append(ss)

        with open('tmp/comment_en.xml', 'w') as rout:
            rout.writelines(str_en_line)
    pass


def findkce(key, kce_list):
    for kce in kce_list:
        if kce.key == key:
            return kce


if __name__ == '__main__':
    main()
    pass
