
vowels = ['a','e','i','o','u']
word = input('provide a word to search for vowels:\n')

found = {}
for f in vowels:
    found[f] = 0

for w in word:
    if w in vowels:
        found[w] += 1

for k,v in sorted(found.items()):
    print(k,'was found',v,' time(s).')

