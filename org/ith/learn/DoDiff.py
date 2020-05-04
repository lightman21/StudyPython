import os
import sys
import time

from org.ith.learn.CleanModule import clean_module, read_ios_as_kce_list
from org.ith.learn.OhMyEXCEL import excel_to_xml, xml_to_excel
from org.ith.learn.scratch.Trans535 import big_dict
from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import open_excel_as_list, read_xml_as_kce_list, KCEBean, highlight, modify_time, md5, \
    auto_escape, extra_chinese, remove_punctuation, is_contains_chinese, exec_cmd
import re
import difflib


def main():
    path_535 = '/tmp/th/OnMobile-official-5.35.10-SNAPSHOT-armeabi-v7a-envGrd-2020-04-27-16-17-10/res/values/strings.xml'
    path_534 = '/tmp/th/5.35.0-armeabi-v7a-envCiTest/res/values/strings.xml'
    new_list = read_xml_as_kce_list(path_535)
    old_list = read_xml_as_kce_list(path_534)
    key_old = set()
    key_new = set()
    for kce in new_list:
        key_new.add(kce.key)
    for kce in old_list:
        key_old.add(kce.key)
    key_old = sorted(key_old)
    key_new = sorted(key_new)

    diff = list()
    for new in new_list:
        if new not in old_list:
            diff.append(new)

    key_diff = set(key_new) - set(key_old)

    print('diff size ', len(diff), ',old list ', len(old_list), ',new list ', len(new_list))
    print('key_old ', len(key_old), ',key new ', len(key_new))
    diff.clear()
    for new in new_list:
        if new.key in key_diff:
            diff.append(new)

    write_kce_to_path(diff, 'scratch/tmp/old_files/key_th_diff.xml')


def shuangwei():
    # sw = '/Users/lightman_mac/Desktop/today2020_04_27_K-mobile_i18n.xlsx'
    # list_kce = open_excel_as_list(sw)
    # write_kce_to_path(list_kce, './sw_cn.xml')
    # write_kce_to_path(list_kce, './sw_en', key='en')
    pass


if __name__ == '__main__':
    # remote = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/build/intermediates/res/merged/official/envCiTest/values-en/values-en.xml'
    # list_remote = read_xml_as_kce_list(remote)
    # write_kce_to_path(list_remote, './all_merged_keys.xml')

    excel_to_xml('/Users/lightman_mac/Desktop/all_excel.xlsx','/Users/lightman_mac/Desktop/tanghao/')

    # sw_cn = './sw_cn.xml'
    # sw_kces = read_xml_as_kce_list(sw_cn)
    # diff_kces = read_xml_as_kce_list('./key_th_diff.xml')
    # common = []
    # for diff in diff_kces:
    #     for sw in sw_kces:
    #         if sw.key == diff.key:
    #             common.append(diff)
    # write_kce_to_path(common, './common.xml')
    # for cm in common:
    #     sw_kces.remove(cm)
    #     diff_kces.remove(cm)
    # write_kce_to_path(sw_kces, './remove_common_sw_cn.xml')
    # write_kce_to_path(diff_kces, './remove_common_diff_kces.xml')
    #
    # dict_path = '/Users/lightman_mac/company/keruyun/oh_my_python/StudyPython/docs/dicts/2020_04_24_22_09__auto__kce_dict.xml'
    # list_dict = list()
    # with open(dict_path, 'r') as rin:
    #     lines = rin.readlines()
    #     pattern = r'<kce key="(.*)" cn="(.*)" en="(.*)"'
    #     for line in lines:
    #         rets = re.findall(pattern, line)
    #         rets = rets[0]
    #         kce = KCEBean(key=rets[0], cn=rets[1], en=rets[2])
    #         list_dict.append(kce)
    #
    # keys = set()
    # for k in list_dict:
    #     keys.add(k)
    #
    # to_done = list()
    # for diff in diff_kces:
    #     if diff.key not in keys:
    #         to_done.append(diff)
    #
    # write_kce_to_path(to_done, './remove_dict_common_diff_kces.xml')
