import difflib


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2)


if __name__ == '__main__':

    pass
