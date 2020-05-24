from tkinter import *
from tkinter.font import Font
from main import *


tree = RBT()


def clear_tree(*args):
    global tree
    tree = RBT()
    tree_list.delete(0, END)
    change_list()


def fill_randomly(*args):
    clear_tree()
    with open("data.txt", "r") as f:
        data_list = f.readlines()

    set_keys = set()
    for _ in range(20):
        num = random.randint(1, 100)
        if num not in set_keys:
            set_keys.add(num)
            num2 = random.randint(0, 9999)
            data = data_list[num2]
            tree.insert(num, data)

    change_list()


def change_list(*args):
    b = []
    global tree
    Node.node_traversal(tree.root, b)
    for node in b:
        tree_list.insert(END, node.rstrip())


root = Tk()

root['background'] = '#C98ED3'

root.title("Red-Black Tree")
root.geometry("900x700")
root.resizable(width=False, height=False)

tree_list = Listbox(root, height=20, width=30, font=Font(size=18))
tree_list.place(x=10, y=50)
myFont = Font(weight="bold")
fill_but = Button(root, text="Fill with random data", bg='#FCA8F4', command=fill_randomly, height=2, width=20)
fill_but['font'] = myFont
fill_but.place(x=575, y=90)

clear_but = Button(root, text="Clear", bg='#FCA8F4', command=clear_tree, height=2, width=5)
clear_but['font'] = myFont
clear_but.place(x=655, y=190)

lk = Label(root, text="Key: ", bg='#C98ED3',)
lk['font'] = myFont
lk.place(x=560, y=300)
key = IntVar(root)
Entry(root, textvariable=key).place(x=650, y=300)

lv = Label(root, text="Value: ", bg='#C98ED3')
lv['font'] = myFont
lv.place(x=560, y=330)
value = StringVar(root)
Entry(root, textvariable=value).place(x=650, y=330)


def insert(*args):
    k = key.get()
    v = value.get()
    global tree
    tree.insert(k, v)
    tree_list.delete(0, END)
    change_list()

def find(*args):
    k = key.get()
    global tree
    v = tree.search_data(k)
    if v is not None:
        value.set(v.rstrip())
    else:
        value.set("None")

def update(*args):
    k = key.get()
    v = value.get()
    global tree
    f = tree.change_data(k, v)
    if f:
        tree_list.delete(0, END)
        change_list()
    else:
        label["text"] = f"Key {k} does not exist"


def delete(*args):
    k = key.get()
    global tree
    tree.delete(k)
    tree_list.delete(0, END)
    change_list()


label = Label(root, text="")
label.place(x=600, y=600)
insert_but = Button(root, text="Insert", bg='#FCA8F4', command=insert, height=3, width=4)
insert_but['font'] = myFont
insert_but.place(x=630, y=410)

find_but = Button(root, text="Find", bg='#FCA8F4', command=find, height=3, width=4)
find_but['font'] = myFont
find_but.place(x=700, y=410)
update_but = Button(root, text="Update", bg='#FCA8F4', command=update, height=3, width=4)
update_but['font'] = myFont
update_but.place(x=700, y=480)

delete_but = Button(root, text="Delete", bg='#FCA8F4', command=delete, height=3, width=4)
delete_but['font'] = myFont
delete_but.place(x=630, y=480)


root.mainloop()
