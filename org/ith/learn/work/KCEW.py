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
    path_of_search = '/Users/lightman_mac/company/keruyun/oh_my_python/StudyPython/org/ith/learn/scratch/tmp' \
                     '/auto_extract_work/2020_04_27/'
    for dir_path_name, dirs, files in os.walk(path_of_search):

        print(files)


        pass


if __name__ == '__main__':
    main()
