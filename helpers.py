from os import path as p
from tkinter import messagebox as mb


def dismiss(window):
    window.grab_release()
    window.destroy()


def getSize(value, scale):
    return int(value * scale)


def get_abspath(dir, name=""):
    return p.abspath(dir + "/" + name)


def show_message(str, type="w"):
    if type == "i":
        return mb.showinfo("Сообщение", str)
    if type == "w":
        return mb.showwarning("Предупреждение", str)
    mb.showerror("Ошибка", str)
