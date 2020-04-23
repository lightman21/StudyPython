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

读取主工程最新大kce    

"""


def demo():
    mpath = '/Users/toutouhiroshidaiou/Desktop/th_values.xml'

    # fanyi_excel = '/Users/toutouhiroshidaiou/Desktop/i18n/0421_i18n.xlsx'
    # list_excel_kce = gener_dict_by_excel(fanyi_excel, just_return=True)
    master_path = '/tmp/OnMobile-official-5.35.0-SNAPSHOT-armeabi-v7a-envGrd-2020-04-23-11-03-14/res/values/strings.xml'
    ch_path = '/tmp/OnMobile-official-5.35.0-SNAPSHOT-armeabi-v7a-envGrd-2020-04-23-11-03-14/res/values-zh/strings.xml'

    merge_path = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/app/build/intermediates/res/merged/appStore' \
                 '/bugRelease/values/values.xml '

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
    print('master size ', len(master_list), ', ch size ', len(ch_list), 'rewrite count ' + str(count))

    write_kce_to_path(master_list, './rewrite_master.xml', sort=False)
    write_kce_to_path(merge_list, './rewrite_merge.xml')

    rmaster_list = read_xml_as_kce_list('./rewrite_master.xml')
    write_kce_to_path(rmaster_list, './rewrite_sort_master.xml')

    # count = 0
    # for fanyin in list_excel_kce:
    #     for master in master_list:
    #         if fanyin.key == master.key:
    #             if fanyin.cn != master.cn:
    #                 count += 1
    #                 print(fanyin.cn, '----> ', highlight(master.cn, 3), '----> ', highlight(master.key, 4))

    print('not match count ', str(count))

    # write_kce_to_path(master_list, './rewrite_master.xml')

    pass


def main():
    demo()

    # r=re.compile(matching,re.DOTALL)
    # master_list = read_xml_as_kce_list('./rewrite_master.xml')
    # merge_list = read_xml_as_kce_list('./rewrite_merge.xml')
    # print('merge len ', len(merge_list), ', master len ', len(master_list))
    # master_keys = []
    # merge_keys = []
    # demo()




    pass


if __name__ == '__main__':
    main()
