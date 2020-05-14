import os
import time

from org.ith.learn.OhMyEXCEL import excel_to_xml, xml_to_excel
from org.ith.learn.scratch.Trans535 import big_dict
from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import open_excel_as_list, read_xml_as_kce_list, KCEBean, highlight, modify_time, md5, \
    auto_escape, extra_chinese, remove_punctuation, is_contains_chinese, exec_cmd, extract_string_array, chunk_in_slice, \
    make_sure_file_exist, file_md5
import re
import difflib
import os

from org.ith.learn.work.IBaidu import get_all_pics, loop_pics

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

# 需要跳过忽略的库
libs_need_skip = [
    'ocr相关',
    'com_keruyun_kmobile_third_loan_ocr_live_body',
    'kmobile-android-ocr-dish-contain',
    '',
    '打印',
    'com_keruyun_print_print',
    '',
    '',
    'com_keruyun_android_android_crop_image',
    'com_keruyun_android_widget_digitinputview',
    'com_keruyun_kmobile_kmobile_react_native_spinkit',
    'com_keruyun_android_recyclerview_helper',
    'com_keruyun_android_osmobile_dialog',
    'com_keruyun_android_osmobile_title_manager',
    'com_keruyun_kmobile_kmobile_react_native_picker',
    'com_keruyun_android_android_safe_webview',
    'com_keruyun_calm_dns_discovery',
    '',
    '',
    '',
]


def main():
    # daily_work()
    do_extract()


def daily_work():
    lib_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/.idea/libraries'
    # lib_path = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/.idea/libraries'
    now_date = time.strftime("%Y_%m_%d", time.localtime())
    out_dir = './tmp/auto_extract_work/' + now_date + os.sep
    aar_path_dict = gener_aar_path_dict(lib_path)
    for aar_name, aar_abs_path in aar_path_dict.items():
        values_path_list = extract_values_or_res(aar_abs_path)
        for path in values_path_list:
            # 如 values-en.xml
            values_name = path.split('/')[-1]
            extract_string_array(path, extract_path=out_dir + '__string_array_' + str(aar_name) + '__' + values_name)
            list_kce = read_xml_as_kce_list(path)
            kce_out_path = out_dir + str(aar_name) + '___' + values_name
            write_kce_to_path(list_kce, kce_out_path)


def do_extract():
    lib_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/.idea/libraries'
    lib_path = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/.idea/libraries'
    aar_path_dict = gener_aar_path_dict(lib_path)
    # dest_root = '/tmp/kmobile/'
    dest_root = '../../../../docs/km_pics/kmobile/'

    pic_desc_list = list()
    last_simple_aar_name = ''

    for aar_name, aar_abs_path in aar_path_dict.items():
        res_path = extract_values_or_res(aar_abs_path, just_res=True)
        all_pics = get_all_pics(res_path)
        if len(all_pics) > 0:
            for full_path_of_pic in all_pics:
                pic_name = full_path_of_pic.split('/')[-1]
                print('full name ', full_path_of_pic, ',\t' + pic_name)
                # /Users/lightman_mac/.gradle/caches/transforms-1/files-1.1/custompay-2.4.4.aar/b75dde205be3047ee7f621d8e8d1af6a/res/drawable-xhdpi-v4/img_unchecked.png
                res_arr = full_path_of_pic.split('files-1.1/')[1].split('/res')
                # /drawable-xhdpi-v4/img_unchecked.png
                dest_pic_name = res_arr[1]
                # 第一个数字的索引 -1 是因为还多了一个下划线
                index = [x.isdigit() for x in aar_name].index(True) - 1
                # com_keruyun_mobile_custompay
                pkg_name = aar_name[:index]

                index = [x.isdigit() for x in res_arr[0]].index(True) - 1
                # custompay
                simple_aar_name = res_arr[0][:index]

                print(highlight(res_arr, 3), ',pkg_name ', pkg_name, ',simple_aar_name ', simple_aar_name)

                to_dest = dest_root + simple_aar_name + os.sep + pkg_name + dest_pic_name
                make_sure_file_exist(to_dest, just_dir=True)
                command = 'cp {} {}'.format(full_path_of_pic, to_dest)
                print(command)
                exec_cmd(command)

                pic_md5 = file_md5(full_path_of_pic)
                # simple_aar_name  pkg_name pic_name  md5:xxx

                new_line = '\n' if last_simple_aar_name == simple_aar_name else '\n' * 1
                pid_desc = '{:<30} {:<40} {}{}'.format(simple_aar_name, pic_name, pic_md5, new_line)
                pic_desc_list.append(pid_desc)
                last_simple_aar_name = simple_aar_name

    with open('../../../../docs/km_pics/pic_desc.txt', 'w') as rout:
        rout.writelines(pic_desc_list)

    # exec_cmd('git add . && git commit -m "extract pics" && git push origin i18n  ')


