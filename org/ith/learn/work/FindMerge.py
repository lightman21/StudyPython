import os

# from util.PXML import write_kce_to_path
from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import modify_time, read_xml_as_kce_list

app_path = '/tmp/th/OnMobile-Android/app/'
build_path = 'build/intermediates/res/merged/'


def main():
    path = '/Users/toutouhiroshidaiou/Desktop/mock/english.xml'
    kce_list = read_xml_as_kce_list(path)

    # 遍历kce_list 把所有c的值存成一个 dict(cn,list<key>)

    # kce_list.sort(key=lambda x: x.cn)
    # write_kce_to_path(kce_list, path)

    k_dict = dict()
    for kce in kce_list:
        list_keys = k_dict.get(kce.cn)
        if list_keys is None:
            list_keys = list()
        if not list_keys.__contains__(kce.key):
            list_keys.append(kce.key)
        k_dict[kce.cn] = list_keys

    print("len list ", len(kce_list), 'len dict ', len(k_dict))

    copyed_list = list(kce_list)
    count = 0
    dict_of_value_key = dict()
    for cn_value, list_of_key in k_dict.items():
        if len(list_of_key) > 1:
            list_of_key.sort(key=lambda x: len(x))
            dict_of_value_key[cn_value] = list_of_key[0]
            count += 1

    to_write_kces = list()
    for kce in copyed_list:
        if kce.cn in dict_of_value_key.keys():
            # 取出value
            to_keys = dict_of_value_key[kce.cn]
            if to_keys != kce.key:
                kce.cn = '@string/' + to_keys
                # print(kce.key, '------------>', kce.cn)
                to_write_kces.append(kce)
            else:
                to_write_kces.append(kce)
        else:
            to_write_kces.append(kce)

    print('copyed_list size ',len(copyed_list),', to_write size ',len(to_write_kces))

    dest_path = '___Desktop/out.xml'
    # write_kce_to_path(to_write_kces, dest_path)
    kces = read_xml_as_kce_list(dest_path)
    write_kce_to_path(kces,dest_path)

    # for kce in kce_list:
    #     print(kce)


def walk():
    gen_path = app_path + build_path
    first = True
    xml_dict = dict()
    for dir_path_name, dirs, files in os.walk(gen_path):
        if files.__contains__('values-en.xml'):
            short_name = dir_path_name.split('merged')[1]
            file = dir_path_name + os.sep + files[0]
            # print(file, modify_time(file), short_name)
            list_xml = read_xml_as_kce_list(file)
            # print(short_name, len(list_xml))
            xml_dict[file] = list_xml

    # xml_dict.keys()
    # for (k, v) in xml_dict.items():
    #     print(k, modify_time(k), len(v))

    tmp = None
    for val in xml_dict.values():
        if tmp is None:
            tmp = val

        # if first:
        #     first = False
        #     build_dir = dirs
        #     for dir_name in dirs:
        #         print(modify_time(dir_path_name + dir_name))


if __name__ == '__main__':
    main()
