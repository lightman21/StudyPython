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


def check_default_biggest():
    path_of_search = '/Users/lightman_mac/company/keruyun/oh_my_python/StudyPython/org/ith/learn/scratch/tmp' \
                     '/auto_extract_work/2020_05_01/'
    count = 0
    path_dict = dict()
    for dir_path_name, dirs, files in os.walk(path_of_search):
        files = sorted(files)
        for single in files:
            full_path = dir_path_name + single
            kce_list = read_xml_as_kce_list(full_path)
            count += 1
            string = '{:<105} ,size {:<10}'.format(full_path, len(kce_list))
            simple = full_path.split('___')[0]
            path_dict[full_path] = simple
            print(string)

    print('total count ', count)
    aar_path_list_dict = dict()
    for keypath, aar in path_dict.items():
        list_of_path = list()
        if aar in aar_path_list_dict.keys():
            list_of_path = aar_path_list_dict.get(aar)
        list_of_path.append(keypath)
        aar_path_list_dict[aar] = list_of_path

    print('aar_path_list_dict size ', len(aar_path_list_dict))

    for aar, values_list in aar_path_list_dict.items():
        deal_single(aar, values_list)


def deal_single(aar, values_list):
    def_flag = '___values.xml'
    list_of_keyset = []
    def_keyset = list()
    for value in values_list:
        list_kce = read_xml_as_kce_list(value)
        keyset = set()
        for kce in list_kce:
            keyset.add(kce.key)
        keyset = sorted(keyset)
        if str(value).endswith(def_flag):
            def_keyset = keyset
        list_of_keyset.append(keyset)

    for keys in list_of_keyset:
        for key in keys:
            if key not in def_keyset:
                ss = '{:<80}  default is not biggest'.format(aar)
                print(ss)
                return False


def main():
    check_default_biggest()


if __name__ == '__main__':
    main()
