from __future__ import division, print_function

words = open('wordsEn.txt').readlines()
words = set(word.strip() for word in words)

for line in open('homophones103.txt', 'r').readlines():
    hs = line.split(',')
    for h in hs[1:]:
        words.discard(h)

words = sorted(words)

with open('wordlist.csv', 'wb') as f:
    f.write(','.join(words))
