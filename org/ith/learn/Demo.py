import os

from org.ith.learn.MergeThing import remove_namespace
from org.ith.learn.PXML import parse_string_as_kce, write_kce_to_path


def write_demo():
    # 遍历目录
    path = "/Users/lightman_mac/company/keruyun/proj_sourcecode/Dinner/dinnerui/src/main/res"

    out_path = "../../../docs/tmmp/"

    # walk方法会返回一个三元组，分别是root、dirs和files
    # 目录名称  目录下的目录 目录里的文件list<string>

    biggest = []
    biggest_key = []
    ch_list = []

    for dir_path_name, dirs, files in os.walk(path):

        if dir_path_name.__contains__('values'):
            base = dir_path_name.split("/")[-1]

            for file in files:
                if file.__contains__('strings'):
                    full_name = dir_path_name + '/' + file

                    # print(full_name)

                    p_list = parse_string_as_kce(full_name)
                    out = out_path + base + '___string.xml'
                    write_kce_to_path(p_list, os.path.abspath(out))

                    if full_name.__contains__('values-zh'):
                        ch_list = p_list

                    simple_name = full_name[full_name.index('res'):]

                    print(full_name, "keys ", len(p_list))

                    for f in p_list:
                        if not biggest_key.__contains__(f.key):
                            biggest.append(f)
                            biggest_key.append(f.key)

    print("total key s ", len(biggest), len(ch_list))

    for big in biggest:
        for ch in ch_list:
            if ch.key == big.key:
                big.cn = ch.cn

    write_kce_to_path(biggest, out_path + "biggest.xml")


if __name__ == '__main__':
    write_demo()
