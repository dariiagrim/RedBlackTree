class Node:
    def __init__(self, value, parent, color="R"):
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None
        self.color = color

    def get_uncle(self):
        if self.parent is not None and self.parent.parent is not None:
            if self.parent.value < self.parent.parent.value:
                return self.parent.parent.right
            else:
                return self.parent.parent.left
        return None

    def get_sibling(self):
        if self.parent is not None:
            if self.parent.value > self.value:
                return self.parent.right
            else:
                return self.parent.left
        return None

    def __repr__(self):
        parent = None
        if self.parent is not None:
            parent = self.parent.value
        string = f"{self.value}<-({parent})({self.color}) \n"
        if self.left is not None:
            string += f"L:{self.left}"
        if self.right is not None:
            string += f"R:{self.right}"
        return string


class RBT:
    root = None

    def __init__(self):
        self.width = 20
        self.height = 10
        self.grid = [["  " for _ in range(self.width)] for _ in range(self.height)]

    def __insert(self, value, node):
        if node is None:
            self.root = Node(value, None, "B")
            return
        if node.value > value:
            if node.left is None:
                node.left = Node(value, node)
                self.fix_violations(node.left)
            else:
                self.__insert(value, node.left)
        else:
            if node.right is None:
                node.right = Node(value, node)
                self.fix_violations(node.right)
            else:
                self.__insert(value, node.right)

    def insert(self, value):
        self.__insert(value, self.root)

    def fix_violations(self, node: None):
        while node.parent.color != "B" and node.parent.parent is not None and node.color == "R":
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
                    break
                if s is None or s.color == "B":
                    if s.left.color == "B" and s.right.color == "B":
                        if p.color == "B":
                            self.recolor(s)
                            node = node.parent
                        else:
                            self.recolor(p)
                            self.recolor(s)
                    elif node == node.parent.left:
                        if s.left.color == "R" and s.right.color == "B":
                            self.recolor(s)
                            self.recolor(s.left)
                            self.right_rotation(node)
                        else:
                            if s.parent.color != s.color:
                                temp = s.color
                                s.color = s.parent.color
                                s.parent.color = temp
                                self.left_rotation(p)
                                s.right.color = "B"
                    else:
                        if s.right.color == "R" and s.left.color == "B":
                            self.recolor(s)
                            self.recolor(s.right)
                            self.left_rotation(node)
                        else:
                            if s.parent.color != s.color:
                                temp = s.color
                                s.color = s.parent.color
                                s.parent.color = temp
                                self.right_rotation(p)
                                s.left.color = "B"
                else:
                    self.recolor(p)
                    self.recolor(s)
                    if p.left == node:
                        self.left_rotation(p)
                    else:
                        self.right_rotation(p)
            if node == node.parent.left:
                node.parent.left = None
            else:
                node.parent.right = None
            return

    def get_position_in_tree(self, node):
        x, y = (0, 0)
        if node == self.root:
            x, y = (self.width/2, 0)
        else:
            if node == node.parent.left:
                x, y = (self.get_position_in_tree(node.parent)[0]-2, self.get_position_in_tree(node.parent)[1]+1)
            else:
                x, y = (self.get_position_in_tree(node.parent)[0] + 2, self.get_position_in_tree(node.parent)[1] + 1)
        return int(x), int(y)

    def print_grid(self):
        for dot in self.grid:
            print(*dot)
        self.traversal(self.root)

        for dot in self.grid:
            print(*dot)

    def traversal(self, node):
        if node is None:
            return
        x, y = self.get_position_in_tree(node)
        self.grid[y][x] = node.value
        self.traversal(node.left)
        self.traversal(node.right)








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




    def recolor(self, node: Node):
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

    def __print(self, node):
        if node is None:
            return
        print(node.value, node.color)
        self.__print(node.left)
        self.__print(node.right)

    def print(self):
        self.__print(self.root)




tree = RBT()
a = [5, 6, 8, 4, 3, 9, 15]
for i in a:
    tree.insert(i)
print(tree.root)
tree.print_grid()





