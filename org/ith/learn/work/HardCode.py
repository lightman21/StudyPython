import os
import re

import pypinyin

from org.ith.learn.util.PXML import write_kce_to_path
from org.ith.learn.util.TUtils import is_contains_chinese, highlight, exec_cmd, read_xml_as_kce_list, KCEBean, md5

"""
autogen
KCEBean(string key,string cn,string en)

0.遍历工程默认strings.xml生成cur_list_kce
拉取主工程默认values文件并解析为all_of_kce

1.扫描工程layout下的xml文件发现hardcode,
hardcode:解析xml当且仅当android:text或android:hint节点的值为中文时  认为这是一次可自动替换的hardcode.
纪录原始hardcode字符串以及所在文件路径 res_hd_value_to_path

2.扫描工程.java .kt结尾的文件发现hardcode
hardcode:当且仅当setText()括号中内容为中文时,认为这是一次可自动替换的hardcode
纪录原始hardcode字符串以及所在文件路径
src_hd_value_to_path

3.遍历插入
如果all_of_kce中有cn值match到当前扫描到的hardcode,
将该kce插入cur_list_kce
如果没有匹配则需要自动生成kce并插入cur_list_kce
需要自动生成的kce的key值规则如下
key=当前module名_autogen_汉字首字母小写
考虑中文字符串过长的情况不要首字母直接md5
如kreport工程下的hardcode 我爱小龙虾 
key值为 kreport_autogen_waxlx
这里不区分src和res下hardcode的key值是因为可能有一样的hardcode 希望最终只生成一个key

3.将cur_list_kce写入当前工程strings.xml,
至此工程src以及res/layout下的hardcode都已在strings.xml中有key和value 

4.登陆模块实现一个静态方法resStr(int resID),里面实现是取当前工程的application context方便后续替换
所以放登陆模块是因为所有modelu都依赖登陆且能保证resStr方法内的context随时可用,因为要第一时间初始化

src指的扫描工程.java .kt结尾的文件
res指的扫描工程src/layout里的xml文件
5.替换有两种
src替换 把hardcode替换为Utils.resStr(hardcode_key)
res替换 把hardcode替换为@string/hardcode_key

6.执行upload编译工程

考虑到后续可能把自动生成的hardcode的key字符串替换为其他可读性较好的字符串

 0张可用优惠券  --> /Users/toutouhiroshidaiou/keruyun/proj/sub_modules/Dinner/dinnerui/src/main/res/layout/dinner_act_member_base.xml
 (人头费 10)  --> /Users/toutouhiroshidaiou/keruyun/proj/sub_modules/Dinner/dinnerui/src/main/res/layout/dinner_act_additional_layout.xml

<string name="kreport_RTF_10">出票口(可多选)</string>

"""

flag_and_texter = 'android_text'
flag_and_hinter = 'android_hint'

layout_path = '/src/main/res/layout'
default_values = 'src/main/res/values/strings.xml'

list_all_remote = []


def main():
    list_all_remote.extend(pull_remote_values())
    hardcode_killer('/Users/lightman_mac/company/keruyun/proj_sourcecode/mobile-ui/')


