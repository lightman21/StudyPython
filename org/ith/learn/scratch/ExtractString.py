import os

from org.ith.learn.OhMyEXCEL import excel_to_xml, xml_to_excel
from org.ith.learn.scratch.Trans535 import big_dict
from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import open_excel_as_list, read_xml_as_kce_list, KCEBean, highlight, modify_time, md5, \
    auto_escape, extra_chinese, remove_punctuation, is_contains_chinese, exec_cmd
import re
import difflib
import os

"""
<root url="file://$USER_HOME$/.gradle/caches/transforms-1/files-1.1/tradeui-kmobile-1.11.30-SNAPSHOT.aar/6287918f966595e8c2b0fe549739a62e/res" />

tradeserver      : 'com.keruyun.mobile:mobile-tradeserver:1.11.30@aar',
tradeui_library  : 'com.keruyun.mobile:tradeui-library:1.11.30@aar',
tradeui_klight   : 'com.keruyun.mobile:tradeui-klight:1.11.30@aar',
tradeui_klightlib: 'com.keruyun.mobile:tradeui-klightlib:1.11.30@aar',
tradeui_kmobile  : 'com.keruyun.mobile:tradeui-kmobile:1.11.30@aar',
dinner           : 'com.keruyun.mobile:dinner:2.25.60',
klight           : 'com.keruyun.mobile:klight:1.10.20',

"""

libs_need_care = [
    'com.keruyun.mobile:dinner',
    'com.keruyun.mobile:klight',
    '',
    'com.keruyun.mobile:mobile-tradeserver',
    'com.keruyun.mobile:tradeui-library',
    'com.keruyun.mobile:tradeui-klight',
    'com.keruyun.mobile:tradeui-klightlib',
    'com.keruyun.mobile:tradeui-kmobile',
    '',
    'com.keruyun.kmobile:kreport',
    '',
    'com.keruyun.kmobile:kmobile-commodity',
    '',
    '',
]


def extract_res():
    pass


def main():
    lib_path = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/.idea/libraries'

    home_path = os.path.expanduser('~')

    # ss = '<root url="file://$USER_HOME$/.gradle/caches/transforms-1/files-1.1/tradeui-kmobile-1.11.30-SNAPSHOT.aar/6287918f966595e8c2b0fe549739a62e/res" />'
    # pattern = '<root url="(.*)" />'
    # ret = re.findall(pattern, ss)
    # if ret is not None:
    #     ret = ret[0]
    #     spt = ret.split(r'$USER_HOME$')
    #     if len(spt) > 1:
    #         res_path = home_path + spt[1]
    #         print('res_path', res_path)
    #         get_values_path(res_path)

    count = 0

    for dir_path_name, dirs, files in os.walk(lib_path):
        for file in files:
            full_path = dir_path_name + os.sep + file
            if full_path.endswith('aar.xml'):
                if file.__contains__('keruyun'):
                    aar_name = full_path.split('__')[1]
                    print('aar_name')
                    extract_values(aar_name, full_path)

    print('total count ', count)


pass


def extract_values(aar_name, aar_path):
    home_path = os.path.expanduser('~')
    pattern = '<root url="(.*)" />'
    with open(aar_path, 'r') as rin:
        content = rin.read()
        rets = re.findall(pattern, content)
        if rets is not None:
            for ret in rets:
                if str(ret).endswith('res'):
                    spt = ret.split(r'$USER_HOME$')
                    if len(spt) > 1:
                        res_path = home_path + spt[1]
                        print(highlight('aar_name'), aar_name)
                        print(highlight('res_path'), res_path)
                        rt = get_values_path(res_path)
                        # print(rt)


def get_values_path(m_path):
    list_of_res = []
    for dir_path_name, dirs, files in os.walk(m_path):
        for file in files:
            if file.__contains__('values'):
                full_name = dir_path_name + '/' + file
                print('full_name -> ', full_name)
                list_of_res.append(full_name)
    return list_of_res


if __name__ == '__main__':
    main()
