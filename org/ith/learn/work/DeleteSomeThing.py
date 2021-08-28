import os
import shutil


def main():
    # dir_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/src/main/res/'
    dir_path = '/tmp/th/lib_common/'
    # dir_path = '/Users/lightman_mac/thtmp/anr/try_gradle'
    count = 1
    limit = 20
    for dir_path_name, dirs, files in os.walk(dir_path):
        for file in files:
            real_path = dir_path_name + os.sep + file
            if real_path.endswith(".java") or real_path.endswith(".kt"):
                if count < limit:
                    handleFile(real_path)
                count = count + 1


def handleFile(real_path):
    print("real_path: ", real_path)
    with open(real_path, "r", encoding='utf-8') as text:
        lines = text.readlines()

        with open(real_path, 'w', encoding='utf-8') as f_w:

            for line in lines:
                if line.__contains__("*") \
                        and (line.__contains__("author") or line.__contains__("作者") or line.__contains__("created by")):
                    spt = line.split("*")
                    lenth = len(spt)
                    if lenth == 2:
                        oldstr = spt[1]
                        print('before ', line)
                        line = line.replace(oldstr, "\t-_-\n")
                        f_w.write(line)
                        continue

                f_w.write(line)


if __name__ == '__main__':
    main()