def hardcode_killer(path_of_module):
    os.chdir(path_of_module)

    modules_path_list = get_module_path(path_of_module)

    list_of_kces_path_flag = list()

    for module_path in modules_path_list:
        for dir_path, dirs, files in os.walk(module_path):
            if dir_path.__contains__(layout_path):
                # 本模块的默认strings.xml
                def_value_path = module_path + os.sep + default_values
                # 本模块下的 kce 列表
                module_kce_list = read_xml_as_kce_list(def_value_path)

                # files 即 模块layout/文件下的所有xml文件
                for file_item in files:
                    # /Users/toutouhiroshidaiou/keruyun/proj/sub_modules/Dinner/dinnerui/src/main/res/layout/dinner_act_setmeal.xml
                    full_name = dir_path + os.sep + file_item

                    if full_name.endswith('.xml'):
                        # 找到每个文件下的hardcode并和文件路径 关联成一个dict
                        # key hardcode value path_of_xml
                        hardcode_to_path_dict = parse_xml_as_dict(full_name, parser=flag_and_texter)
                        if len(hardcode_to_path_dict) > 0:
                            list_kce_by_text = hardcode_to_kce_list(dh_path_dict=hardcode_to_path_dict,
                                                                    module_kces=module_kce_list,
                                                                    path_of_module=module_path)
                            if len(list_kce_by_text) > 0:
                                module_kce_list.extend(list_kce_by_text)
                                list_of_kces_path_flag.append((list_kce_by_text, full_name, flag_and_texter))

                        hint_hardcode_dict = parse_xml_as_dict(full_name, parser=flag_and_hinter)
                        if len(hint_hardcode_dict) > 0:
                            list_kce_by_hint = hardcode_to_kce_list(dh_path_dict=hint_hardcode_dict,
                                                                    module_kces=module_kce_list,
                                                                    path_of_module=module_path)
                            if len(list_kce_by_hint) > 0:
                                module_kce_list.extend(list_kce_by_hint)
                                list_of_kces_path_flag.append((list_kce_by_hint, full_name, flag_and_hinter))

                # todo 这里不用每次写 后续改成有变化再写
                # 这里需要手动处理重复
                # tmp = []
                # for tm in module_kce_list:
                #     if tm not in tmp:
                #         tmp.append(tm)

                write_kce_to_path(module_kce_list, def_value_path)

    if len(list_of_kces_path_flag) > 0:

        for hkp in list_of_kces_path_flag:
            kces = hkp[0]
            file = hkp[1]
            flag = hkp[2]
            old_to_new_dict = gener_replacer(kces, flag)

            with open(file, 'r') as all_str:
                to_file_str = all_str.read()
                for old, new in old_to_new_dict.items():
                    to_file_str = to_file_str.replace(old, new)
                    write_auto_log(module_path, old_hardcode=old, new_tweaked=new, path_of_xml=file)
                with open(file, 'w') as out:
                    out.write(to_file_str)

    log_path = module_path + os.sep + 'autogen.log'
    if not os.path.exists(log_path):
        return

    with open(log_path, 'r') as logger:
        lines = logger.readlines()
        for line in lines:
            ele_arr = line.split('<=>')
            old = ele_arr[0].strip()
            new = ele_arr[1].strip()
            xpath = ele_arr[2].strip()

            if old != new:
                modifyxml(old, new, module_path)
                with open(xpath, 'r') as mxml:
                    all_str = mxml.read().replace(old, new)
                    with open(xpath, 'w') as out:
                        out.write(all_str)


def modifyxml(old, new, module_path):
    def_stringx = module_path + os.sep + default_values
    old_str = old.split('@string/')[1][:-1]
    if new.__contains__('@string/'):
        new_str = new.split('@string/')[1][:-1]
    else:
        new_str = ''

    list_kce = read_xml_as_kce_list(def_stringx)

    tmp_kce = []
    for kce in list_kce:
        if len(new_str) == 0:
            if kce.key != old_str.strip():
                tmp_kce.append(kce)
        else:  # 这是替换
            if kce.key == old_str:
                kce.key = new_str

            tmp_kce.append(kce)

    write_kce_to_path(tmp_kce, def_stringx)


def write_auto_log(module_path, old_hardcode, new_tweaked, path_of_xml):
    log_path = module_path + os.sep + 'autogen.log'
    print('log_path:', highlight(log_path, 2))

    # 格式   path_of_xml<=>hardcode<=>replaced
    separator = '\t\t<=>\t\t'
    log = new_tweaked + separator + new_tweaked + separator + path_of_xml + '\r\n'

    with open(log_path, 'a') as outer:
        outer.write(log)


def gener_replacer(list_of_kce, flag):
    old_new_dict = dict()
    for kce in list_of_kce:
        if flag == flag_and_texter:
            old = 'android:text=\"{}\"'.format(kce.cn)
            new = 'android:text=\"@string/{}\"'.format(kce.key)
            old_new_dict[old] = new
        elif flag == flag_and_hinter:
            old = 'android:hint=\"{}\"'.format(kce.cn)
            new = 'android:hint=\"@string/{}\"'.format(kce.key)
            old_new_dict[old] = new

    return old_new_dict


def hardcode_to_kce_list(dh_path_dict, path_of_module, module_kces):
    to_write_kce = list()

    for hardcode, path in dh_path_dict.items():
        # 先在本模块列表查 如果不行再在all_kce里面找 不行就生成key
        find_kce = search_value_in_list(list_of_kce=module_kces,
                                        input_value=hardcode, hc_path=path)

        if not find_kce:
            genkey = gener_key_by_hardcode(path_of_module, hardcode)
            find_kce = KCEBean(key=genkey, cn=hardcode, en='')
            to_write_kce.append(find_kce)

    return to_write_kce


