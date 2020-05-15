"""
MD5 (com_keruyun_android_android_crop_images_1_2_20_aar.xml___crop_images_divider.9.png) = ff3cfec21b2bc6f195bf90ea72a54cb8


"""
import re

from org.ith.learn.OhMyEXCEL import excel_to_xml
from org.ith.learn.util.TUtils import read_xml_as_kce_list, highlight, auto_escape, auto_transascii10, KCEBean


def sort_by_value(d):
    items = d.items()
    backitems = [[v[1], v[0]] for v in items]
    backitems.sort()
    return [backitems[i][1] for i in range(0, len(backitems))]


def pic_md5():
    path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/work/res/pics/all_pic_md5.txt'
    md5_dict = dict()
    with open(path, 'r') as rin:
        lines = rin.readlines()
        pattern = r'MD5<(.*)>=(.*)'
        for line in lines:
            line = line.replace(' ', '').replace('(', '<').replace(')', '>')
            rets = re.findall(pattern, line)
            if len(rets) == 1:
                rets = rets[0]
                md5_dict[rets[0]] = rets[1]

        print(md5_dict)
        dict_sorted_list = sorted(md5_dict.items(), key=lambda x: x[1], reverse=True)

        to_lines = list()
        last_value = ''
        for item in dict_sorted_list:
            new_line = '\n'
            if last_value != item[1]:
                new_line *= 2
            out = '{:<100} = {}{}'.format(item[0], item[1], new_line)
            last_value = item[1]

            to_lines.append(out)

        with open('./tmp.tmp', 'w') as rout:
            rout.writelines(to_lines)


def day_work():
    inventory = '/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/kmobile-android-inventory-management/inventoryui/src/main/res/values-ru/strings.xml'
    takeout = '/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/kmobile-takeout-ui/takeoutui/src/main/res/values-zh/strings.xml'
    takeout_values = '/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/kmobile-takeout-ui/takeoutui/src/main/res/values/strings.xml'
    total_all = '/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/kmobile-android-inventory-management/test/src/main/res/values-en/strings.xml'
    smart_path = '/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/kmobile-smart-management/smartmanage/src/main/res/values-en/strings.xml'
    table_manage = '/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/kmobile-table-manage/tablemanage/src/main/res/values/strings.xml'
    kreport = '/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/KReport/kreport/src/main/res/values-en/origin_strings.xml'
    table_code = '/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/Manager-Table-Code/tablecodelib/src/main/res/values-zh-rTW/strings.xml'
    cashier = '/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/kmobile-cashier/cashier/src/main/res/values/strings.xml'
    order_center = '/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/kmobile-order-center/trade/src/main/res/values/strings.xml'
    merge = '/Users/toutouhiroshidaiou/keruyun/proj/OnMobile-Android/app/build/intermediates/res/merged/official/envCiTest/values/values.xml'

    sub_path = merge

    # just_sort(cashier)

    total_all = '/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/mobile-storage/translate/kmobile/i18n.xml'
    kce_sub_list = read_xml_as_kce_list(sub_path)
    total_list = read_xml_as_kce_list(total_all)
    total_keys = set()
    for kce in total_list:
        total_keys.add(kce.key)

    tmp = list()
    no_i18n = list()
    for kce in kce_sub_list:
        if kce.key in total_keys:
            tmp.append(kce)
        else:
            print('nnnot find in trans key ', kce.key, ',and value :', kce.cn)
            no_i18n.append(kce)

    print('total sub ', len(kce_sub_list), ', not find ', len(no_i18n))


def write_pics_desc(to_write_list):
    """
       将list_of_kce 写到指定指定路径
       """
    import xlwt
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Android_i18n')
    worksheet.write(0, 0, "模块名")
    worksheet.write(0, 1, "图片名")
    worksheet.write(0, 2, "MD5")

    for row, item in enumerate(to_write_list):
        row += 1
        for column in range(3):
            key = item.key
            cn = item.cn
            en = item.en

            if column == 0:
                worksheet.write(row, column, key)
            elif column == 1:
                worksheet.write(row, column, cn)
            elif column == 2:
                worksheet.write(row, column, en)

    workbook.save('path_of_excel.xlsx')


def gener_tweak():
    new_en = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/docs/0514_swxlsx_2020_05_14_16_40_48_english.xml'
    old_en = '/Users/toutouhiroshidaiou/Downloads/google/2020_05_10_21_54_18__english.xml'

    new_kce_list = read_xml_as_kce_list(new_en)
    old_kce_list = read_xml_as_kce_list(old_en)

    count = 0

    to_write_list = list()

    for kce_new in new_kce_list:
        for old in old_kce_list:
            if kce_new.key == old.key:
                kce_new.cn = auto_escape(kce_new.cn)
                kce_new.cn = auto_transascii10(kce_new.cn)
                old.cn = auto_escape(old.cn)
                old.cn = auto_transascii10(old.cn)
                if kce_new.cn != old.cn:
                    print(kce_new.key, highlight(kce_new.cn, 2), old.cn)
                    count += 1
                    to_write_list.append(kce_new)

    print('old_en ', len(old_kce_list), ', new en ', len(new_kce_list), ',count = ', count)

    from org.ith.learn.util.PXML import write_kce_to_path
    write_kce_to_path(to_write_list, './new_tweaked_again.xml')


"""
 total_eng_path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/docs/i18n/english.xml'
    tweak_path = 'new_tweaked_again.xml'
    kce_en_list = read_xml_as_kce_list(tweak_path)
    total_list = read_xml_as_kce_list(total_eng_path)
    for total in total_list:
        for kce in kce_en_list:
            if total.key == kce.key:
                total.cn = kce.cn
    from org.ith.learn.util.PXML import write_kce_to_path
    write_kce_to_path(total_list, './new_total_eng.xml')

"""


def replaceAll(str_input, to_replace, replace_with):
    while str_input.find(to_replace) > -1:
        str_input = str_input.replace(to_replace, replace_with)

    return str_input


def main():
    pic_path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/docs/km_pics/pic_desc.txt'
    list_of_kce = list()
    with open(pic_path, 'r') as rin:
        all_lines = rin.readlines()
        for line in all_lines:
            spt = line.split(' ')
            its = list()
            for s in spt:
                if len(s.strip()) > 0:
                    its.append(s)
            list_of_kce.append(KCEBean(key=its[0], cn=its[1], en=its[2]))

    list_of_kce = sorted(list_of_kce)

    out_line = list()
    keys = set()

    for kce in list_of_kce:
        line = '{:<40} {:<50} {}'.format(kce.key, kce.cn, kce.en)
        out_line.append(line)
        keys.add(kce.en)

    with open('./here.txt', 'w')as rout:
        rout.writelines(out_line)

    print('total pic ', len(out_line), ',and unique ', len(keys))

    pass


if __name__ == '__main__':
    main()
