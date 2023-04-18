# import os
# from PIL import ImageTk, Image
# import tkinter as tk
# from tkinter import ttk

# root = tk.Tk()
# root.title("METANIT.COM")
# root.geometry("250x200")


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


# def dismiss(window):
#     window.grab_release()
#     window.destroy()


# def click():
#     window = tk.Toplevel()
#     window.title("Новое окно")
#     window.attributes("-fullscreen", True)
#     # window.attributes("-toolwindow", True)
#     window.protocol(
#         "WM_DELETE_WINDOW", lambda: dismiss(window)
#     )  # перехватываем нажатие на крестик

#     close_button = ttk.Button(
#         window, text="Закрыть окно", command=lambda: dismiss(window)
#     )
#     # close_button.pack(anchor="center", expand=1)
#     close_button.pack()

#     # cur_dir = os.getcwd()
#     cur_dir = ""
#     # img = PhotoImage(file=cur_dir)

#     # label = ttk.Label(window, image=img)
#     # label.pack()
#     # print(label.winfo_parent())

#     canv = tk.Canvas(window, width=2000, height=2000, bg="white")

#     # canv.grid(row=2, column=3)
#     canv.pack()
#     img = ImageTk.PhotoImage(Image.open(cur_dir))  # PIL solution
#     canv.create_image(0, 0, anchor=tk.NW, image=img)

#     window.grab_set()  # захватываем пользовательский ввод


# open_button = ttk.Button(text="Создать окно", command=click)
# open_button.pack(anchor="center", expand=1)

# root.mainloop()

import tkinter as tk
from PIL import ImageTk, Image

root = tk.Tk()

canv = tk.Canvas(root, width=2000, height=2000, bg="white")
# canv.grid(row=2, column=3)
canv.pack()

cur_dir = ""

img = ImageTk.PhotoImage(Image.open(cur_dir))  # PIL solution
canv.create_image(0, 0, anchor=tk.NW, image=img)

root.mainloop()