def gener_key_by_hardcode(module_path, hardcode):
    """
    通过hardcode 生成key
    shorthardcode = hardcode.replace
    key = 模块名_autogen_shorthardcode
    """

    num = re.findall("\\d+", hardcode)
    if len(num) > 0:
        num = num[0]

    mps = module_path.split('/')
    module_name = mps[len(mps) - 1].lower()
    total_len = 10
    hardcode = extra_chinese(hardcode)
    tmp = str(hardcode)
    md5_str = md5(hardcode + str(num))
    hardcode = str2pinyin(hardcode)
    hardcode = hardcode[:(len(hardcode))]
    hlen = len(hardcode)
    # key = module_name + '_autogen_' + hardcode + '_' + md5_str[:total_len - hlen]
    key = module_name + '_autogen_' + hardcode + "_" + md5_str[:5]
    return key


def parse_xml_as_dict(path_of_xml, parser):
    """
    在指定文件下扫描
    android:text="@string/kry_version_name_text"
    android:hint="@string/input_address"
    ss = 'android:text=\"{}\"'.format(ret)
    """
    hardcode_path = dict()
    with open(path_of_xml.strip(), 'r') as file:
        all_str = file.read()
        if parser == 'android_text':
            matcher = r'android:text="(.*)"'
        else:
            matcher = r'android:hint="(.*)"'
        rets = re.findall(matcher, all_str)
        for ret in rets:
            if is_contains_chinese(str(ret)):
                hardcode_path[str(ret)] = path_of_xml
    return hardcode_path


def is_hard_code(str_input):
    """
    判断输入的str_input 算不算hardcode
    以@string/ 开头的不算
    纯数字不算
    .不算
    其他都算
    """
    if str_input is None:
        return False

    str_input = str(str_input).strip()

    # 空字符串不算
    if len(str_input) == 0:
        return False

    # 纯数字不算
    if str_input.isdigit():
        return False

    if str_input == '.':
        return False

    # 以@string/开头不算
    if str_input.startswith('@string'):
        return False

    # 其他情况 根据是否包含中文
    return is_contains_chinese(str_input)


def get_module_path(path):
    settings = 'settings.gradle'
    skip_dir = {'demo', 'test'}
    module_dirs = []
    for dir_path, dirs, files in os.walk(path):
        if settings in files:
            root_dir = dir_path
            os.chdir(root_dir)
            # 读取settings.gradle文件获取需要的module
            with open(root_dir + os.sep + settings, 'r') as sg:
                modules = sg.readlines()
                for m in modules:
                    if m.__contains__('include') and not m.__contains__('//'):
                        file = m.split(':')[1].split('\'')[0]
                        if not skip_dir.__contains__(file):
                            module_dirs.append(root_dir + file)

                return module_dirs


def search_value_in_list(list_of_kce, input_value, hc_path, compare='cn', ):
    is_remote_find = False
    for rem in list_all_remote:
        if not is_remote_find:
            if rem.cn == input_value:
                print(highlight('find in remote', 2),
                      ',,,,' + highlight((rem.key + "=" + rem.cn), 2) + ',hc_path' + highlight(hc_path))
                is_remote_find = True

    for it in list_of_kce:
        if compare == 'cn':
            if it.cn == input_value:
                print(highlight('find in local' + input_value, 3))
                return it
        elif compare == 'en':
            if it.en == input_value:
                return it
        else:  # 比key
            if it.key == input_value:
                return it

    return None


def pull_remote_values():
    """
    拉取主工程 en-values 下的strings.xml文件
    """
    os.chdir('/tmp/')
    remote_path = '/tmp/app/src/main/res/values/strings.xml'

    if os.path.exists(remote_path):
        return read_xml_as_kce_list(remote_path)

    # 注意这里 命令不能换行
    command = """git archive i18n_5.34.10 --remote=ssh://git@gitlab.shishike.com:38401/c_iphone/OnMobile-Android.git app/src/main/res/values/strings.xml | tar -x """
    exec_cmd(command)

    list_remote = read_xml_as_kce_list(remote_path)
    return list_remote


"""
pip install pypinyin

"""


def str2pinyin(input_str):
    a = pypinyin.pinyin(input_str, style=pypinyin.NORMAL)
    b = []
    for i in range(len(a)):
        b.append(str(a[i][0]).lower())
    c = ''.join(b)
    return c


def extra_chinese(word):
    outer = ''
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            outer += ch
    return outer


if __name__ == '__main__':
    main()
