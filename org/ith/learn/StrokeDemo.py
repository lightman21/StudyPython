def get_stroke(hanzi):
    """
    输入汉字 输出笔画  如 唐 10 浩10
    如果返回 0,则也是在unicode中不存在kTotalStrokes字段
    """
    strokes = []
    with open('../../../docs/py_strokes.py', 'r') as fr:
        for line in fr:
            strokes.append(int(line.strip()))
    unicode_ = ord(hanzi)

    if 13312 <= unicode_ <= 64045:
        return strokes[unicode_ - 13312]
    elif 131072 <= unicode_ <= 194998:
        return strokes[unicode_ - 80338]
    else:
        print("c should be a CJK char, or not have stroke in unihan data.")
        return -1


if __name__ == '__main__':
    print(get_stroke('浩'))
