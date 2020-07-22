import os

from org.ith.learn.util.TUtils import modify_time, read_xml_as_kce_list

app_path = '/tmp/th/OnMobile-Android/app/'
build_path = 'build/intermediates/res/merged/'


def main():
    walk()


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
