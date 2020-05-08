"""
smb://172.16.0.17
"""
import time

from smb.SMBConnection import SMBConnection

from org.ith.learn.util.TUtils import human_time


def main():
    host = "172.16.0.17"
    username = "kry"
    password = "kry"
    conn = SMBConnection(username, password, "", "", use_ntlm_v2=True)
    result = conn.connect(host, 445)  # smb协议默认端口445
    print("登录成功")

    shares = conn.listShares()

    for share in shares:
        if not share.isSpecial and share.name not in ['NETLOGON', 'SYSVOL']:
            # sharedfiles = conn.listPath(share.name, '/keruyun-mobile/android/kmobile-android/envGrd/5.36.0/20200508')
            sharedfiles = conn.listPath(share.name, '/keruyun-mobile/android/kmobile-android/envGrd/')
            for sharedfile in sharedfiles:
                # help(sharedfile)
                if not str(sharedfile.filename).startswith('.'):
                    to_str = '{:<20} {:<20}'.format(sharedfile.filename,
                                                    human_time(sharedfile.create_time))
                    print(to_str, sharedfile.isNormal)

    pass


if __name__ == '__main__':
    main()
