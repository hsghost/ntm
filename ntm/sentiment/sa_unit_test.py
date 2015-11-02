#!/usr/bin/python

import sa

file_path = "ch.txt"

f = open(file_path)

n, c = 0, 0

for line in f:
    n += 1
    t = eval(line)
    print "Test {0}: -----------------------".format(n)
    print t[0]
    s = sa.sa_text(t[0])
    print "Tag: {0}".format(t[1])
    print "Predict: {0}".format(s)
    if s == t[1]:
        c += 1

print "Test passed: {0}/{1}".format(c, n)
print ""

print "Top 1:"
print sa.sa_main(1)
print ""

print "Top 2:"
print sa.sa_main(2)
print ""

print "Top 20:"
print sa.sa_main()
print ""
