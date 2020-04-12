import re

from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import read_xml_as_kce_list, KCEBean, highlight, modify_time

i18n_xml_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/src/main/res/values-en' \
                '/strings.xml'

diff_path = '/Users/lightman_mac/Desktop/0411work/tsd/diff.xml'

cn_xml_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/src/main/res/values/strings.xml'


def main():
    trans_autogen()


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