def gener_aar_path_dict(path_of_search):
    """
    抽取指定path_of_search 路径下 所有aar.xml

    aar name  com_keruyun_mobile_dinner_2_25_70_SNAPSHOT_aar.xml
    abs_path  /Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/.idea/libraries/Gradle__com_keruyun_mobile_dinner_2_25_70_SNAPSHOT_aar.xml

    返回 key 为aar name ,value 为 abs_path(绝对路径)的dict

    """
    aar_path_dict = dict()

    for dir_path_name, dirs, files in os.walk(path_of_search):
        for file in files:
            full_path = dir_path_name + os.sep + file
            if full_path.endswith('aar.xml'):
                if file.__contains__('keruyun'):
                    aar_name = full_path.split('__')[1]
                    abs_path = full_path.split('___')[0]
                    aar_path_dict[aar_name] = abs_path

    return aar_path_dict


def extract_values_or_res(aar_path, just_res=False):
    """
    :param just_res 是不是只需要res目录
    :param aar_path 输入的aar在本地的缓存地址
        如 /Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/.idea/libraries/Gradle__com_keruyun_mobile_dinner_2_25_70_SNAPSHOT_aar.xml
    :return 返回一个dict key为aar_name,value为相应路径的values目录列表
    """
    home_path = os.path.expanduser('~')
    pattern = '<root url="(.*)" />'
    with open(aar_path, 'r') as rin:
        content = rin.read()
        rets = re.findall(pattern, content)
        # now_date = time.strftime("%Y_%m_%d", time.localtime())
        if rets is not None:
            for ret in rets:
                if str(ret).endswith('res'):
                    spt = ret.split(r'$USER_HOME$')
                    if len(spt) > 1:
                        res_path = home_path + spt[1]
                        if just_res:
                            return res_path

                        value_paths = get_values_path(res_path)
                        return value_paths


def get_values_path(m_path):
    """
    @param m_path  '/Users/lightman_mac/.gradle/caches/transforms-1/files-1.1/dinner-2.25.70-SNAPSHOT.aar/714e6c249d4a08323211d78d2c891558/res'
    返回所有values的列表 如
    [
    '/Users/lightman_mac/.gradle/caches/transforms-1/files-1.1/dinner-2.25.70-SNAPSHOT.aar/714e6c249d4a08323211d78d2c891558/res/values/values.xml',
    '/Users/lightman_mac/.gradle/caches/transforms-1/files-1.1/dinner-2.25.70-SNAPSHOT.aar/714e6c249d4a08323211d78d2c891558/res/values-en/values-en.xml'
    ]
    """
    list_of_values_paths = []
    for dir_path_name, dirs, files in os.walk(m_path):
        for file in files:
            if file.__contains__('values'):
                full_name = dir_path_name + '/' + file
                list_of_values_paths.append(full_name)
                print(highlight(modify_time(full_name), 2), ' full_name -> ', full_name)

    return list_of_values_paths


def should_handle(aar_name):
    tmper = aar_name.replace('_', '.')
    for need in libs_need_care:
        if len(need) > 0 and str(tmper).strip().__contains__(need):
            print(tmper, ', should True', highlight(need, 2))
            return True
    return False


def gener_kcew(aar_path, huanout_path):
    print(highlight('gener_kcew before size '), len(read_xml_as_kce_list(huanout_path)))

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


if __name__ == '__main__':
    main()
