import time

from org.ith.learn.OhMyEXCEL import excel_to_xml, xml_to_excel
from org.ith.learn.scratch.Trans535 import big_dict
from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import open_excel_as_list, read_xml_as_kce_list, KCEBean, highlight, modify_time, md5, \
    auto_escape, extra_chinese, remove_punctuation, is_contains_chinese, exec_cmd
import re
import difflib

from org.ith.learn.work.Work import just_sort

tmp = libs_need_care = [
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
    '',
    '经营设置',
    'com.keruyun.kmobile.kmobile.business.setting'
]

"""
 now_date = time.strftime("%Y_%m_%d", time.localtime())
    to_write_lines = []
    for kce in no_dup:
        if len(kce.key) > 0 and len(kce.cn) > 0 and len(kce.en) > 0:
            v_cn = auto_escape(kce.cn).replace('please', 'pls').replace('Please', 'Pls').capitalize()
            v_en = auto_escape(kce.en).capitalize()
            line = '<kce key="{:<40}" cn="{}" en="{}"/>\n'.format(kce.key, v_cn, v_en)
            to_write_lines.append(line)

    with open('./{}_kce_dict.xml'.format(now_date), 'w') as out:
        out.writelines(to_write_lines)

"""


def gener_dict(en_path, cn_path):
    en_list = read_xml_as_kce_list(en_path)
    ch_list = read_xml_as_kce_list(cn_path)

    for cn in ch_list:
        for en in en_list:
            if cn.key == en.key:
                cn.en = en.cn

    now_date = time.strftime("%Y_%m_%d", time.localtime())
    to_write_lines = []
    for kce in ch_list:
        if len(kce.key) > 0 and len(kce.cn) > 0 and len(kce.en) > 0:
            v_cn = auto_escape(kce.cn)
            v_en = auto_escape(kce.en)
            line = '<kce key="{:<40}" cn="{}" en="{}"/>\n'.format(kce.key, v_cn, v_en)
            to_write_lines.append(line)

    with open('./{}___kce_dict.xml'.format(now_date), 'w') as out:
        out.writelines(to_write_lines)


def remove_by_path(master_path, sub_module_path):
    master_kce_list = read_xml_as_kce_list(master_path)
    module_list = read_xml_as_kce_list(sub_module_path)

    master_pure = []

    remove_list = []

    for module in module_list:
        for master in master_kce_list:
            if master.key == module.key:
                # to be remove
                remove_list.append(master)

    for master in master_kce_list:
        if master not in remove_list:
            master_pure.append(master)

    print('before size ', len(master_kce_list), 'write in size ', len(master_pure))

    write_kce_to_path(master_pure, master_path)


def do_remove():
    # master_zh = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/app/src/main/res/values-zh/strings.xml'
    master_def = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/app/src/main/res/values/strings.xml'
    master_en = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/app/src/main/res/values-en/strings.xml'

    local_dinner = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/scratch/tmp' \
                   '/auto_extract_work/2020_04_26/com_keruyun_mobile_dinner_2_25_70_SNAPSHOT_aar.xml___values.xml'

    local_tradeserver = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/scratch/tmp' \
                        '/auto_extract_work/2020_04_26/com_keruyun_mobile_mobile_tradeserver_1_11_40_SNAPSHOT_aar' \
                        '.xml___values-en.xml'

    local_kreport = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/scratch/tmp/auto_extract_work/2020_04_26/com_keruyun_kmobile_kreport_5_31_60_SNAPSHOT_aar.xml___values-en.xml'
    local_commidity = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/scratch/tmp/auto_extract_work/2020_04_26/com_keruyun_kmobile_kmobile_commodity_1_12_20_SNAPSHOT_aar.xml___values-en.xml'
    loal_inventory = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/scratch/tmp/auto_extract_work/2020_04_26/com_keruyun_kmobile_kmobile_inventory_management_ui_1_3_00_SNAPSHOT_aar.xml___values-en.xml'
    local_member_manager = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/scratch/tmp/auto_extract_work/2020_04_26/com_keruyun_kmobile_kmobile_member_manage_1_11_50_SNAPSHOT_aar.xml___values-en.xml'
    local_business_setting = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/scratch/tmp/auto_extract_work/2020_04_26/com_keruyun_kmobile_kmobile_business_setting_1_01_10_SNAPSHOT_aar.xml___values-en.xml'

    module_list = read_xml_as_kce_list(local_business_setting)

    master_kce_list = read_xml_as_kce_list(master_en)
    master_pure = []

    remove_list = []

    for module in module_list:
        for master in master_kce_list:
            if master.key == module.key:
                # to be remove
                remove_list.append(master)

    for master in master_kce_list:
        if master not in remove_list:
            master_pure.append(master)

    print('before size ', len(master_kce_list), 'write in size ', len(master_pure))

    write_kce_to_path(master_pure, master_en)
    pass


