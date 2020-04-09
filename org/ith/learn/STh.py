import time

from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import KCEBean, highlight, is_contains_chinese, write_to_excel, read_xml_as_kce_list
import re
# from bs4 import BeautifulSoup, CData
import os

list_of_android_path = "/Users/toutouhiroshidaiou/Desktop/keruyun/tmp/android.xlsx"
list_of_ios_path = "/Users/toutouhiroshidaiou/Desktop/keruyun/tmp/ios.xlsx"

android_en_xml_path = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/app/src/main/res/values-en/strings.xml'
android_cn_xml_path = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/app/src/main/res/values/strings.xml'

"""
1.根据当前master分支最新的strings.xml 翻译一个new_master.xml
2.读取最新的i18n文件  i18n.xml
3.对比两个list 把i18n中的key对应的值 写到 new_master.xml中
4.

        yonghuan  <string name="(.*)">(.*)</string>

// 拉取主工程英文strings.xml文件
git archive --remote=ssh://git@gitlab.shishike.com:38401/c_iphone/OnMobile-Android.git HEAD:app/src/main/res/values-en/ strings.xml | tar -x


pickerview_hours  h 1 	  -Hour  5
 pickerview_hours  -Hour  6 	  Hour  4
 pickerview_minutes  Minute 6 	  Point  5
 pickerview_minutes  Point 5 	  -Minute  7
 pickerview_month  Month 5 	  -Month  6
 pickerview_seconds  sec 3 	  -Second  7
 pickerview_year  year 4 	  Year  4
 pickerview_year   Year  6 	  -Year  5
 order_video_second  sec 3 	  -Second  7
 mobileui_date_tab_sdf_month  yyyy-MM 7 	  MM month, yyyy year  19

 kreport_day  Sun. 4 	  -Day  4
 kreport_hour  h 1 	  -Hour  5
 kreport_hour  -Hour  6 	  Hour  4
 kreport_minute  Minute 6 	  Point  5
 kreport_minute  Point 5 	  -Minute  7
 kreport_year  year 4 	  Year  4
 kreport_year   Year  6 	  -Year  5
 kmember_unit_fen  Minute 6 	  Point  5
 kmember_unit_fen  Point 5 	  -Minute  7
 klight_week  Week 4 	  -Week  5
 klight_month  Month 5 	  -Month  6
 day  Sun. 4 	  -Day  4
 check_home_act_value  Minute 6 	  Point  5
 check_home_act_value  Point 5 	  -Minute  7
year  year 4 	  Year  4
 year   Year  6 	  -Year  5

 user_operate_log_day  day 3 	  Sun.  4
 user_operate_log_day  Sun. 4 	  -Day  4
 user_operate_log_month  month 5 	  Month  5
 user_operate_log_month   Month 6 	  Month  5
 user_operate_log_month   Month  7 	  -Month  6
 user_operate_log_year  year 4 	  Year  4
 user_operate_log_year   Year  6 	  -Year  5
 utils_mon_str  Mon. 4 	  One  3
 utils_month  Month 5 	  -Month  6
 utils_sun_str  Sun. 4 	  -Day  4
 
 
 待翻译
 "营业收入" = "Business income";
 "门店销售趋势" = "Store's sales trends";
"服务员绩效" = "Waiter performance";
"门店外卖订单统计" = "Store's takeaway order statistics";
"无单收款报表" = "Statement of revenue from orders without receipts   ";
"会员挂账销账报表" = "Member report of pending orders and charge-off";
"开台数" = "No. of opening tables ";
"笔数: " = "No. of orders:";
"营业收入" = "Business income";
"翻台率" = "Table turnover rate";
"来客数" = "Number of customers  ";
"(人)" = "(person)";
"(元/人)" = "(yuan / person)";
"桌均价" = "Average price per table";
"(元/桌)" = "(yuan/table)";
"总金额" = "Total amount";
"总笔数" = "Total orders";
"订单来源占比" = "Source ratio of orders";
"均为营业日时间" = "All of them are opening hours";
"选择时间" = "Select time";
"员工操作日志" = "Employee Operation Log";
"加盟合作" = "Join us";

"操作员工：" = "Operating staff:";
"操作模块：" = "Operation module:";
"操作端：" = "Operate at:";
"操作内容：" = "Operation contents:";
"操作备注：" = "Operation notes:";

"选择时间段" = "Select time period";
"就餐人数(人)" = "Diners (person)";

"今日总收款" = "Total revenue today";

查询会员模块
"优惠券" = "Coupon";
"会员状态：" = "Member status:";
"会员积分" = "Member's points";
"会员挂账" = "Pending amount of members ";
"储值金额" = "Stored value";
"剩余挂帐额度" = "Remaining pending orders' amount";
"设置挂账额度" = "Set up pending orders' amount";
"挂账记录" = "Pending orders record";
"设置挂账额度" = "Set up pending orders' amount";

储值金额界面
"储值金额补录" = "Re-enter top-up amount";
"扣除确认" = "Confirm deduction";
"补录确认" = "Confirm re-entering";
"扣除实储金额：" = "Deduct top-up amount:";
"补录实储金额：" = "Re-enter top-up amount:";
"扣除赠送金额：" = "Deduct offered amount:";
"补录赠送金额：" = "Re-enter offered amount:";
"最终储值余额：" = "Final top-up balance:";
"储值金额补录" = "Re-enter top-up amount";
"储值金额扣除" = "Deduct top-up amount";
"(原储值余额：%@%@)" = "(original top-up balance: %@ %@） ";
"扣除理由：" = "Deduction reason:";
"补录理由：" = "Reason for re-entering:";
"补录理由：" = "Reason for re-entering:";
"实储金额" = "Top-up amount";
"赠送金额" = "Offered amount";
"理由必填" = "Reason is required";
"储值余额有误？" = "What's wrong with the top-up balance?";
"会员充值" = "Member top-up";


"精选资讯" = "Selected information";

"元/人" = " / Pax";
"%@人" = "%@ Pax";
"/单" = "/Order";

# os.path.getmtime(file) 输出文件最近修改时间

	<string name="mobileui_date_tab_sdf_month">MM month, yyyy year</string>

    <string name="mobileui_date_tab_sdf_month">yyyy-MM</string>


"""

