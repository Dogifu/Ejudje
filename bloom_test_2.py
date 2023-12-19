import re
import math


'''
В стандартном Python массиве булевых значений каждый бит обычно занимает 8 бит (1 байт) 
из-за особенностей внутреннего представления данных и выравнивания. 
Таким образом, массив из 8 булевых значений будет занимать минимум 8 байт памяти.

Но в данной реализации каждый бит хранится как отдельное значение, 
и мы можем эффективно упаковать восемь битов в один байт. 
Это позволяет экономить память, особенно при работе с большими объемами данных.
Итого, экономия памяти примерно в 8 раз!
'''


class BitArray:
    def __init__(self, size):
        self.size = size
        self.array = 0

    def set_bit(self, index):
        self.array |= (1 << index)

    def get_bit(self, index):
        return bool(self.array & (1 << index))

    def __str__(self):
        return bin(self.array)[2:].zfill(self.size)[::-1]

# вычисляем наши простые числа только один раз и затем раз при
# вызове set_filter и сохраняем их для последующего использования в методе hash_function.


class BloomFilter:
    def precompute_primes(self, n):
        primes = [2]
        num = 3
        while len(primes) < n:
            is_prime = all(num % i != 0 for i in primes if i * i <= num)
            if is_prime:
                primes.append(num)
            num += 2
        return primes

    def hash_function(self, i, key):
        if not hasattr(self, 'primes') or self.primes is None:
            raise ValueError("Primes not precomputed. Call set_filter first.")

        prime = self.primes[i]
        result = ((i + 1) * key + prime) % self.Mersenne_Value
        return result % self.size

    def calculate_filter_params(self, n, P):
        size = round(-n * math.log2(P) / math.log(2))
        num_hash_functions = round(-math.log2(P))
        if num_hash_functions < 1:
            raise ValueError("error")
        return size, num_hash_functions

    def __init__(self):
        self.bit_array = None
        self.size = None
        self.num_hash_functions = 1
        self.Mersenne_Value = 2 ** 31 - 1

    def set_filter(self, n, P):
        if self.bit_array is not None or n < 1 or not 0 < P < 1:
            raise ValueError("error")

        self.size, self.num_hash_functions = self.calculate_filter_params(n, P)
        if self.num_hash_functions is not None:
            primes = self.precompute_primes(self.num_hash_functions)
            self.bit_array = BitArray(self.size)
            self.primes = primes
            return self.size, self.num_hash_functions
        else:
            raise ValueError("error")

    def add_element(self, key):
        if self.bit_array is None:
            raise ValueError("error")
        for i in range(self.num_hash_functions):
            index = self.hash_function(i, key)
            self.bit_array.set_bit(index)
        return True

    def search_element(self, key):
        if self.bit_array is None:
            raise ValueError("error")
        return all(self.bit_array.get_bit(self.hash_function(i, key)) for i in range(self.num_hash_functions))

    def print_filter(self):
        if self.bit_array is None:
            return ""
        return str(self.bit_array)


def process_set_command(filter, n, p):
    size, num_hash_functions = filter.set_filter(n, p)
    print(f"{size} {num_hash_functions}")


def process_add_command(filter, k):
    filter.add_element(k)


def process_search_command(filter, k):
    result = filter.search_element(k)
    if result:
        print('1')
    else:
        print('0')


def process_print_command(filter):
    result = filter.print_filter()
    if result == '':
        print('error')
    else:
        print(result)


filter = BloomFilter()
while True:
    try:
        line = input()
    except EOFError:
        break
    if line:
        try:
            if re.fullmatch(r'set (-?\d+) ([-+]?\d+(\.\d*)?)', line):
                _, n, p = re.split(' ', line, maxsplit=2)
                process_set_command(filter, int(n), float(p))
            elif re.fullmatch(r'add (0|([1-9]\d*))', line):
                _, k = re.split(' ', line, maxsplit=1)
                process_add_command(filter, int(k))
            elif re.fullmatch(r'search (0|([1-9]\d*))', line):
                _, k = re.split(' ', line, maxsplit=1)
                process_search_command(filter, int(k))
            elif line == 'print':
                process_print_command(filter)
            else:
                print('error')
        except ValueError:
            print('error')
