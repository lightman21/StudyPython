"""
MD5 (com_keruyun_android_android_crop_images_1_2_20_aar.xml___crop_images_divider.9.png) = ff3cfec21b2bc6f195bf90ea72a54cb8


"""
import re
from filecmp import cmp

from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import read_xml_as_kce_list
from org.ith.learn.work.Work import just_sort


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


def main():
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

    sub_path = order_center

    # just_sort(cashier)

    total_all = '/Users/toutouhiroshidaiou/keruyun/proj/sub_modules/mobile-storage/translate/kmobile/english.xml'
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

    # write_kce_to_path(tmp, './path_of_xml_sub.xml')


if __name__ == '__main__':
    main()
