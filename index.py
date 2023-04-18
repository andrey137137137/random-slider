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
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image


def dismiss(window):
    window.grab_release()
    window.destroy()


def click():
    def clock():
        global index

        index += 1

        if index == count:
            index = 0

        label.config(image=images[index])
        label.after(1000, clock)

    window = tk.Toplevel()
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


root = tk.Tk()

cur_dir = ""
items = os.listdir(cur_dir)
count = len(items)
index = 0

images = []

for item in items:
    images.append(ImageTk.PhotoImage(Image.open(cur_dir + "/" + item)))

label = ""

open_button = ttk.Button(text="Создать окно", command=click)
open_button.pack(anchor="center", expand=1)

root.mainloop()