def merge_keys():
    master_zh = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/app/src/main/res/values-zh/strings.xml'
    master_def = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/app/src/main/res/values/strings.xml'

    zh_list = read_xml_as_kce_list(master_zh)
    def_list = read_xml_as_kce_list(master_def)

    all_keys = set()
    zh_keys = list()
    def_keys = list()

    all_kce = []

    for zh in zh_list:
        zh_keys.append(zh.key)
        all_keys.add(zh.key)

        all_kce.append(zh)

    for def_kce in def_list:
        def_keys.append(def_kce.key)
        all_keys.add(def_kce.key)
        all_kce.append(def_kce)

    add_kces = []
    add_keys = set()
    count = 0
    for kce in all_kce:
        if kce.key not in add_keys:
            add_kces.append(kce)
            add_keys.add(kce.key)
        else:
            print('dup ', kce)
            count += 1

    write_kce_to_path(add_kces, master_zh)
    write_kce_to_path(add_kces, master_def)

    print('all keys ', len(all_keys), ', zh_keys ', len(zh_keys), ', def keys ', len(def_keys), ', len add_kces ',
          len(add_kces), ',dup count ', count)

    pass


def main():
    # do_remove()
    # merge_keys()
    master_def = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/app/src/main/res/values/strings.xml'
    sub_module_path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/scratch/tmp/auto_extract_work/2020_04_26/com_keruyun_kmobile_kmobile_business_setting_1_01_10_SNAPSHOT_aar.xml___values.xml'
    sub_module_path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/scratch/tmp/auto_extract_work/2020_04_26/com_keruyun_kmobile_kmobile_commodity_1_12_20_SNAPSHOT_aar.xml___values.xml'
    sub_module_path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/scratch/tmp/auto_extract_work/2020_04_26/com_keruyun_kmobile_kmobile_inventory_management_ui_1_3_00_SNAPSHOT_aar.xml___values.xml'
    sub_module_path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/scratch/tmp/auto_extract_work/2020_04_26/com_keruyun_kmobile_kmobile_member_manage_1_11_50_SNAPSHOT_aar.xml___values.xml'
    sub_module_path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/scratch/tmp/auto_extract_work/2020_04_26/com_keruyun_kmobile_kreport_5_31_60_SNAPSHOT_aar.xml___values.xml'
    sub_module_path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/scratch/tmp/auto_extract_work/2020_04_26/com_keruyun_mobile_dinner_2_25_70_SNAPSHOT_aar.xml___values.xml'
    sub_module_path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/scratch/tmp/auto_extract_work/2020_04_26/com_keruyun_mobile_mobile_tradeserver_1_11_40_SNAPSHOT_aar.xml___values.xml'
    sub_module_path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/scratch/tmp/auto_extract_work/2020_04_26/com_keruyun_mobile_tradeui_klight_1_11_40_SNAPSHOT_aar.xml___values.xml'
    sub_module_path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/scratch/tmp/auto_extract_work/2020_04_26/com_keruyun_mobile_tradeui_klightlib_1_11_40_SNAPSHOT_aar.xml___values.xml'
    sub_module_path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/scratch/tmp/auto_extract_work/2020_04_26/com_keruyun_mobile_tradeui_kmobile_1_11_40_SNAPSHOT_aar.xml___values.xml'
    sub_module_path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/scratch/tmp/auto_extract_work/2020_04_26/com_keruyun_mobile_tradeui_library_1_11_40_SNAPSHOT_aar.xml___values.xml'
    sub_module_path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/scratch/tmp/auto_extract_work/2020_04_26/com_keruyun_kmobile_kmobile_takeout_ui_1_1_60_SNAPSHOT_aar.xml___values.xml'
    sub_module_path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/scratch/tmp/auto_extract_work/2020_04_26/com_keruyun_kmobile_kmobile_takeout_ui_1_1_60_SNAPSHOT_aar.xml___values-zh.xml'
    # remove_by_path(master_def, sub_module_path)

    # open_excel_as_list('/Users/toutouhiroshidaiou/Desktop/tweak_0426_tang.xlsx')
    en_path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/docs/tweak_0426_tangxlsx_2020_04_26_16_16_30_english.xml'
    cn_path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/docs/tweak_0426_tangxlsx_2020_04_26_16_16_30_china.xml'
    gener_dict(en_path, cn_path)


def gener_cn_en_dict(path_of_excel):
    list_kce = open_excel_as_list(path_of_excel)
    cn_en_dict = dict()
    for kce in list_kce:
        if len(kce.cn) > 0 and len(kce.en) > 0:
            cn_en_dict[kce.cn] = kce.en

    return cn_en_dict


if __name__ == '__main__':
    main()
