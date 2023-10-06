import re
import sys

numlist = list()
for line in sys.stdin:
    for value in re.findall(r'-?[0-9]+', line):
        numlist.append(int(value))
print(sum(numlist))