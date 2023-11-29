import sys
import re


class Node:
    def __init__(self, key=None, value=None,
                 left=None, right=None, parent=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent


class SplayTree:
    def __init__(self):
        self.root = None

    def zig(self, node):
        parent = node.parent
        grandparent = parent.parent
        parent.left = node.right

        if node.right is not None:
            node.right.parent = parent
        node.right = parent
        parent.parent = node

        if grandparent is not None:
            if grandparent.left == parent:
                grandparent.left = node
            else:
                grandparent.right = node
        node.parent = grandparent

        return node

    def zag(self, node):
        parent = node.parent
        grandparent = parent.parent
        parent.right = node.left

        if node.left is not None:
            node.left.parent = parent
        node.left = parent
        parent.parent = node

        if grandparent is not None:
            if grandparent.left == parent:
                grandparent.left = node
            else:
                grandparent.right = node
        node.parent = grandparent

        return node

    def zig_zag(self, node):
        node = self.zig(node)
        node = self.zag(node)
        return node

    def zag_zig(self, node):
        node = self.zag(node)
        node = self.zig(node)
        return node

    def zig_zig(self, node):
        node.parent = self.zig(node.parent)
        node = self.zig(node)
        return node

    def zag_zag(self, node):
        node.parent = self.zag(node.parent)
        node = self.zag(node)
        return node

    def splay(self, node):
        while node and node.parent is not None:
            parent = node.parent
            grandparent = parent.parent

            if grandparent is None:
                if node == parent.left:
                    node = self.zig(node)
                else:
                    node = self.zag(node)
            elif node == parent.left and parent == grandparent.left:
                node = self.zig_zig(node)
            elif node == parent.right and parent == grandparent.right:
                node = self.zag_zag(node)
            elif node == parent.right and parent == grandparent.left:
                node = self.zag_zig(node)
            else:
                node = self.zig_zag(node)

        if node and node.parent is None:
            self.root = node

    def find_closest(self, key):
        current = self.root
        closest = None

        while current:
            if key < current.key:
                closest = current
                current = current.left
            elif key > current.key:
                closest = current
                current = current.right
            else:
                return current

        return closest

    def add(self, key, value):
        node = Node(key, value)
        root = self.root
        parent = None

        if key is None or value is None:
            raise ValueError('Invalid input: Key and value must not be None')

        if self.root is None:
            self.root = node
            return

        while root is not None:
            parent = root
            if key < root.key:
                root = root.left
            elif key > root.key:
                root = root.right
            else:
                self.splay(root)
                raise ValueError('Element already exists')

        if node.key < parent.key:
            parent.left = node
        else:
            parent.right = node
        node.parent = parent
        self.splay(node)

    def find_extreme(self, node, direction):
        while getattr(node, direction) is not None:
            node = getattr(node, direction)
        self.splay(node)
        return node

    def min(self, tree):
        if self.root is None:
            return False
        return self.find_extreme(tree, 'left')

    def max(self, tree):
        if self.root is None:
            return False
        return self.find_extreme(tree, 'right')

    def search(self, key):
        node = self.root
        closest = None

        while node:
            if key == node.key:
                self.splay(node)
                return node
            elif key < node.key:
                closest = node
                node = node.left
            else:
                closest = node
                node = node.right

        if closest:
            self.splay(closest)
        return None

    def set(self, key, value):
        if self.root is None:
            raise ValueError('Tree is empty')
        node = self.search(key)
        if node:
            node.value = value
            self.splay(node)
        else:
            raise ValueError('Element not found')
        return

    def delete(self, key):
        if self.root is None:
            raise ValueError('Tree is empty')
        elif self.search(key):
            if self.root.right is None and self.root.left is None:
                self.root = None
            elif self.root.right is None:
                self.root.left.parent = None
                self.root = self.root.left
            elif self.root.left is None:
                self.root.right.parent = None
                self.root = self.root.right
            else:
                self.max(self.root.left)
                self.root.right.parent = None
                self.root.right = self.root.right.right
                self.root.right.parent = self.root
        else:
            raise ValueError('Element not found')

    def _print_def_(self, node, position_node, current_level, _printy_):
        if current_level == len(_printy_):
            _printy_.append(["_"] * (2 ** current_level))

        node_str = f"[{node.key} {node.value}"
        if node.parent is not None:
            node_str += f" {node.parent.key}]"
        else:
            node_str += "]"

        _printy_[current_level][position_node] = node_str

        if node.left is not None:
            self._print_def_(node.left, 2 * position_node,
                             current_level + 1, _printy_)
        if node.right is not None:
            self._print_def_(node.right, 2 * position_node +
                             1, current_level + 1, _printy_)

    def print_tree(self):
        print_tree = []
        if self.root is None:
            return "_\n"
        self._print_def_(self.root, 0, 0, print_tree)
        result = ""
        for level in print_tree:
            result += ' '.join(level) + "\n"

        return result


splay_tree = SplayTree()

for line in sys.stdin:
    space = []
    for i in range(len(line)):
        if line[i] == ' ':
            space.append(i)
    if line == '\n':
        pass
    elif (re.match(r'add\s[^\s]*\s[^\s]*', line)) and (len(space) == 2):
        try:
            if line[4:space[1]:1].isdigit():
                splay_tree.add(int(line[4:space[1]:1]),
                               line[space[1] + 1:len(line)-1:1])
            elif (line[4] == '-') and (line[5:space[1]:1].isdigit()):
                splay_tree.add((-1)*int(line[5:space[1]:1]),
                               line[space[1] + 1:len(line)-1:1])
            else:
                raise ValueError('Invalid input')
        except ValueError as e:
            print('error')
    elif (re.match(r'set\s[^\s]*\s[^\s]*', line)) and (len(space) == 2):
        try:
            if line[4:space[1]:1].isdigit():
                splay_tree.set(int(line[4:space[1]:1]),
                               line[space[1] + 1:len(line)-1:1])
            elif (line[4] == '-') and (line[5:space[1]:1].isdigit()):
                splay_tree.set(
                    (-1) * int(line[5:space[1]:1]), line[space[1] + 1:len(line) - 1:1])
            else:
                raise ValueError('Invalid input')
        except ValueError as e:
            print('error')
    elif (re.match(r'delete\s[^\s]*', line)):
        try:
            if len(line) > 7:
                if line[7:len(line)-1:1].isdigit():
                    splay_tree.delete(int(line[7:len(line)-1:1]))
                elif (line[7] == '-') and (line[8:len(line)-1:1].isdigit()):
                    splay_tree.delete((-1)*int(line[8:len(line)-1:1]))
                else:
                    raise ValueError('Invalid input')
            else:
                raise ValueError('Invalid input')
        except ValueError as e:
            print('error')
    elif (re.match(r'search\s[^\s]*', line)):
        try:
            if line[7:len(line) - 1:1].isdigit():
                if splay_tree.search(int(line[7:len(line)-1:1])):
                    print('1 ' + splay_tree.root.value)
                else:
                    print('0')
            elif (line[7] == '-') and (line[8:len(line)-1:1].isdigit()):
                if splay_tree.search((-1)*int(line[8:len(line)-1:1])):
                    print('1 ' + splay_tree.root.value)
                else:
                    print('0')
            else:
                raise ValueError('Invalid input')
        except ValueError as e:
            print('error')
    elif line == 'min\n':
        try:
            if splay_tree.min(splay_tree.root):
                print(str(splay_tree.root.key) + ' ' + splay_tree.root.value)
            else:
                raise ValueError('Tree is empty')
        except ValueError as e:
            print('error')
    elif line == 'max\n':
        try:
            if splay_tree.max(splay_tree.root):
                print(str(splay_tree.root.key) + ' ' + splay_tree.root.value)
            else:
                raise ValueError('Tree is empty')
        except ValueError as e:
            print('error')
    elif line == 'print\n':
        try:
            if splay_tree.root is None:
                print('_')
                continue
            result = splay_tree.print_tree()
            print(result, end="")
        except Exception as e:
            print('error')
    else:
        print('error')
