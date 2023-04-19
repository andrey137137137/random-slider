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
from tkinter import messagebox as mb
from PIL import ImageTk, Image, UnidentifiedImageError


def dismiss(window):
    window.grab_release()
    window.destroy()


def getSize(value, scale):
    return int(value * scale)


def click():
    if cur_dir == "":
        show_message("Выберите директорию")
        return

    temp_items = os.listdir(cur_dir)
    items = []

    for item in temp_items:
        if p.isfile(get_abspath(cur_dir, item)):
            items.append(item)

    count = len(items)
    print(items)

    if count:
        images = []

        for item in items:
            try:
                img = Image.open(cur_dir + "/" + item)
                h, w = img.size
                scale = monitor_height / max(h, w)
                images.append(
                    ImageTk.PhotoImage(
                        img.resize(
                            (getSize(h, scale), getSize(w, scale)), Image.LANCZOS
                        )
                    )
                )
            except UnidentifiedImageError:
                continue

        count = len(images)

    if count == 0:
        show_message("В этой папке нет изображений")
        return

    global index
    index = 0

    def clock():
        global index

        index += 1

        if index == count:
            index = 0

        label.config(image=images[index])
        label.after(500, clock)

    window = tk.Toplevel(bg="black")
    window.title("Новое окно")
    window.attributes("-fullscreen", True)
    # window.attributes("-toolwindow", True)

    window.protocol(
        "WM_DELETE_WINDOW", lambda: dismiss(window)
    )  # перехватываем нажатие на крестик

    close_button = ttk.Button(
        window, text="Закрыть окно", command=lambda: dismiss(window)
    )
    # close_button.pack(anchor="center", expand=1)
    close_button.pack()

    label = ttk.Label(window, image=images[0])
    label.pack()

    window.grab_set()  # захватываем пользовательский ввод

    clock()


def show_message(str, type="w"):
    if type == "i":
        return mb.showinfo("Сообщение", str)
    if type == "w":
        return mb.showwarning("Предупреждение", str)
    mb.showerror("Ошибка", str)


def get_file_selected():
    selection = file_listbox.curselection()

    if len(selection) == 0:
        show_message("Выберите директорию")
        return ""

    return file_listbox.get(selection[0])


def get_abspath(dir, name=""):
    return p.abspath(dir + "/" + name)


def get_path(root, dir):
    if dir in drives:
        print(dir)
        return get_abspath(dir)

    if len(root) == 3 and dir == "..":
        return ""

    path = get_abspath(root, dir)

    if p.isfile(path):
        print(p.getsize(path))

    return path


def set_label_value(path):
    global label_value, cur_dir
    cur_dir = path
    label_value.set(path)


def set_cur_dir(dir):
    global cur_dir, prev_cur_dir

    path = get_path(cur_dir, dir)
    print(path)

    if not path == "" and not p.isdir(path):
        return False

    prev_cur_dir = cur_dir
    set_label_value(path)
    return True


def set_cur_list():
    global cur_dir, cur_list, prev_cur_list

    if cur_dir == "":
        cur_list = drives
    else:
        try:
            prev_cur_list = cur_list
            cur_list = [".."] + os.listdir(cur_dir)
        except:
            show_message("Невозможно открыть директорию: " + cur_dir, "e")
            set_label_value(prev_cur_dir)
            cur_list = prev_cur_list


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

    print(cur_dir)

    set_cur_list()
    file_listbox.delete(0, tk.END)

    i = 0
    for item in cur_list:
        if cur_dir == "" or p.isdir(get_abspath(cur_dir, item)):
            i = add(i, item)

    print(cur_list)


root = tk.Tk()
root.title("SLIDER")
root.geometry("700x500")

index = 0

drives = [chr(x) + ":" for x in range(65, 91) if p.exists(chr(x) + ":")]

cur_dir = prev_cur_dir = ""
cur_list = prev_cur_list = drives
list_var = tk.Variable(value=cur_list)

label_value = tk.StringVar(value=cur_dir)
ttk.Label(textvariable=label_value).pack()

file_listbox = tk.Listbox(listvariable=list_var)
file_listbox.pack()

ttk.Button(text="Перейти в папку", command=select).pack()

monitor_height = root.winfo_screenheight()
monitor_width = root.winfo_screenwidth()

open_button = ttk.Button(text="Создать окно", command=click)
open_button.pack(anchor="center", expand=1)

print("width x height = %d x %d (pixels)" % (monitor_width, monitor_height))

root.mainloop()
