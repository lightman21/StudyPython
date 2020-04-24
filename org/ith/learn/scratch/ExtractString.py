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
]


def should_handle(aar_name):
    tmper = aar_name.replace('_', '.')
    for need in libs_need_care:
        if len(need) > 0 and str(tmper).strip().__contains__(need):
            print(tmper, ', should True', highlight(need, 2))
            return True
    return False


def extract_res(path_of_search):
    count = 0
    for dir_path_name, dirs, files in os.walk(path_of_search):
        for file in files:
            full_path = dir_path_name + os.sep + file
            if full_path.endswith('aar.xml'):
                if file.__contains__('keruyun'):
                    aar_name = full_path.split('__')[1]
                    if should_handle(aar_name):
                        if count < 100:
                            extract_values(aar_name, full_path)
                            count += 1

        print('total count ', count)


def main():
    lib_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/.idea/libraries'
    # lib_path = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/.idea/libraries'
    # extract_res(lib_path)
    test()


def test():
    ss = """
    	<string name="kmember_tip_auto_pause">需要暂停所有会员等级后,才可以进行编辑,
    	是否暂停并编辑等级?</string>
	<string name="kmember_tip_cancel">取消</string>
	<string name="kmember_tip_confirm">确定</string>
	    	<string name="kmember_tip_auto_pause">woshihexiaowe,才可以进行编辑,
    	是否暂停并编辑等级?</string>
    """

    fuzzy_matching = r'<string name="(\w*)">(.*)</string>'
    # r = re.compile(matching, re.DOTALL)
    # rets = r.findall(mock_all_xml)
    # r'/\*(.*?)\*/'
    pattern = r'<string name="(\w*)">(.*)</string>'
    pattern = r'<string name="(\w*)">(.*?)</string>'
    # r = re.compile(pattern, re.DOTALL)
    # rets = r.findall(ss)
    rets = re.findall(pattern, ss, re.DOTALL)

    print('len ', len(rets))
    for ret in rets:
        print(ret)


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
                        value_paths = get_values_path(res_path)
                        for path in value_paths:
                            list_kce = read_xml_as_kce_list(path)
                            out_path = './tmp/auto_extract_work/' + aar_name + '___' + path.split('/')[-1]
                            write_kce_to_path(list_kce, out_path)


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