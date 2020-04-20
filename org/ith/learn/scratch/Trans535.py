import os

from org.ith.learn.OhMyEXCEL import excel_to_xml, xml_to_excel
from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import open_excel_as_list, read_xml_as_kce_list, KCEBean, highlight, modify_time, md5, \
    auto_escape, extra_chinese, remove_punctuation, is_contains_chinese, exec_cmd

import re
import difflib
import zipfile


def get_apk_string_as_kce(apk_path):
    os.chdir('/tmp/tanghao/')
    apk_name = apk_path.split('/')[-1].split('.apk')[0]
    string_path = os.path.dirname(apk_path) + os.sep + apk_name + '/res/values/strings.xml'
    ret = exec_cmd('apktool d ' + apk_path)
    kce_list = read_xml_as_kce_list(string_path)
    return kce_list


def string_similar(s1, s2):
    # return difflib.SequenceMatcher(None, s1, s2).quick_ratio()
    return difflib.SequenceMatcher(lambda x: x in ':：！!?。', s1, s2).quick_ratio()


def main():
    # path_new = '/Users/lightman_mac/Desktop/0418work/535_app-official-armeabi-v7a-envSingapore.apk'
    # path_old = '/Users/lightman_mac/Desktop/0418work/534app-official-armeabi-v7a-envCiTest.apk'
    # new_kce_list = get_apk_string_as_kce(path_new)
    # old_kce_list = get_apk_string_as_kce(path_old)
    gener_diff(new_path='/tmp/tanghao/535_app-official-armeabi-v7a-envSingapore/res/values/strings.xml',
               old_path='/tmp/tanghao/534app-official-armeabi-v7a-envCiTest/res/values/strings.xml',
               diff_path='/tmp/diff.xml')


def ios_by_excel():
    excel_path = '/Users/lightman_mac/Desktop/km2008.xlsx'
    km_list = open_excel_as_list(excel_path)
    count = 0
    ios_km = []
    for km in km_list:
        if len(km.en) > 0:
            print(km)
            count += 1
            km.key = md5(km.key)
            ios_km.append(km)

    print('km count ', count)

    str_lines = []

    for kce in ios_km:
        # line = '<kce key="{:<30}" cn="{}" en="{}" />'.format(kce.key, kce.cn, kce.en)
        if len(kce.key) > 0 and len(kce.cn) > 0 and len(kce.en) > 0:
            line = '<kce key="{}"__keyend cn="{}"__cnend en="{}"__enend />'.format(kce.key, kce.cn, kce.en)
            str_lines.append(line)
            str_lines.append('\r\n')

    out_name = modify_time('./').replace(' ', '_') + '__' + 'ios_kce_dict.xml'
    with open(out_name, 'w') as out:
        out.writelines(str_lines)


def i18n_trans():
    path_535 = '/tmp/tanghao/OnMobile-official-5.35.0-SNAPSHOT-armeabi-v7a-envGrd-2020-04-17-19-15-13/res/values' \
               '/strings.xml '
    kce_list_535 = read_xml_as_kce_list(path_535)
    path_534 = '/Users/lightman_mac/Desktop/0418work/534app-official-armeabi-v7a-envCiTest/res/values/strings.xml'

    yuedeng = set()

    gener_diff(old_path=path_534, new_path=path_535)
    big_kce_list = big_dict()
    diff_kce_list = read_xml_as_kce_list('diff_534_535.xml')
    find_kce = []
    count = 0
    for diff in diff_kce_list:
        for big in big_kce_list:
            # 只取汉字
            tmpbig = big.cn
            tmpdiff = diff.cn
            tmpbig = auto_escape(tmpbig)
            tmpdiff = auto_escape(tmpdiff)

            # tmpbig = extra_chinese(tmpbig)
            # tmpdiff = extra_chinese(tmpdiff)

            tmpbig = remove_punctuation(tmpbig)
            tmpdiff = remove_punctuation(tmpdiff)

            is_match = big.cn == diff.cn and tmpbig == tmpdiff

            if not is_match:
                if tmpdiff == tmpbig:
                    rate = string_similar(big.cn, diff.cn)
                    if rate < 1.0:
                        if is_contains_chinese(diff.cn):
                            yuedeng.add(diff.cn)
                            print(highlight(rate, 1), '--> ', highlight(diff.cn, 2), highlight(big.cn, 3),
                                  highlight(big.en, 4))

            if is_match:
                diff.en = big.en
                if not find_kce.__contains__(diff):
                    find_kce.append(diff)
                    count += 1

    print('big size ', len(big_kce_list), ',diff size ', len(diff_kce_list), ',find count ', count)

    write_kce_to_path(find_kce, path='./diff_534_535_find.xml', key='en')

    find_kce.clear()
    for kce in diff_kce_list:
        if len(kce.en) < 1:
            find_kce.append(kce)

    write_kce_to_path(find_kce, path='./diff_534_535_not_find.xml', key='cn')

    print('约等于 ', len(yuedeng))
    for s in yuedeng:
        print(s)


