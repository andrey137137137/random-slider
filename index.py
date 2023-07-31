# # выбранная тема
# selected_theme = tk.StringVar()
# style = ttk.Style()

# # изменение текущей темы
# def change_theme():
#     style.theme_use(selected_theme.get())


# ttk.Label(textvariable=selected_theme, font="Helvetica 13").grid(anchor=tk.NW)

# for theme in style.theme_names():
#     ttk.Radiobutton(
#         text=theme, value=theme, variable=selected_theme, command=change_theme
#     ).grid(anchor=tk.NW)

import os
import tkinter as tk
from os import path as p
from tkinter import ttk

from PIL import Image, ImageTk, UnidentifiedImageError

import global_vars as gl
import slider
from helpers import *


def get_file_selected():
    selection = file_listbox.curselection()

    if len(selection) == 0:
        show_message("Выберите директорию")
        return ""

    return file_listbox.get(selection[0])


def get_path(root, dir):
    if dir in gl.drives:
        print(dir)
        return get_abspath(dir)

    if len(root) == 3 and dir == "..":
        return ""

    path = get_abspath(root, dir)

    if p.isfile(path):
        print(p.getsize(path))

    return path


def set_label_value(path):
    gl.cur_dir = path
    label_value.set(path)


def set_cur_dir(dir):
    path = get_path(gl.cur_dir, dir)
    print(path)

    if not path == "" and not p.isdir(path):
        return False

    gl.prev_cur_dir = gl.cur_dir
    set_label_value(path)
    return True


def set_cur_list():
    if gl.cur_dir == "":
        gl.cur_list = gl.drives
    else:
        try:
            gl.prev_cur_list = gl.cur_list
            gl.cur_list = [".."] + os.listdir(gl.cur_dir)
        except:
            show_message("Невозможно открыть директорию: " + gl.cur_dir, "e")
            set_label_value(gl.prev_cur_dir)
            gl.cur_list = gl.prev_cur_list


def add(index, name):
    index += 1
    file_listbox.insert(index, name)
    return index


def select():
    selected = get_file_selected()
    print(selected)

    if not selected:
        return

    if not set_cur_dir(selected):
        return

    print(gl.cur_dir)

    set_cur_list()
    file_listbox.delete(0, tk.END)

    i = 0
    for item in gl.cur_list:
        if gl.cur_dir == "" or p.isdir(get_abspath(gl.cur_dir, item)):
            i = add(i, item)

    print(gl.cur_list)


def add_to_tree(index, text):
    if index == 0:
        id = ""
        iid = gl.last_dir_id
    else:
        id = gl.last_dir_id
        temp_index = index
        if index > 1:
            id = str(id) + "." + str(index - 1)
        iid = str(gl.last_dir_id) + "." + str(temp_index)
    tree.insert(parent=id, index=tk.END, iid=iid, text=text, open=True)


def clean_tree():
    for item in tree.get_children(""):
        tree.delete(item)


def build_tree(path):
    parts = path.split("\\")
    print(len(parts))

    # clean_tree()
    add_to_tree(0, parts[0])

    i = 1
    while i < len(parts):
        add_to_tree(i, parts[i])
        i += 1


def add_cur_path():
    # gl.slider_dirs.append(gl.cur_dir)
    gl.slider_dirs[gl.last_dir_id] = gl.cur_dir
    build_tree(gl.cur_dir)
    gl.last_dir_id += 1


def clean_slider_dirs():
    global pathes

    # gl.slider_dirs = []
    gl.slider_dirs.clear()
    clean_tree()
    gl.last_dir_id = 0
    gl.images = []
    gl.count = 0
    pathes = {}


def convertSpeed(*args):
    intSpeed.set(gl.speed.get())


def run():
    if gl.count == 0:
        if gl.cur_dir == "":
            show_message("Выберите директорию")
            return

        items = []

        for id in gl.slider_dirs:
            pathes[id] = 0
            dir = gl.slider_dirs[id]
            file_list = os.listdir(dir)
            for item in file_list:
                path = get_abspath(dir, item)
                if p.isfile(path):
                    items.append(path)
                    pathes[id] = pathes[id] + 1

        count = len(items)
        print(items)
        print(pathes)

        if count:
            gl.images = []

            for item in items:
                try:
                    # img = Image.open(gl.cur_dir + "/" + item)
                    img = Image.open(item)
                    h, w = img.size
                    scale = gl.monitor_height / max(h, w)
                    gl.images.append(
                        ImageTk.PhotoImage(
                            img.resize(
                                (getSize(h, scale), getSize(w, scale)), Image.LANCZOS
                            )
                        )
                    )
                except UnidentifiedImageError:
                    continue

            gl.count = len(gl.images)

        if gl.count == 0:
            show_message("В этой папке нет изображений")
            return

    slider.run()


pathes = {}

root = tk.Tk()
root.title("SLIDER")
root.geometry("700x800")

gl.monitor_height = root.winfo_screenheight()
gl.monitor_width = root.winfo_screenwidth()

print("width x height = %d x %d (pixels)" % (gl.monitor_width, gl.monitor_height))

# ttk.Style().configure(
#     ".", font="helvetica 13", foreground="#004D40", padding=8, background="#B2DFDB"
# )

row = 0
column = 0
tree = ttk.Treeview()
tree.grid(row=row, column=column, sticky=tk.NSEW)
# tree.heading("#0", text="Отделы", anchor=NW)

# tree.insert("", tk.END, iid=1, text="Административный отдел", open=True)
# tree.insert("", tk.END, iid=2, text="IT-отдел")
# tree.insert("", tk.END, iid=3, text="Отдел продаж")

# tree.insert(1, index=tk.END, text="Tom")
# tree.insert(2, index=tk.END, text="Bob")
# tree.insert(2, index=tk.END, text="Sam")

row = 2
ttk.Button(text="Удалить все пути", command=clean_slider_dirs).grid(
    row=row, column=column, sticky=tk.NSEW
)


row = 0
column = 1
label_value = tk.StringVar(value=gl.cur_dir)
ttk.Label(textvariable=label_value).grid(row=row, column=column)

row = 1
list_var = tk.Variable(value=gl.cur_list)
file_listbox = tk.Listbox(listvariable=list_var)
file_listbox.grid(row=row, column=column)

row = 2
ttk.Button(text="Перейти в папку", command=select).grid(row=row, column=column)


row = 0
column = 2
start = 1000
gl.speed = tk.IntVar(value=start)
gl.speed.trace_add("write", convertSpeed)
intSpeed = tk.IntVar()

row = 1
ttk.Label(text=str(start), textvariable=intSpeed).grid(row=row, column=column)

row = 2
horizontalScale = ttk.Scale(
    orient=tk.HORIZONTAL, length=200, from_=100.0, to=2000.0, variable=gl.speed
).grid(row=row, column=column)

row = 3
ttk.Button(text="Добавить путь", command=add_cur_path).grid(row=row, column=column)

row = 4
ttk.Button(text="Запустить слайдер", command=run).grid(row=row, column=column)

# canvas = tk.Canvas(
#     window, bg="white", width=gl.monitor_width, height=gl.monitor_height
# )
# canvas.pack(anchor=tk.CENTER, expand=1)
# canvas.create_image(0, 0, anchor=tk.NW, image=images[0])

root.mainloop()
