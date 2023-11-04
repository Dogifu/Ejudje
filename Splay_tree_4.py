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
                print('error')
                self.splay(root)
                return

        if node.key < parent.key:
            parent.left = node
        else:
            parent.right = node
        node.parent = parent
        self.splay(node)
        return
    

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
            print('error')
            return

        node = self.search(key)
        if node:
            node.value = value
            self.splay(node)
        else:
            print('error')
        return



    def delete(self, key):
        if self.root is None:
            print('error')
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
            print('error')
        return


    def print_tree(self, children: list = None):
        if children is None:    
            if not self.root:
                print('_')
                return
            print(f'[{self.root.key} {self.root.value}]')
            self.print_tree([self.root.left, self.root.right])   
            return

        if not children:
            return

        is_end = True
        for child in children:     
            if type(child) == Node:
                is_end = False
                break
        if is_end:
            return

        new_children = []    
        for child in children[:-1]:
            if type(child) == int:
                print('_ '*child, end='')
                new_children.append(child*2)
            elif not child:
                print('_ ', end='')
                if not new_children:
                    new_children.append(2)
                elif type(new_children[-1]) == int:
                    new_children[-1] += 2
                else:
                    new_children.append(2)
            else:
                print(f'[{child.key} {child.value} {child.parent.key}] ', end='')
                new_children.extend([child.left, child.right])

        if type(children[-1]) == int:
            print('_ ' * (children[-1]-1) + '_', end='')
            if not new_children:
                new_children.append(children[-1] * 2)
            elif type(new_children[-1]) == int:
                new_children[-1] += children[-1] * 2
            else:
                new_children.append(children[-1] * 2)
        elif not children[-1]:
            print('_', end='')
            if not new_children:
                new_children.append(2)
            elif type(new_children[-1]) == int:
                new_children[-1] += 2
            else:
                new_children.append(2)
        else:
            print(f'[{children[-1].key} {children[-1].value} {children[-1].parent.key}]', end='')
            new_children.extend([children[-1].left, children[-1].right])
        print()
        self.print_tree(new_children) 


splay_tree = SplayTree()
for line in sys.stdin:
    space = []
    for i in range(len(line)):
        if line[i] == ' ':
            space.append(i)
    if line == '\n':
        pass
    elif (re.match(r'add\s[^\s]*\s[^\s]*', line)) and (len(space) == 2):
        if line[4:space[1]:1].isdigit():
            splay_tree.add(int(line[4:space[1]:1]), line[space[1] + 1:len(line)-1:1])
        elif (line[4] == '-') and (line[5:space[1]:1].isdigit()):
            splay_tree.add((-1)*int(line[5:space[1]:1]), line[space[1] + 1:len(line)-1:1])
        else:
            print('error')
    elif (re.match(r'set\s[^\s]*\s[^\s]*', line)) and (len(space) == 2):
        if line[4:space[1]:1].isdigit():
            splay_tree.set(int(line[4:space[1]:1]), line[space[1] + 1:len(line)-1:1])
        elif (line[4] == '-') and (line[5:space[1]:1].isdigit()):
            splay_tree.set((-1) * int(line[5:space[1]:1]), line[space[1] + 1:len(line) - 1:1])
        else:
            print('error')
    elif (re.match(r'delete\s[^\s]*', line)):
        if len(line) > 7: 
            if line[7:len(line)-1:1].isdigit():
                splay_tree.delete(int(line[7:len(line)-1:1]))
            elif (line[7] == '-') and (line[8:len(line)-1:1].isdigit()):
                splay_tree.delete((-1)*int(line[8:len(line)-1:1]))
            else:
                print('error')
        else:
            print('error')
    elif (re.match(r'search\s[^\s]*', line)):
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
            print('error')
    elif line == 'min\n':
        if splay_tree.min(splay_tree.root):
            print(str(splay_tree.root.key) + ' ' + splay_tree.root.value)
        else:
            print('error')
    elif line == 'max\n':
        if splay_tree.max(splay_tree.root):
            print(str(splay_tree.root.key) + ' ' + splay_tree.root.value)
        else:
            print('error')
    elif line == 'print\n':
        if splay_tree.root is None:
            print('_')
            continue
        splay_tree.print_tree()
    else:
        print('error')