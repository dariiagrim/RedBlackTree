import random


class Node:
    def __init__(self, value, parent, data1, color="R"):
        self.value = value
        self.data = data1
        self.parent = parent
        self.left = None
        self.right = None
        self.color = color

    def get_uncle(self):
        if self.parent is not None and self.parent.parent is not None:
            if self.parent == self.parent.parent.left:
                return self.parent.parent.right
            else:
                return self.parent.parent.left
        return None

    def get_sibling(self):
        if self.parent is not None:
            if self.parent.right == self:
                return self.parent.left
            else:
                return self.parent.right
        return None

    def __repr__(self):
        parent = None
        if self.parent is not None:
            parent = self.parent.value
        string = f"{self.value}<-({parent})({self.color}){self.data}\n"
        if self.left is not None:
            string += f"L:{self.left}"
        if self.right is not None:
            string += f"R:{self.right}"
        return string


class RBT:
    root = None

    def __insert(self, value, node, data1):
        if node is None:
            self.root = Node(value, None, data1)
            return
        if node.value > value:
            if node.left is None:
                node.left = Node(value, node, data1)
                self.fix_violations(node.left)
            else:
                self.__insert(value, node.left, data1)
        else:
            if node.right is None:
                node.right = Node(value, node, data1)
                self.fix_violations(node.right)
            else:
                self.__insert(value, node.right, data1)

    def insert(self, value, data1):
        self.__insert(value, self.root, data1)

    def fix_violations(self, node: None):
        while node.parent is not None and node.parent.color != "B" and node.parent.parent is not None and node.color == "R":
            g = node.parent.parent
            p = node.parent
            u = node.get_uncle()
            if u is not None and u.color == "R":
                self.recolor(p)
                self.recolor(g)
                self.recolor(u)
                if g != self.root:
                    node = g
            else:
                if node.value < p.value < g.value:
                    self.right_rotation(g)
                    self.recolor(g)
                    self.recolor(p)
                elif node.value >= p.value < g.value:
                    self.left_rotation(p)
                    self.right_rotation(g)
                    self.recolor(g)
                    self.recolor(node)
                elif node.value >= p.value >= g.value:
                    self.left_rotation(g)
                    self.recolor(g)
                    self.recolor(p)
                else:
                    self.right_rotation(p)
                    self.left_rotation(g)
                    self.recolor(g)
                    self.recolor(node)

    def recolor(self, node: Node):
        if node is None:
            return
        if node.color == "B" and node != self.root:
            node.color = "R"
        else:
            node.color = "B"

    def right_rotation(self, node: Node):
        temp = node.left
        node.left = temp.right
        if node.left is not None:
            node.left.parent = node
        if node.parent is not None:
            if node.parent.right == node:
                node.parent.right = temp
            else:
                node.parent.left = temp
            temp.parent = node.parent
        else:
            self.root = temp
            temp.parent = None
        temp.right = node
        node.parent = temp

    def left_rotation(self, node: Node):
        temp = node.right
        node.right = temp.left
        if node.right is not None:
            node.right.parent = node
        if node.parent is not None:
            if node.parent.right == node:
                node.parent.right = temp
            else:
                node.parent.left = temp
            temp.parent = node.parent
        else:
            self.root = temp
            temp.parent = None
        temp.left = node
        node.parent = temp

    def __search(self, value, node):
        if node is None:
            return
        if node.value == value:
            return node
        if node.value > value:
            return self.__search(value, node.left)
        else:
            return self.__search(value, node.right)

    def search(self, value):
        return self.__search(value, self.root)

    def __delete(self, node):
        if node is None:
            return
        if node.left is None and node.right is None:
            self.fix_delete(node)
            return

        if node.right is not None:
            minn = self.get_min_node(node.right)
            temp = node.value
            node.value = minn.value
            minn.value = temp
            self.__delete(minn)
        else:
            maxn = self.get_max_node(node.left)
            temp = node.value
            node.value = maxn.value
            maxn.value = temp
            self.__delete(maxn)

    def delete(self, value):
        node = self.search(value)
        self.__delete(node)

    def fix_delete(self, node):
        count = 0
        while True:
            if node.color == "R":
                if node == node.parent.left:
                    node.parent.left = None
                else:
                    node.parent.right = None
                return
            else:
                p = node.parent
                s = node.get_sibling()
                if node == self.root:
                    return
                if s is None or s.color == "B":
                    if self.delete_check_bbb(s):
                        if p.color == "B":
                            self.recolor(s)
                            if count == 0:
                                if node == node.parent.left:
                                    count += 1
                                    node.parent.left = None
                                else:
                                    count += 1
                                    node.parent.right = None
                            node = p
                        else:
                            self.recolor(p)
                            self.recolor(s)
                            break
                    elif node == node.parent.left:
                        if (s.right is None or s.right.color == "B") and s.left.color == "R":
                            self.recolor(s)
                            self.recolor(s.left)
                            self.right_rotation(s)
                        else:
                            if s.parent.color != s.color:
                                temp = s.color
                                s.color = s.parent.color
                                s.parent.color = temp
                            s.right.color = "B"
                            self.left_rotation(p)
                            break
                    else:
                        if (s.left is None or s.left.color == "B") and s.right.color == "R":
                            self.recolor(s)
                            self.recolor(s.right)
                            self.left_rotation(s)
                        else:
                            if s.parent.color != s.color:
                                temp = s.color
                                s.color = s.parent.color
                                s.parent.color = temp
                            s.left.color = "B"
                            self.right_rotation(p)
                            break
                else:
                    # self.recolor(p)
                    # self.recolor(s)
                    if s.parent.color != s.color:
                        temp = s.color
                        s.color = s.parent.color
                        s.parent.color = temp
                    if p.left == node:
                        self.left_rotation(p)
                    else:
                        self.right_rotation(p)
        if node == node.parent.left:
            node.parent.left = None
        else:
            node.parent.right = None
        return

    @staticmethod
    def delete_check_bbb(s):
        if s is None:
            return True
        if s.left is None and s.right is None:
            return True
        if s.right is None and s.left is not None and s.left.color == "B":
            return True
        if s.left is None and s.right is not None and s.right.color == "B":
            return True
        if s.left is not None and s.right is not None and s.left.color == "B" and s.right.color == "B":
            return True
        return False

    @staticmethod
    def get_min_node(node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    @staticmethod
    def get_max_node(node):
        current = node
        while current.right is not None:
            current = current.right
        return current

    def search_data(self, value):
        node = self.search(value)
        if node is not None:
            return node.data
        return None

    def change_data(self, value):
        node = self.search(value)
        if node is not None:
            node.data = input()
            return
        return "Key doesn't exist"

    def __print(self, node):
        if node is None:
            return
        print(node.value, node.color)
        self.__print(node.left)
        self.__print(node.right)

    def print(self):
        self.__print(self.root)


tree = RBT()
a = []
# for _ in range(10000):
#     num = random.randint(1, 10000)
#     a.append(num)
#     tree.insert(num)
# print(tree.root)
# for _ in range(5000):
#     tree.delete(random.randint(1, 10000))

with open("data.txt", "r") as f:
    data_list = f.readlines()


set_keys = set()
for _ in range(15):
    num = random.randint(1, 15)
    if num not in set_keys:
        set_keys.add(num)
        num2 = random.randint(0, 9999)
        data = data_list[num2]
        tree.insert(num, data)

print(tree.search_data(10))
print(tree.root)
print(tree.search_data(30))
tree.insert(30, data_list[random.randint(0, 9999)])
print(tree.root)
print(tree.search(30))
tree.change_data(30)
print(tree.root)











