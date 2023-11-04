import sys
import re

class MinBinaryHeap:
    
    def __init__(self):
        self._heap = []
        self._key_to_index = {} # используем хэш-таблицу для быстрого доступа к индексам элементов в куче по ключу
        # то есть реализуем константное время

    def insert(self, key, value):
        if key in self._key_to_index:
            index = self._key_to_index[key]
            self._heap[index] = (key, value)
            self._heapify_up(index)
        else:
            self._key_to_index[key] = len(self._heap)
            self._heap.append((key, value))
            self._heapify_up(len(self._heap) - 1)

    def set(self, key, value):
        if not self._heap:
            print ("error")
            return
        if key in self._key_to_index:
            index = self._key_to_index[key]
            self._heap[index] = (key, value)
            self._heapify_up(index)
            self._heapify_down(index)
        else:
            self.insert(key, value)

    def delete(self, key):
        if key in self._key_to_index:
            index = self._key_to_index[key]
            last_element = self._heap.pop()
            if index < len(self._heap):
                self._heap[index] = last_element
                self._key_to_index[last_element[0]] = index
                self._heapify_up(index)
                self._heapify_down(index)
            del self._key_to_index[key]

    def search(self, key):
        if key in self._key_to_index:
            index = self._key_to_index[key]
            value = self._heap[index][1]
            return f"1 {index} {value}"
        else:
            return "0"

    def min(self):
        if not self._heap:
            return "error"
        min_key, min_value = min(self._heap, key=lambda x: x[0])
        min_index = self._key_to_index[min_key]
        return f"{min_key} {min_index} {min_value}"

    def max(self):
        if not self._heap:
            return "error"
        max_key, max_value = max(self._heap, key=lambda x: x[0])
        max_index = self._key_to_index[max_key]
        return f"{max_key} {max_index} {max_value}"

    def extract(self):
        if not self._heap:
            return "error"
        key, value = self._heap[0]
        self.delete(key)
        return f"{key} {value}"

    def print(binary_heap):
        
        level, index, flag = 1, 0, False
        while not flag:
            ins, li = [None] * level, 0
            if index + level < len(binary_heap._heap):
                upper_bound = index + level
            else:
                flag, upper_bound, it = True, len(binary_heap._heap), len(binary_heap._heap) - index
                while it < level:
                    ins[it] = '_'
                    it += 1
            while index < upper_bound:
                value = binary_heap._heap[index]
                if index == 0:
                    ins[li] = f'[{value[0]} {value[1]}]'
                elif li == 0:
                    parent_key = binary_heap._get_parent_key(value[0]) if binary_heap._get_parent_key(value[0]) is not None else "_"
                    ins[li] = f'[{value[0]} {value[1]} {parent_key}]'
                else:
                    parent_key = binary_heap._get_parent_key(value[0]) if binary_heap._get_parent_key(value[0]) is not None else "_"
                    ins[li] = f'[{value[0]} {value[1]} {parent_key}]'
                li += 1
                index += 1
            level *= 2
            print(' '.join(ins))



    def _get_parent_key(self, key):
        parent_index = (self._key_to_index[key] - 1) // 2
        if parent_index >= 0:
            return self._heap[parent_index][0]
        return "_"

    def _heapify_up(self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if self._heap[index][0] < self._heap[parent_index][0]:
                self._swap(index, parent_index)
                index = parent_index
            else:
                break

    def _heapify_down(self, index):
        while True:
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2
            smallest = index

            if (
                left_child_index < len(self._heap)
                and self._heap[left_child_index][0] < self._heap[smallest][0]
            ):
                smallest = left_child_index

            if (
                right_child_index < len(self._heap)
                and self._heap[right_child_index][0] < self._heap[smallest][0]
            ):
                smallest = right_child_index

            if smallest == index:
                break

            self._swap(index, smallest)
            index = smallest

    def _swap(self, i, j):
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
        self._key_to_index[self._heap[i][0]] = i
        self._key_to_index[self._heap[j][0]] = j


heap = MinBinaryHeap()

for line in sys.stdin:
    space = [m.start() for m in re.finditer(' ', line)]

    if line == '\n':
        pass

    elif re.match(r'add\s[^\s]*\s[^\s]*', line) and len(space) == 2:
        key_str, value = line[4:space[1]], line[space[1] + 1:len(line) - 1]
        if key_str.isdigit():
            key = int(key_str)
            if key in heap._key_to_index:
                print('error')
            else:
                heap.insert(key, value)
        elif key_str[0] == '-' and key_str[1:].isdigit():
            key = -int(key_str[1:])
            if key in heap._key_to_index:
                print('error')
            else:
                heap.insert(key, value)
        else:
            print('error')

    elif (re.match(r'set\s[^\s]*\s[^\s]*', line)) and (len(space) == 2):
        key_str, value = line[4:space[1]], line[space[1] + 1:len(line) - 1]
        if key_str.isdigit():
            key = int(key_str)
            if key in heap._key_to_index:
                heap.set(key, value)
            else:
                print('error')
        elif key_str[0] == '-' and key_str[1:].isdigit():
            key = -int(key_str[1:])
            if key in heap._key_to_index:
                heap.set(key, value)
            else:
                print('error')
        else:
            print('error')

    elif re.match(r'delete\s[^\s]*\s*', line):
        if len(line) > 7:
            key_str = line[7:len(line) - 1].strip()
            if key_str.isdigit():
                key = int(key_str)
                if key not in heap._key_to_index:
                    print('error')
                else:
                    heap.delete(key)
            elif key_str.startswith('-') and key_str[1:].isdigit():
                key = -int(key_str[1:])
                if key not in heap._key_to_index:
                    print('error')
                else:
                    heap.delete(key)
            else:
                print('error')
        else:
            print('error')
            
    elif re.match(r'search\s[^\s]*\s*', line):
        if len(line) > 7:
            key_str = line[7:len(line) - 1].strip()
            if key_str.isdigit():
                key = int(key_str)
                result = heap.search(key)
                print(result)
            elif key_str.startswith('-') and key_str[1:].isdigit():
                key = -int(key_str[1:])
                result = heap.search(key)
                print(result)
            else:
                print('error')
        else:
            print('error')

    elif line == 'min\n':
        result = heap.min()
        print(result)

    elif line == 'max\n':
        result = heap.max()
        print(result)

    elif line == 'extract\n':
        result = heap.extract()
        print(result)

    elif line == 'print\n':
        heap.print()

    else:
        print('error')
