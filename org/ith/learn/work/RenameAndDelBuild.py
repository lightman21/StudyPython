import os
import shutil


def main():
    # dir_path = '/Users/lightman_mac/company/keruyun/proj_sourcecode/OnMobile-Android/app/src/main/res/'
    dir_path = '/Users/lightman_mac/.gradle'
    # dir_path = '/Users/lightman_mac/thtmp/anr/try_gradle'
    cout = 1
    for dir_path_name, dirs, files in os.walk(dir_path):
        if len(files) > 0:
            for f in files:
                real_path = dir_path_name + "/" + f
                real_size = os.path.getsize(real_path) / 1024 / 1024
                # out = '/tmp/th/del/' + 'big/' + real_path
                # dst = shutil.move(dir_path_name, out)
                if real_size > 20:
                    print('-------->',real_path,real_size,"M")

        # print(dir_path_name,"dirs -> ",dirs,", files -> ",files,len(files))
        # size = os.path.getsize(dir_path_name) / 1024 / 1024
        # print(dir_path_name,' ,size ',size)

        if dir_path_name.endswith('.1git'):
            # dst = shutil.move(dir_path_name, out)
            new_name = dir_path_name.split(".git")[0] + "__git__"
            # print("split -> ",dir_path_name.split(".git")[0],new_name)
            os.rename(dir_path_name, new_name)
            print(dir_path_name, new_name, cout)
        cout = cout + 1
    pass


if __name__ == '__main__':
    main()
