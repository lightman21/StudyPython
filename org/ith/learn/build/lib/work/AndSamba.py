"""
smb://172.16.0.17
"""
import os
import time

from smb.SMBConnection import SMBConnection

from org.ith.learn.util.TUtils import human_time, highlight

"""
怎么获取前一天build的apk

"""
my_smb_file = ''


def main():
    host = "172.16.0.17"
    username = "kry"
    password = "kry"
    conn = SMBConnection(username, password, "", "", use_ntlm_v2=True)
    result = conn.connect(host, 445)  # smb协议默认端口445
    print("登录成功")

    find_lastest_apk(conn)
    pull_apk(conn, my_smb_file)

    pass


def pull_apk(smb_conn, remote_path):
    start = time.time()
    print('start pull apk ', highlight(remote_path, 3))
    file_path = remote_path.split('/')[-1]
    localFile = open('/tmp/' + file_path, "wb")
    localFile = open('/tmp/xiu.apk', "wb")
    # conn.retrieveFile("client-apk", "keruyun-mobile/android/kmobile-android/envGrd/5.36.0/20200508/OnMobile-official-5.36.0-SNAPSHOT-armeabi-v7a-envGrd-2020-05-08-16-49-02.apk", localFile)
    smb_conn.retrieveFile("client-apk", remote_path, localFile)
    print('done that pull apk ', highlight(remote_path, 2), 'cost ', (time.time() - start), ' s')


# def find_lastest_apk(smb_conn, base_dir='/keruyun-mobile/android/kmobile-android/'):
def find_lastest_apk(smb_conn, base_dir='/keruyun-mobile/'):
    """
    找到最近更新的apk文件
    """
    shares = smb_conn.listShares()
    max_timestamp = 0
    max_tt_file = 0
    for share in shares:
        if not share.isSpecial and share.name not in ['NETLOGON', 'SYSVOL']:
            sharedfiles = smb_conn.listPath(share.name, base_dir)
            for sharedfile in sharedfiles:
                if not str(sharedfile.filename).startswith('.'):
                    if sharedfile.create_time > max_timestamp:
                        max_timestamp = sharedfile.create_time
                        max_tt_file = sharedfile
                    to_str = '{:<20} {:<20}'.format(sharedfile.filename,
                                                    human_time(sharedfile.create_time))

                    print(to_str, sharedfile.isNormal, '\t ', sharedfile.create_time)

            # for 循环完了如果不满足isNormal 就继续追加文件名继续找
            print('max timestamp:', human_time(max_timestamp), ', max_tt_file:', max_tt_file.filename,
                  'sharedfile.isNormal:', max_tt_file.isNormal)

            if max_tt_file.isNormal:
                print(highlight(base_dir + os.sep + max_tt_file.filename, 2))
                global my_smb_file
                my_smb_file = base_dir + os.sep + max_tt_file.filename
                return base_dir + os.sep + max_tt_file.filename

            if max_tt_file is not None and not max_tt_file.isNormal:
                base_dir = base_dir + os.sep + max_tt_file.filename
                print('recursive search ', base_dir)
                find_lastest_apk(smb_conn, base_dir)


if __name__ == '__main__':
    main()
