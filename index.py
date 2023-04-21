# # выбранная тема
# selected_theme = tk.StringVar()
# style = ttk.Style()

# # изменение текущей темы
# def change_theme():
#     style.theme_use(selected_theme.get())


# ttk.Label(textvariable=selected_theme, font="Helvetica 13").pack(anchor=tk.NW)

# for theme in style.theme_names():
#     ttk.Radiobutton(
#         text=theme, value=theme, variable=selected_theme, command=change_theme
#     ).pack(anchor=tk.NW)

import os
from os import path as p
import tkinter as tk
from tkinter import ttk
from helpers import *
import global_vars as gl
import slider


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
    # global label_value, gl.cur_dir
    gl.cur_dir = path
    label_value.set(path)


def set_cur_dir(dir):
    # global gl.cur_dir, gl.prev_cur_dir

    path = get_path(gl.cur_dir, dir)
    print(path)

    if not path == "" and not p.isdir(path):
        return False

    gl.prev_cur_dir = gl.cur_dir
    set_label_value(path)
    return True


def set_cur_list():
    # global gl.cur_dir, gl.cur_list, gl.prev_cur_list

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


root = tk.Tk()
root.title("SLIDER")
root.geometry("700x500")

list_var = tk.Variable(value=gl.cur_list)

label_value = tk.StringVar(value=gl.cur_dir)
ttk.Label(textvariable=label_value).pack()

file_listbox = tk.Listbox(listvariable=list_var)
file_listbox.pack()

ttk.Button(text="Перейти в папку", command=select).pack()

gl.monitor_height = root.winfo_screenheight()
gl.monitor_width = root.winfo_screenwidth()

open_button = ttk.Button(text="Создать окно", command=slider.run)
open_button.pack(anchor="center", expand=1)

print("width x height = %d x %d (pixels)" % (gl.monitor_width, gl.monitor_height))

root.mainloop()
