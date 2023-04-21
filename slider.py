from PIL import ImageTk, Image, UnidentifiedImageError
import os
from os import path as p
from helpers import *
import global_vars as gl
import tkinter as tk
from tkinter import ttk


def run():
    if gl.cur_dir == "":
        show_message("Выберите директорию")
        return

    temp_items = os.listdir(gl.cur_dir)
    items = []

    for item in temp_items:
        if p.isfile(get_abspath(gl.cur_dir, item)):
            items.append(item)

    count = len(items)
    print(items)

    if count:
        images = []

        for item in items:
            try:
                img = Image.open(gl.cur_dir + "/" + item)
                h, w = img.size
                scale = gl.monitor_height / max(h, w)
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

    # global gl.index
    gl.index = 0

    def clock():
        # global gl.index

        gl.index += 1

        if gl.index == count:
            gl.index = 0

        label.config(image=images[gl.index])
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
