import random
import sys
import time
import requests
import json
import os

from multiprocessing import Process

from org.ith.learn.util.TUtils import exec_cmd

cmd_list = []

dest_all_path = '/Users/lightman_mac/company/keruyun/all_gitlab_code'


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
        'Cookie': "sidebar_collapsed=false; __utmz=88038286.1580971726.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=("
                  "none); __utma=88038286.1460782901.1580971726.1584367992.1585327915.11; "
                  "remember_user_token"
                  "=W1s4NjFdLCIkMmEkMTAkMHdtaEM0ckpDUDZjSk5rbFo5ZTFyTyIsIjE1ODU1Nzg1OTAuMjg3MDA3Il0%3D"
                  "--973f22857312ff21d733523deafc897321268556; _gitlab_session=6c43f845a0e5db7606c204183e77f25d",
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
    time.sleep(random.randint(0, 20))
    ret = exec_cmd(command)


def loopUrl():
    for i in range(4):
        gitlab(page=i)

    while 1:
        pass


if __name__ == "__main__":
    sys.exit(main())
