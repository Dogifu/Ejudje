import re
import sys


def print_error():
    print('error')


def print_overflow():
    print('overflow')


def print_underflow():
    print('underflow')


def print_empty():
    print('empty')


bool_check = 0
for line in sys.stdin:
    if re.match(r'set_size [^\s]*', line):
        if bool_check == 0:
            STROKA = line[9:len(line) - 1:1]
            if STROKA.isdigit():
                deq_size = int(STROKA)
                deq = [None] * deq_size
                bool_check = 1
                golova = -1
                tail = 0
            elif STROKA == '-0':
                deq_size = int(line[10:len(line) - 1:1])
                deq = [None] * deq_size
                bool_check = 1
                golova = -1
                tail = 0
            else:
                print_error()
        else:
           print_error()
    elif line == '\n':
        pass
    elif bool_check == 0:
        print_error()
    elif re.match(r'pushb [^\s]*', line) or re.match(r'pushf [^\s]*', line):
        if (line[5:6] == '\n') or (' ' in line[6:len(line) - 1:1]) or ('\t' in line[6:len(line) - 1:1]):
            print_error()
        elif (deq_size == 0) or (golova == (tail + 1) % deq_size):
            print_overflow()
        else:
            if golova == -1:
                golova = 0
                deq[golova] = line[6: len(line) - 1:1]
            elif re.match(r'pushb [^\s]*', line):
                tail = (tail + 1) % deq_size
                deq[tail] = line[6: len(line) - 1:1]
            else:
                golova = (golova - 1) % deq_size
                deq[golova] = line[6: len(line) - 1:1]
    elif (line == 'popf\n') or (line == 'popb\n'):
        if (deq_size == 0) or (golova == -1):
           print_underflow()
        else:
            if line == 'popf\n':
                print(deq[golova])
                deq[golova] = None
            else:
                print(deq[tail])
                deq[tail] = None
            if golova == tail:
                golova = -1
                tail = 0
            elif line == 'popf\n':
                golova = (golova + 1) % deq_size
            else:
                tail = (tail - 1) % deq_size
    elif line == 'print\n':
        if (deq_size == 0) or (golova == -1):
            print_empty()
        else:
            if tail >= golova:
                for i in range(golova, tail + 1):
                    if i == tail:
                        print(deq[i])
                    else:
                        print(deq[i], end=' ')
            else:
                for i in range(golova, deq_size):
                    print(deq[i], end=' ')
                for i in range(0, tail + 1):
                    if i == tail:
                        print(deq[i])
                    else:
                        print(deq[i], end=' ')
    else:
        print_error()