import random
import sys
import time
import requests
import json
import os

from multiprocessing import Process

from org.ith.learn.util.TUtils import exec_cmd, highlight

cmd_list = []

# dest_all_path = '/Users/lightman_mac/company/keruyun/all_gitlab_code'
dest_all_path = '/tmp/tanghaohao/'

"""
_ga=GA1.2.890225156.1571303130; __utmz=88038286.1571707491.12.5.utmcsr=cdjk.shishike.com|utmccn=(referral)|utmcmd=referral|utmcct=/jenkins/me/my-views/view/all/job/Keruyun-Mobile/job/kmobile-android-module/job/OnMobile_Android_Lib_KReport/580/changes; sidebar_collapsed=false; gr_user_id=5ad0cae1-3e25-466a-87c9-307732bf6d9d; grwng_uid=93a3c8a9-431f-4d4a-bbaa-ff337ae759bd; _gitlab_session=8f5e9ba0ced4f566bd4336801f6a7993; __utmc=88038286; __utma=88038286.1765784403.1568081186.1586832252.1587017207.101; _gid=GA1.2.2086868300.1587086109
"""


def main():
    proc = Process(target=loopUrl)
    proc.start()


def gitlab(base_url='http://gitlab.shishike.com/groups/c_iphone/-/children.json?page=', page=0):
    body = {}
    url = base_url + str(page)

    headers = {
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'Cache-Control': "no-cache",
        'Connection': "keep-alive",
        'Cookie': "_ga=GA1.2.890225156.1571303130; __utmz=88038286.1571707491.12.5.utmcsr=cdjk.shishike.com|utmccn=(referral)|utmcmd=referral|utmcct=/jenkins/me/my-views/view/all/job/Keruyun-Mobile/job/kmobile-android-module/job/OnMobile_Android_Lib_KReport/580/changes; sidebar_collapsed=false; gr_user_id=5ad0cae1-3e25-466a-87c9-307732bf6d9d; grwng_uid=93a3c8a9-431f-4d4a-bbaa-ff337ae759bd; _gitlab_session=8f5e9ba0ced4f566bd4336801f6a7993; __utmc=88038286; __utma=88038286.1765784403.1568081186.1586832252.1587017207.101; _gid=GA1.2.2086868300.1587086109",
        'Host': "gitlab.shishike.com",
        'Pragma': "no-cache",
        'Referer': "http://gitlab.shishike.com/c_iphone",
        'User-Agent': "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, "
                      "like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36",
        'X-CSRF-Token': "7gQxJ/3DA2dPC4zwxasA/Tjfg2qPYrNudksvtQeTaoubc9aVvGpFKzMrEId9RpS3kMFV5NBK+vnL+H+sFxQdCA==",
        'X-Requested-With': "XMLHttpRequest"
    }

    response = requests.get(url, data=json.dumps(body), headers=headers)
    resp = (response.json())

    global cmd_list

    for re in resp:

        addr = "git clone -b develop ssh://git@gitlab.shishike.com:38401/c_iphone/" + re['name'] + ".git"

        if addr in cmd_list:
            print(addr, " contains return")
            continue
        else:
            cmd_list.append(addr)

        try:
            tproc = Process(target=execute_command, args=(addr,))
            tproc.start()
        except Exception as e:
            print(e)
            print("Error: 无法启动进程", e)

    print("================after forlop====================")


def execute_command(command):
    os.chdir(dest_all_path)
    time.sleep(random.randint(0, 10))
    # ret = exec_cmd(command)


def loopUrl():
    for i in range(4):
        gitlab(page=i)

    while 1:
        pass


def write_repo(dest='/tmp/gitlab_repo_all.txt'):
    print('--------------global list ', len(cmd_list), str(cmd_list))
    tmp = []
    for t in cmd_list:
        tmp.append(t)
        tmp.append('\n')
    with open(dest, 'w') as out:
        out.writelines(tmp)


if __name__ == "__main__":
    sys.exit(main())
