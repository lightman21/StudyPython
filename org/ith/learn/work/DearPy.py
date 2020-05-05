if __name__ == '__main__':
    path = '/Users/toutouhiroshidaiou/keruyun/INTELLIJ_IDEA/PycharmProjects/org/ith/learn/work/2020_05_06_10:00_work_pic_every_path.xml'
    with open(path, 'r') as rin:
        lines = rin.readlines()
        lines = sorted(lines)
        with open('./sort_path.xml', 'w') as rout:
            rout.writelines(lines)