skip_keys = ['sun_str', 'product_desc_handset', 'product_desc_kiosk', 'product_desc_kmobile',
             'mobileui_date_tab_sdf_month', 'main_e_jia']


# amp;

def main():
    # diff()
    # and_merge_en()

    xml_cn = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/app/src/main/res/values/strings.xml'

    xml_en = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/app/src/main/res/values-en/strings.xml'

    en_list = read_xml_as_kce_list(xml_en.strip(), lang='en')
    default_cn_list = read_xml_as_kce_list(xml_cn.strip(), lang='cn')

    for cn in default_cn_list:
        for en in en_list:
            if cn.key == en.key:
                cn.en = en.en

    write_to_excel(default_cn_list, '../../../docs/android_i18n_0407.xlsx')


def total_excel(xml_cn, xml_en, out_path='./out_excel.xlsx'):
    zh_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/build/intermediates/res' \
              '/merged/official/envCiTest/values-zh/values-zh.xml'

    en_list = read_xml_as_kce_list(xml_en, lang='en')
    default_cn_list = read_xml_as_kce_list(xml_cn, lang='cn')
    china_list = read_xml_as_kce_list(zh_path, lang='cn')

    print('china_list size ', len(china_list), '最新修改时间:',
          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(zh_path).st_mtime)))

    print('default size ', len(default_cn_list), '最新修改时间:',
          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(xml_cn).st_mtime)))

    print('en_list size ', len(en_list), '最新修改时间:',
          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(xml_en).st_mtime)))

    key_cn = []
    for cn in default_cn_list:
        key_cn.append(cn.key)
    key_en = []
    for en in en_list:
        key_en.append(en.key)

    count = 0
    no_china_list = []
    for def_cn in default_cn_list:
        if not is_contains_chinese(def_cn.cn):
            no_china_list.append(def_cn)

    for trans in china_list:
        for no_ch in no_china_list:
            if no_ch.key == trans.key:
                if is_contains_chinese(trans.cn):
                    no_ch.cn = trans.cn
                    # count += 1
                    # print(trans.key, trans.cn, '\t', highlight(no_ch.cn))

    for def_cn in default_cn_list:
        for trans in no_china_list:
            if def_cn.key == trans.key:
                if not is_contains_chinese(def_cn.cn) and is_contains_chinese(trans.cn):
                    def_cn.cn = trans.cn

    # 移除 abc_font_family_menu_material home_menu_  jg_channel_name_p_
    tmp = []
    for def_cn in default_cn_list:
        if not str(def_cn.key).startswith('abc_') and (
                not str(def_cn.key).startswith('home_menu_') and (
                not str(def_cn.key).startswith('jg_channel_name_p_'))):
            tmp.append(def_cn)

    print("default chinese size ", len(default_cn_list), ',tmp size ', len(tmp))
    count = 0
    for t in tmp:
        if not is_contains_chinese(t.cn):
            count += 1
            print(t)

    print('final find ', count)

    write_kce_to_path(tmp, './cn_xml.xml')


#

def and_merge_en():
    # 最新string.xml
    studio_en = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/src/main/res/values-en' \
                '/strings.xml'

    en_merpath = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/build/intermediates/res' \
                 '/merged/official/envCiTest/values-en/values-en.xml'

    studio_en_list = read_xml_as_kce_list(studio_en, lang='en')
    print(len(studio_en_list))

    merge_en_list = read_xml_as_kce_list(en_merpath, lang='en')

    skip = ['jg_channel_name_p', 'home_menu_']
    tmp = []
    for m in merge_en_list:
        if str(m.key).__contains__('jg_channel_name_p') or str(m.key).__contains__('home_menu_'):
            print(m)
            continue
        else:
            tmp.append(m)

    print(len(merge_en_list), 'skip ', len(tmp))

    # 是不是所有的studio_en都在
    # all(ele in bg for ele in sm)
    print(all(ele in tmp for ele in studio_en))

    write_kce_to_path(tmp, './tanghao.xml', key='en')


