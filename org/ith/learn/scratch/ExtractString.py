import os
import time

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
    '正餐',
    'com.keruyun.mobile.dinner',
    'com.keruyun.mobile.klight',
    ','
    '快餐',
    'com.keruyun.mobile.mobile.tradeserver',
    'com.keruyun.mobile.tradeui.library',
    'com.keruyun.mobile.tradeui.klight',
    'com.keruyun.mobile.tradeui.klightlib',
    'com.keruyun.mobile.tradeui.kmobile',
    ','
    '报表',
    'com.keruyun.kmobile.kreport',
    ','
    '商品管理',
    'com.keruyun.kmobile.kmobile.commodity',
    '',
    'com.keruyun.android.android.mobilecommondata',
    '',
    '库存',
    'com.keruyun.kmobile.kmobile.inventory.management.ui',
    '',
    '会员管理',
    'com.keruyun.kmobile.kmobile.member.manage',
    '',
    '订单中心',
    'com.keruyun.kmobile.kmobile.order.center',
    '',
    '外卖',
    'com.keruyun.kmobile.kmobile.takeout.ui',
    '',
    '经营设置',
    'com.keruyun.kmobile.kmobile.business.setting',
    '',
    '员工管理',
    'com.keruyun.kmobile.kmobile.staff',
    '',
    '',
]

need_auto_del = {
    "员工管理": ['com.keruyun.kmobile.kmobile.staff'],
    "经营设置": ['com.keruyun.kmobile.kmobile.business.setting'],
    "正餐": ['com.keruyun.mobile.dinner', 'com.keruyun.mobile.klight'],
}


def should_handle(aar_name):
    tmper = aar_name.replace('_', '.')
    for need in libs_need_care:
        if len(need) > 0 and str(tmper).strip().__contains__(need):
            print(tmper, ', should True', highlight(need, 2))
            return True
    return False


def extract_res(path_of_search):
    path_set = set()
    count = 0
    for dir_path_name, dirs, files in os.walk(path_of_search):
        for file in files:
            full_path = dir_path_name + os.sep + file
            if full_path.endswith('aar.xml'):
                if file.__contains__('keruyun'):
                    aar_name = full_path.split('__')[1]
                    # if should_handle(aar_name):
                    if count < 500:
                        extract_values(aar_name, full_path)
                        count += 1
                        # path_set.add(full_path.split('___')[0])
                        print('aar name ', aar_name)
                        print('path_set ', full_path.split('___')[0])

        print('total count ', count, 'path set ', len(path_set))


def main():
    """
    遍历目录 生成kcew  全部写成一行 格式
    <kce key="da7bf8ff5663ce74873b34b5425258cc" cn="正在导航" en="Navigating" where='com_keruyun_android_android_mobileui_2_8_60_SNAPSHOT_aar.xml___values.xml'/>
    """
    do_extract()

def read_origin(path):
    kce_list = read_xml_as_kce_list(path)

def gener_kcew(aar_path, huanout_path):
    # print(highlight('gener_kcew before size '), len(read_xml_as_kce_list(out_path)))

    kce_list = read_xml_as_kce_list(aar_path)

    if len(kce_list) == 0:
        print('0 return---------------- ', highlight(aar_path))
        return

    str_lines = []
    where = get_aar_simple(aar_path)
    for kce in kce_list:
        line = '<kce key="{}" cn="{}" en="{}" where="{}"/>'.format(kce.key, kce.cn, kce.en, where)
        str_lines.append(line)
        str_lines.append('\r\n')

    with open(huanout_path, 'a+') as out:
        print(highlight('gener_kcew', 2), ',size ', len(str_lines), highlight(',to path '), huanout_path)
        out.writelines(str_lines)
    pass


def get_aar_simple(path_aar):
    return path_aar.split('/')[-1]


def do_extract():
    # lib_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/.idea/libraries'
    # lib_path = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/.idea/libraries'
    # lib_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/.idea/libraries'
    lib_path = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/.idea/libraries'

    extract_res(lib_path)


def extract_values(aar_name, aar_path):
    home_path = os.path.expanduser('~')
    pattern = '<root url="(.*)" />'
    with open(aar_path, 'r') as rin:
        content = rin.read()
        rets = re.findall(pattern, content)

        now_date = time.strftime("%Y_%m_%d", time.localtime())

        if rets is not None:
            for ret in rets:
                if str(ret).endswith('res'):
                    spt = ret.split(r'$USER_HOME$')
                    if len(spt) > 1:
                        res_path = home_path + spt[1]
                        value_paths = get_values_path(res_path)
                        for path in value_paths:
                            list_kce = read_xml_as_kce_list(path)
                            out_path = './tmp/auto_extract_work/' + now_date + os.sep + aar_name + '___' + \
                                       path.split('/')[-1]
                            write_kce_to_path(list_kce, out_path)

                            gener_kcew(aar_path=out_path, huanout_path='/tmp/tanghao/zhuijia.xml')


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
