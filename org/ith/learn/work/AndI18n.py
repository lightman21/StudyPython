from org.ith.learn.OhMyEXCEL import excel_to_xml, xml_to_excel
from org.ith.learn.scratch.Trans535 import big_dict
from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import open_excel_as_list, read_xml_as_kce_list, KCEBean, highlight, modify_time, md5, \
    auto_escape, extra_chinese, remove_punctuation, is_contains_chinese, exec_cmd
import re
import difflib

from org.ith.learn.work.Work import gener_dict_by_excel

"""
0. 生成大字典
读取 潘霜微Excel /Users/toutouhiroshidaiou/Desktop/i18n/0421_i18n.xlsx

                /Users/lightman_mac/Desktop/0418work/418_i18n.xlsx

读取主工程最新大kce    

"""


def demo():
    fanyi_excel = '/Users/toutouhiroshidaiou/Desktop/i18n/0421_i18n.xlsx'
    fanyi_excel = '/Users/lightman_mac/Desktop/0418work/418_i18n.xlsx'
    list_excel_kce = gener_dict_by_excel(fanyi_excel, just_return=True)
    master_path = '/tmp/OnMobile-official-5.35.0-SNAPSHOT-armeabi-v7a-envGrd-2020-04-23-11-03-14/res/values/strings.xml'
    master_path = '/tmp/tanghao/official-5.35.0-envGrd-2020-04-17-19-15-13/res/values/strings.xml'
    ch_path = '/tmp/OnMobile-official-5.35.0-SNAPSHOT-armeabi-v7a-envGrd-2020-04-23-11-03-14/res/values-zh/strings.xml'
    ch_path = '/tmp/tanghao/official-5.35.0-envGrd-2020-04-17-19-15-13/res/values-zh/strings.xml'

    merge_path = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/app/build/intermediates/res/merged/appStore' \
                 '/bugRelease/values/values.xml '

    merge_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/build/intermediates/res' \
                 '/merged/official/envCiTest/values/values.xml '

    merge_list = read_xml_as_kce_list(merge_path)

    master_list = read_xml_as_kce_list(master_path)
    ch_list = read_xml_as_kce_list(ch_path)
    count = 0
    for master in master_list:
        for ch in ch_list:
            if master.key == ch.key:
                if not is_contains_chinese(master.cn) and is_contains_chinese(ch.cn):
                    count += 1
                    master.cn = ch.cn
    print('master size ', len(master_list), ', ch size ', len(ch_list), 'rewrite count ' + str(count), ', merge size ',
          len(merge_list))

    write_kce_to_path(master_list, './rewrite_master.xml', sort=False)
    write_kce_to_path(merge_list, './rewrite_merge.xml')

    rmaster_list = read_xml_as_kce_list('./rewrite_master.xml')
    write_kce_to_path(rmaster_list, './rewrite_sort_master.xml')

    master_keys = []
    for m in master_list:
        master_keys.append(m.key)

    for m in merge_list:
        if m.key not in master_keys:
            print('not in master key ', highlight(m.key, 3), ', value ', highlight(m.cn, 4))

    count = 0
    for fanyin in list_excel_kce:
        for master in master_list:
            if fanyin.key == master.key:
                if fanyin.cn != master.cn:
                    count += 1
                    print(highlight(master.key, 4), ', fanyi.cn ', fanyin.cn, '----> master.cn ',
                          highlight('r' + master.cn, 3))

    print('not match count ', str(count))

    # write_kce_to_path(master_list, './rewrite_master.xml')

    pass


def just_test():
    # report_order_source_tips
    # kmember_tip_auto_pause
    master_kce = read_xml_as_kce_list('./tester.xml')
    for kce in master_kce:
        print(kce.hl(), 'cn len ', len(kce.cn))
        kce.cn = auto_transascii10(kce.cn)
        print('after', kce.hl(), ', cn len ', len(kce.cn))


def auto_transascii10(str_input):
    """
    把输入的软换行换成硬换行
    \n        10        换行NL
    \r        13        回车CR
    """
    ascii_indexes = []
    next_line_ascii = 10
    for index in range(len(str_input)):
        if ord(str_input[index]) == next_line_ascii:
            ascii_indexes.append(index)
    blank = list(str_input)
    for ch_index in ascii_indexes:
        blank[ch_index] = r'\n'

    return ''.join(blank)


def main():
    just_test()
    # demo()
    pass


if __name__ == '__main__':
    main()
