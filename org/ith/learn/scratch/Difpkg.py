import difflib


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2)


if __name__ == '__main__':
    npkg = '/Users/lightman_mac/company/keruyun/proj_sourcecode/mobile-storage/package_gradle/kmobile/package_5.35.0.gradle'
    old_pkg = '/Users/lightman_mac/company/keruyun/proj_sourcecode/mobile-storage/package_gradle/kmobile/package_5.34.0.gradle'

    with open(npkg, 'r') as rin:
        npkg = rin.read()

    with open(old_pkg, 'r') as rin:
        old_pkg = rin.read()

    str1 = '我不:'
    str2 = '我不'

    seq = difflib.SequenceMatcher(lambda x: x == ",", str1, str2)
    seq = difflib.Differ().compare(str1, str2)
    print('\n'.join(list(seq)))

    import re
    s = "string. :!~@~;'{}With. Punctuation?"
    s = re.sub(r'[^\w\s]', '', s)
    print(s)