def big_dict():
    big = []
    with open('../../../../docs/dicts/2020-04-19_13:37:39__kce_dict.xml', 'r') as rin:
        lines = rin.readlines()
        for line in lines:
            kce = gener_kce_by_dict(line.strip())
            big.append(kce)

    return big


def gener_kce_by_dict(ss):
    """
    把指定格式的 字符串解析成kcebean
    <kce key="accepted"__keyend cn="已接受"__cnend en="Accepted"__enend />
    """
    match = r'<kce key="(.*)"__keyend.*cn="(.*)"__cnend.*en="(.*)"__enend'
    rets = re.findall(match, ss)
    rets = rets[0]
    key = rets[0]
    cn = rets[1]
    en = rets[2]
    return KCEBean(key=key, cn=cn, en=en)


def gener_dict():
    """
    生成一个大字典
    line = '<kce key="{}" cn="{}" en="{}" />'.format(kce.key, kce.cn, kce.en)
    """
    # 主工程最新的
    path_cn_master = '/tmp/tanghao/OnMobile-official-5.35.0-SNAPSHOT-armeabi-v7a-envGrd-2020-04-17-19-15-13/res' \
                     '/values/strings.xml'
    path_english_master = '/Users/lightman_mac/Desktop/en_kce418.xml'

    en_list = read_xml_as_kce_list(path_english_master)
    cn_list = read_xml_as_kce_list(path_cn_master)

    for kce in en_list:
        kce.en = kce.cn
        kce.cn = ''

    for kce in en_list:
        for cnkce in cn_list:
            if cnkce.key == kce.key:
                kce.cn = cnkce.cn

    str_lines = []

    """
    th = '<kce key="about_text" cn="关于" en="About" />'
    matcher = r'<kce key="(.*)" cn="(.*)" en="(.*)"'
    rets = re.findall(matcher, th)
    """
    for kce in en_list:
        # line = '<kce key="{:<30}" cn="{}" en="{}" />'.format(kce.key, kce.cn, kce.en)
        if len(kce.key) > 0 and len(kce.cn) > 0 and len(kce.en) > 0:
            line = '<kce key="{}"__keyend cn="{}"__cnend en="{}"__enend />'.format(kce.key, kce.cn, kce.en)
            str_lines.append(line)
            str_lines.append('\r\n')

    out_name = modify_time('./').replace(' ', '_') + '__' + 'kce_dict.xml'
    with open(out_name, 'w') as out:
        out.writelines(str_lines)


def gener_diff(new_path, old_path, diff_path='./diff_old_new_1.xml'):
    kce_list_new = read_xml_as_kce_list(new_path)
    kce_list_old = read_xml_as_kce_list(old_path)
    key_olds = []
    for kce in kce_list_old:
        key_olds.append(kce.key)
    diff_kce = []
    count = 0
    for new in kce_list_new:
        if new.key not in key_olds:
            # if not str(new.key).__contains__('autogen'):
            #     if not str(new.key).__contains__('takeout_'):
            if not str(new.key).__contains__('leak_canary_'):
                count += 1
                diff_kce.append(new)

    print('old len ', len(kce_list_old), ',new len ', len(kce_list_new))
    print(', diff count ', count)
    write_kce_to_path(diff_kce, diff_path)


if __name__ == '__main__':
    main()
