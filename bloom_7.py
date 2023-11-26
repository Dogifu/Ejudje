import math
import re


class BloomFilter:
    def __init__(self):
        self.bit_array = 0
        self.size = 0
        self.num_hash_functions = 0
        self.is_set = False
        self.MERSENNE_PRIME = 2147483647

    @staticmethod
    def get_nth_prime(n):
        if n <= 0:
            return 0
        if n == 1:
            return 2

        count = 1
        num = 3

        while count < n:
            is_prime = True

            for i in range(2, int(math.sqrt(num)) + 1):
                if num % i == 0:
                    is_prime = False
                    break

            if is_prime:
                count += 1

            if count < n:
                num += 2

        return num

    def hash_function(self, i, key):
        prime = self.get_nth_prime(i + 1)
        return ((i + 1) * key + prime) % self.MERSENNE_PRIME % self.size

    def set(self, n, P):
        if self.is_set or n <= 0 or P >= 1 or P <= 0:
            raise ValueError("Invalid input")

        self.size = round(-n * math.log2(P) / math.log(2))
        self.num_hash_functions = round(-math.log2(P))

        if self.size <= 0 or self.num_hash_functions <= 0:
            raise ValueError("Invalid input")

        self.bit_array = 0
        self.is_set = True

        return self.size, self.num_hash_functions

    def add(self, key):
        if not self.is_set or key < 0:
            raise ValueError("Structure is not initialized or invalid input")
        for i in range(self.num_hash_functions):
            index = self.hash_function(i, key)
            self.bit_array |= (1 << index)

        return True

    def search(self, key):
        if not self.is_set or key < 0:
            raise ValueError("Structure is not initialized or invalid input")

        for i in range(self.num_hash_functions):
            index = self.hash_function(i, key)
            if not (self.bit_array & (1 << index)):
                return False

        return True

    def print_filter(self):
        if not self.is_set:
            return ""

        result = bin(self.bit_array)[2:].zfill(self.size)
        return result


def main():
    filter = BloomFilter()

    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            continue
        try:
            if re.fullmatch(r'set (0|([1-9]\d*)) ([-+]?((\d+\.\d*)|(\d*\.\d+)|(\d+)))', line):
                _, n, p = re.split(' ', line)
                size, num_hash_functions = filter.set(int(n), float(p))
                print(f"{size} {num_hash_functions}")
            elif re.fullmatch(r'add (0|([1-9]\d*))', line):
                _, k = re.split(' ', line)
                filter.add(int(k))
            elif re.fullmatch(r'search (0|([1-9]\d*))', line):
                _, k = re.split(' ', line)
                result = filter.search(int(k))
                print('1' if result else '0')
            elif line == 'print':
                result = filter.print_filter()
                print('error' if result == "" else result[::-1])
            else:
                print('error')
        except Exception:
            print('error')


if __name__ == '__main__':
    main()
