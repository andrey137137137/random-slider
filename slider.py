import random
import tkinter as tk
from tkinter import ttk

import global_vars as gl
from helpers import *


def get_random(diapozon):
    return int(random.random() * diapozon)


def run():
    gl.index = prev_index = 0

    def clock():
        nonlocal prev_index

        # gl.index += 1
        while gl.index == prev_index:
            gl.index = get_random(gl.count)

        prev_index = gl.index

        # if gl.index == count:
        #     gl.index = 0

        label.config(image=gl.images[gl.index])
        label.after(gl.speed.get(), clock)

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

    label = ttk.Label(window, image=gl.images[0])
    label.pack(anchor=tk.NE)

    window.grab_set()  # захватываем пользовательский ввод

    clock()
