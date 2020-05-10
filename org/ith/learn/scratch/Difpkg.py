import difflib
import re

from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import open_excel_as_list, read_xml_as_kce_list, KCEBean, highlight, modify_time, md5, \
    auto_escape, extra_chinese, remove_punctuation, is_contains_chinese, exec_cmd, auto_transascii10
from org.ith.learn.work.Work import just_sort

skip_key_prefix = [
    'abc_',
    'leak_canary_',
    'title_activity',
    'key_liveness_',
]


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2)



def main():
    cn_path = 'tmp/remove_cn.xml'
    eng_path = 'tmp/remove_eng.xml'
    pass



if __name__ == '__main__':
    main()
    pass
