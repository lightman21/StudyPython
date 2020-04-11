"""
1.找到最初给翻译的excel文件 生成一个0407_origin.xlsx
2.根据最新的翻译excel生成一个0410_new.xlsx
3.diff出两个文件的内容

4.观察最新文件内容  总结出需要忽略的kce规律

skip_key_list = []

在主工程merge大kce列表的时候  考虑需要忽略的东西


python工程 需要一个api支持传入excel路径 转成xml存储


0. 考虑一个过滤表 过滤不写到excel的key
1. 有一个中文重复的list 存储重复的kce


将excel导出为kce 并且根据最新的kce去替换主工程的文件

其中需要注意时间格式问题 可能改动的不对 先把时间格式相关的标记出来

<string name="date_month_day_formate_str">MM month dd</string>
<string name="date_year_month_formate_str">MM month, yyyy year</string>
<string name="klight_yyyy_M_h">Yyyy year M month d</string>
<string name="kreport_ymd">dd MM yyyy</string>
<string name="member_credit_date_month_day_formate_str">MM month dd</string>
<string name="member_credit_date_year_month_formate_str">MM month, yyyy year</string>
<string name="print_year_to_day_format">HH:mm:ss on the DD day of MM month in YYYY year</string>

<string name="date_month_day_formate_str">MM month dd</string>
<string name="date_year_month_formate_str">MM month, yyyy year</string>
"""
from org.ith.learn.OhMyEXCEL import excel_to_xml
from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import read_xml_as_kce_list, highlight

out_path = '/Users/lightman_mac/Desktop/0411work/tsd/'

input_tanghao_old = '/Users/lightman_mac/Desktop/0411work/tanghao_0407.xlsx'
input_shuangwei_new = '/Users/lightman_mac/Desktop/0411work/panshuangwei_0410_origin.xlsx'

# 直接忽略不写入xml 没有用了估计是这个kce
total_skip = ['account_bind_third_login_tip', 'authorization_person_id',
              'authorization_person_id', 'authorization_person_id_input',
              'authorization_person_name', 'danshu_str',
              'daily_stored_money', 'daily_unreceive_money',
              'daily_unreceive_money_2', 'intelligence_push',
              'internal_error', 'international_check_home_act_state_info',
              'invalidate', 'kreport_no_third_pay_data',
              'kreport_paymentAmount', 'kreport_payment_inShop',
              'kry_version_name_text', 'legal_person_partner_check',
              'member_credit_xiaozhangjine_xiaoyu_yiguazhangjine', 'ms_self_pay_all_chinese',
              '', ''
              ]


def diff():
    out_tanghao = excel_to_xml(path_of_excel=input_tanghao_old, xml_path=out_path)
    out_shuangwei = excel_to_xml(path_of_excel=input_shuangwei_new, xml_path=out_path)

    en_path_tanghao = out_tanghao[1]
    en_path_shuangwei = out_shuangwei[1]

    en_tanghao_list = read_xml_as_kce_list(en_path_tanghao)
    en_shuangwei_list = read_xml_as_kce_list(en_path_shuangwei)

    diff_list = []

    for en_th in en_tanghao_list:
        for en_sw in en_shuangwei_list:
            if en_th.key == en_sw.key:
                if auto_escape(en_th.cn) != auto_escape(en_sw.cn):
                    en_sw.cn = auto_escape(en_sw.cn)
                    en_sw.en = auto_escape(en_sw.en)
                    diff_list.append(en_sw)

    print('diff count ', len(diff_list))

    write_kce_to_path(list_of_kce=diff_list, path=out_path + 'diff.xml')


# 跳过key名开头的 跳过
skip_key_list = ['leak_canary_', 'key_liveness_', 'title_activity_']


def main():
    diff()


def write_to_kce(list_of_kce, path_of_dest):
    xml_path = '/Users/lightman_mac/Desktop/0411work/tsd/tanghao_0407xlsx_english.xml'
    en_kce_list = read_xml_as_kce_list(xml_path)
    xml_path = '/Users/lightman_mac/Desktop/0411work/tsd/tanghao_0407xlsx_china.xml'
    kce_list = read_xml_as_kce_list(xml_path)

    for kce in kce_list:
        for enkce in en_kce_list:
            if kce.key == enkce.key:
                kce.en = enkce.cn

    str_lines = []

    """
    th = '<kce key="about_text" cn="关于" en="About" />'
    matcher = r'<kce key="(.*)" cn="(.*)" en="(.*)"'
    rets = re.findall(matcher, th)
    """
    for kce in kce_list:
        # line = '<kce key="{:<30}" cn="{}" en="{}" />'.format(kce.key, kce.cn, kce.en)
        line = '<kce key="{}" cn="{}" en="{}" />'.format(kce.key, kce.cn, kce.en)
        str_lines.append(line)
        str_lines.append('\r\n')

    with open(out_path + 'merge_kce.xml', 'w') as out:
        out.writelines(str_lines)


def auto_escape(inputing):
    """
    检查传入的字符串 是不是需要转义加\
    如果包含' 但是不包含\'
    则需要把' 替换伟\'
    """
    origin = ['\'', ]
    escape = ['\\\'', ]

    if len(inputing) > 0:
        for index in range(len(escape)):
            str_input = str(inputing)
            if str_input.__contains__(origin[index]):
                if not str_input.__contains__(escape[index]):
                    inputing = str_input.replace(origin[index], escape[index])
    return inputing


if __name__ == '__main__':
    main()
