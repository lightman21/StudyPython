def shiftByTwo(*args):
	args = list(args)
	if len(args) >= 2:
		last = args.__getitem__(len(args)-1)
		laast = args.__getitem__(len(args)-2)
		args.insert(0,last)
		args.insert(1,laast)
		index = args.rindex(args.__getitem__(len(args)-2))
        args = ''.join(args)
		return args[:index]
        else:
        return args

if __name__ == '__main__':
    print(shiftByTwo(1,2,3,4,5,6))