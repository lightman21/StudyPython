def isAllLettersUsed(word, required):
	rs = ''.join(sorted(set(required))).replace(' ','')
	rw = ''.join(sorted(set(word))).replace(' ','')
	print(rs)
	print(rw)
	return rw.__contains__(rs)

if __name__ == '__main__':
    w = 'learning python'
    r = 'google'
    isAllLettersUsed(w,r)
