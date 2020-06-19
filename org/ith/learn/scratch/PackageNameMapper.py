import os


class NameWhereBean:
    aar_name_dict = {
        'com.keruyun.mobile.dinner': '正餐',
        'com.keruyun.mobile.klight': '正餐',
        'com.keruyun.mobile.mobile.tradeserver': '快餐',
        'com.keruyun.mobile.tradeui.library': '快餐',
        'com.keruyun.mobile.tradeui.klight': '快餐',
        'com.keruyun.mobile.tradeui.klightlib': '快餐',
        'com.keruyun.mobile.tradeui.kmobile''': '快餐',
        'com.keruyun.kmobile.kreport': '报表',
        'com.keruyun.kmobile.kmobile.commodity': '商品管理',
        'com.keruyun.kmobile.kmobile.inventory.management.ui': '库存',
        'com.keruyun.kmobile.kmobile.member.manage': '会员管理',
        'com.keruyun.kmobile.kmobile.order.center': '订单中心',
        'com.keruyun.kmobile.kmobile.takeout.ui': '外卖',
        'com.keruyun.kmobile.kmobile.business.setting': '经营设置',
        'com.keruyun.kmobile.kmobile.staff': '员工管理',
        'com_keruyun.kmobile.third.loan.ocr.live.body': 'ocr相关body',
        'com.keruyun.kmobile.ai.kmobile.android.ocr.dish.contain': 'ocr相关',
        'com.keruyun.print.print': '打印',
        'com.keruyun.kmobile.kmobile.coupon': '验券',
        'com.keruyun.mobile.manage.table.code': '移动门店',
        'com.keruyun.mobile.paycenter.board': '支付中心',
        'com.keruyun.osmobile.cashpay': '现金支付',
        'com.keruyun.osmobile.groupcoupon': 'groupcoupon',
        'com.keruyun.osmobile.member': '会员',
        'com.keruyun.osmobile.tradebusiness': '正快餐基础库',
        'com.keruyun.kmobile.kmobile.accountsystem.core': '登录模块Core',
        'com.keruyun.kmobile.kmobile.accountsystem.ui': '登录模块UI',
        'com.keruyun.android.printcenter': '打印中心',
        'com.keruyun.android.qrcode': '二维码',
        'com.keruyun.android.batman.card': 'batman',
        'com.keruyun.android.android.mobileui': 'mobileui基础库',
        'com.keruyun.android.android.mobilecommondata': 'mobilecommondata',
        'com.keruyun.kmobile.kmobile.table.manage': '桌台管理',
        'com.keruyun.kmobile.kmobile.smart.management': '经营顾问',
        'com.keruyun.kmobile.iot': 'iot物联网',
    }


def get_aar_name(file_name, aar_name_dict=None):
    if aar_name_dict is None:
        aar_name_dict = NameWhereBean.aar_name_dict
    aar_name = file_name.split('___')[0].replace('_', '.')
    for k, v in aar_name_dict.items():
        if aar_name.startswith(k):
            return v


def gener_name_where():
    """
    希望在这里生成kcew
    """
    total_dir = get_newest_path()

    name_where_dict = dict()
    for dir_path_name, dirs, files in os.walk(total_dir):
        for file in files:
            if file.startswith('__string_array'):
                continue
            full_path = dir_path_name + file
            human_name = get_aar_name(file)
            print(human_name, full_path)
            from org.ith.learn.util.TUtils import read_xml_as_kce_list
            kce_list = read_xml_as_kce_list(full_path)
            for kce in kce_list:
                name_where_dict[kce.key] = human_name

    print('name_where_dict size ', len(name_where_dict))
    return name_where_dict


def get_newest_path():
    total_dir = '../scratch/tmp/auto_extract_work/'
    for dir_path_name, dirs, files in os.walk(total_dir):
        if len(dirs) > 0:
            from org.ith.learn.util.TUtils import modify_timestamp
            max_time = 0
            time_path = dict()
            for pdir in dirs:
                pstr = dir_path_name + pdir
                mtt = modify_timestamp(pstr)
                if mtt > max_time:
                    max_time = mtt
                    time_path.clear()
                    time_path[max_time] = pstr

            new_path = time_path.popitem()[1]
            print("the newest path is ", new_path)
            return new_path + os.sep


if __name__ == '__main__':
    # main()
    # gener_name_where()
    pass