def and_ios():
    ios_p = '/Users/lightman_mac/Desktop/i18n_values-en/ios_en.strings.java'
    en_kce = read_ios_as_kce_list(ios_p)
    ios_p = '/Users/lightman_mac/Desktop/i18n_values-en/ios_cn.strings.java'
    cn_kce = read_ios_as_kce_list(ios_p)
    print(len(en_kce), len(cn_kce))
    ios_kces = list()
    for en in en_kce:
        for cn in cn_kce:
            if en.key == cn.key:
                tmp = en.cn
                ios_kces.append(KCEBean(key=en.key, cn=cn.cn, en=tmp))

    i18n_xml_path = '/Users/lightman_mac/Desktop/i18n_values-en/tanghao/i18nstrings.xml'

    cn_merpath = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/build/intermediates/res' \
                 '/merged/official/envCiTest/values/values.xml'

    android_cn_list = read_xml_as_kce_list(cn_merpath, lang='cn')

    android_i18n = read_xml_as_kce_list(i18n_xml_path, lang='en')

    # android_i18n 中的kce的中文cn赋值
    for en in android_i18n:
        for cn in android_cn_list:
            if en.key == cn.key:
                en.cn = cn.cn

    count = 0
    for android in android_i18n:
        for ios in ios_kces:

            if android.key in skip_keys:
                print("skip_keys return", highlight(skip_keys, 1))
                continue

            if ios.cn == android.cn:
                tmp_android = android.en
                tmp_ios = ios.en.strip().replace('\'', '\\\'')
                if tmp_ios != tmp_android:
                    count += 1
                    android.en = tmp_ios


"""
9910 - 2583
"""


def diff():
    master_xml_path = '/Users/lightman_mac/Desktop/i18n_values-en/tanghao/master_strings.xml'
    i18n_xml_path = '/Users/lightman_mac/Desktop/i18n_values-en/tanghao/i18nstrings.xml'

    cn_merpath = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/build/intermediates/res' \
                 '/merged/official/envCiTest/values/values.xml'

    en_merpath = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/build/intermediates/res' \
                 '/merged/official/envCiTest/values-en/values-en.xml'

    # os.path.getctime(file)输出文件的创建时间
    # os.path.getmtime(file) 输出文件最近修改时间
    # str = ''%H  Hour (24-hour clock) as a decimal number [00,23].
    #     %M  Minute as a decimal number [00,59].
    #     %S  Second as a decimal number [00,61].
    filemt = time.localtime(os.stat(en_merpath).st_mtime)
    print("cn_mergepath ", time.strftime("%Y-%m-%d %H:%M:%S", filemt))

    i18n_list = read_xml_as_kce_list(i18n_xml_path, lang='en')
    master_list = read_xml_as_kce_list(master_xml_path, lang='en')

    print("i18 len ", len(i18n_list), ',master len ', len(master_list), ',cn len ',
          len(read_xml_as_kce_list(cn_merpath, lang='en')), ',en len', len(read_xml_as_kce_list(en_merpath, lang='en')))

    # count = 0
    # i18keys = []
    # masterkeys = []
    # for i18n in i18n_list:
    #     i18keys.append(i18n.key)
    # for master in master_list:
    #     masterkeys.append(master.key)

    # 当i18n的key和master的key相同时
    # 把i18n的value写到master
    # for m in master_list:
    #     for i18 in i18n_list:
    #         if m.key == i18.key:
    #             if m.en != i18.en:
    #                 count += 1
    # write_kce_to_path(i18n_list, './tanghao.xml', key='en')
    # print("overide count ", count, ',total count ', len(i18n_list))


def readlineXML():
    all_str_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/build/intermediates/res' \
                   '/merged/official/envGrd/values/values.xml'
    with open(all_str_path, 'r') as all_value:
        all_str = all_value.read()
        print(all_str.split('<string'))


# def beautiful():
#     all_str_path = '../../../docs/all_values.xml'
#     with open(all_str_path, 'r') as file:
#         txt = file.read()
#         soup = BeautifulSoup(txt, 'html.parser')
#         for cd in soup.findAll(text=True):
#             if isinstance(cd, CData):
#                 print('CData contents: %r' % cd)
#     # print(soup)


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


def extra_strings():
    all_str_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/build/intermediates/res' \
                   '/merged/official/envGrd/values/values.xml'
    with open(all_str_path, 'r') as all_value:
        all_str = all_value.read()

    mock_all_xml = """
    <string name="account_progress_crash_prompt">很抱歉，程序出现异常，即将退出。</string>
    <string name="account_protocol">我已阅读并同意<Data><![CDATA[<a href="%1$s">
    《客如云用户授权协议》</a><a href="%2$s">《客如云用户服务协议》</a>及<a href="%3$s">《客如云用户隐私政策》</a>]]></Data></string>
    <string name="account_pwd">密码</string>
    """

    # matching
    matching = r'<string name="(\w*)">(.*)</string>'
    rets = re.findall(matching, mock_all_xml)
    for rt in rets:
        print("rt--->", 'key=', rt[0], 'value=', rt[1])


if __name__ == '__main__':
    main()
