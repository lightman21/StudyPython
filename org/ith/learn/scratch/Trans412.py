import re

from org.ith.learn.OhMyEXCEL import xml_to_excel
from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import read_xml_as_kce_list, KCEBean, highlight, modify_time

i18n_xml_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/src/main/res/values-en' \
                '/strings.xml'

diff_path = '/Users/lightman_mac/Desktop/0411work/tsd/shuangwei413.xml'

cn_xml_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/src/main/res/values/strings.xml'


def main():
    # cn_path = '/Users/lightman_mac/company/keruyun/oh_my_python/StudyPython/docs/dicts/autogen/20200412_not_trans.xml'
    # en_path = './en_path.xml'
    # xml_to_excel(path_of_cn=cn_path, path_of_en=en_path, excel_path='./not_trans.xlsx')

    ios_list = get_ios_kces()
    not_trans_path = '/tmp/not_trans.xml'
    not_list = read_xml_as_kce_list(not_trans_path)

    print('total  not trans ', len(not_list))

    trans_from_ios = []
    count = 0
    for kce in not_list:
        for ios in ios_list:
            if ios.cn == kce.cn:
                count += 1
                kce.en = ios.en
                if kce not in trans_from_ios:
                    trans_from_ios.append(kce)

    print('from ios trans ', len(trans_from_ios))

    # write_kce_to_path(trans_from_ios, ',/from_ios_cn.xml')
    # write_kce_to_path(trans_from_ios, ',/from_ios_en.xml', key='en')

    realy_not_trans = set()
    for not_tr in not_list:
        for ios in trans_from_ios:
            if not_tr not in trans_from_ios:
                realy_not_trans.add(not_tr)

    print('really not trans ', len(realy_not_trans))

    realy_not_trans = list(realy_not_trans)

    for rea in realy_not_trans:
        print(rea)

    # write_kce_to_path(biggest, out_path + "biggest.xml")

    write_kce_to_path(realy_not_trans, '/tmp/really_cn.xml')
    write_kce_to_path(realy_not_trans, '/tmp/really_en.xml', key='en')
    xml_to_excel(path_of_cn='/tmp/really_cn.xml', path_of_en='/tmp/really_en.xml', excel_path='./really.xlsx')

    """
    b/businesssetting/src/main/res/layout/loading_empty.xml
@@ -16,7 +16,7 @@
         android:layout_marginTop="15dp"
         android:textSize="15sp"
         android:layout_centerHorizontal="true"
-        android:text="咦...没有任何内容，先去逛逛别的吧"
+        android:text="@string/biz_setting_ah_no_data"


b/businesssetting/src/main/res/layout/loading_error.xml
@@ -37,7 +37,7 @@
             android:paddingRight="46dp"
             android:paddingTop="11dp"
             android:paddingBottom="11dp"
-            android:text="重新加载"
+            android:text="@string/biz_setting_reload"


    <string name="biz_setting_ah_no_data">咦...没有任何内容，先去逛逛别的吧</string>
    <string name="biz_setting_reload">重新加载</string>
    
    
    """


def get_ios_kces():
    ios_p = '/tmp/ios_en.strings.java'
    en_kce = read_ios_as_kce_list(ios_p)
    ios_p = '/tmp/ios_cn.strings.java'
    cn_kce = read_ios_as_kce_list(ios_p)
    print(len(en_kce), len(cn_kce))
    ios_kces = list()
    for en in en_kce:
        for cn in cn_kce:
            if en.key == cn.key:
                tmp = en.cn
                ios_kces.append(KCEBean(key=en.key, cn=cn.cn, en=tmp))

    for ios in ios_kces:
        ios.en = ios.en.strip().replace('\'', '\\\'')

    return ios_kces


def read_ios_as_kce_list(ios_path):
    with open(ios_path, 'r') as file:
        all_str = file.read()
        ios_match = r'"(.*)"\s=\s"(.*)"'
        list_kce = []
        rets = re.findall(ios_match, all_str)
        for t in rets:
            h = KCEBean(key=t[0], cn=t[1], en='')
            list_kce.append(h)

        return list_kce


def trans_autogen():
    new_add_list = read_xml_as_kce_list('/Users/lightman_mac/Desktop/added.xml')
    print('new add size ', len(new_add_list))
    count = 0
    transed_list = []
    not_trans = []
    for kce in new_add_list:
        transed = translate(kce.cn)
        if transed != kce.cn:
            # 说明已经找到翻译了
            kce.cn = transed.cn
            kce.en = transed.en

            transed_list.append(kce)

            count += 1
        else:
            not_trans.append(kce)

    write_kce_to_path(not_trans, '../../../../docs/dicts/autogen/20200412_not_trans.xml')
    write_kce_to_path(transed_list, '../../../../docs/dicts/autogen/20200412_has_trans_cn.xml')
    write_kce_to_path(transed_list, '../../../../docs/dicts/autogen/20200412_has_trans_en.xml', key='en')


def translate(hanyu):
    big_kce = []
    dict_path = '../../../../docs/dicts/2020-04-12_20:43:34__kce_dict.xml'
    with open(dict_path) as m_input:
        big_str = m_input.read()
        matcher = r'<kce key="(.*)" cn="(.*)" en="(.*)"'
        rets = re.findall(matcher, big_str)
        for ret in rets:
            kce = KCEBean(key=ret[0], cn=ret[1], en=ret[2])
            big_kce.append(kce)

        finded = False
        kce_finded = hanyu

        for kce in big_kce:
            tmp = kce.cn.replace(':', '').replace('：', '')
            hanyu = hanyu.replace(':', '').replace('：', '')
            if tmp == hanyu:
                finded = True
                kce_finded = kce

    if kce_finded:
        return kce_finded
    else:
        return hanyu


def gener_dict():
    # 主工程最新的
    path_cn_master = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/src/main/res/values' \
                     '/strings.xml'
    path_english_master = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/src/main/res' \
                          '/values-en/strings.xml'

    en_list = read_xml_as_kce_list(path_english_master)
    cn_list = read_xml_as_kce_list(path_cn_master)

    for kce in en_list:
        kce.en = kce.cn
        kce.cn = ''

    for kce in en_list:
        for cnkce in cn_list:
            if cnkce.key == kce.key:
                kce.cn = cnkce.cn

    str_lines = []

    """
    th = '<kce key="about_text" cn="关于" en="About" />'
    matcher = r'<kce key="(.*)" cn="(.*)" en="(.*)"'
    rets = re.findall(matcher, th)
    """
    for kce in en_list:
        # line = '<kce key="{:<30}" cn="{}" en="{}" />'.format(kce.key, kce.cn, kce.en)
        line = '<kce key="{}" cn="{}" en="{}" />'.format(kce.key, kce.cn, kce.en)
        str_lines.append(line)
        str_lines.append('\r\n')

    out_name = modify_time('./').replace(' ', '_') + '__' + 'kce_dict.xml'
    with open(out_name, 'w') as out:
        out.writelines(str_lines)


if __name__ == '__main__':
    main()
