from os import path as p

index = 0

drives = [chr(x) + ":" for x in range(65, 91) if p.exists(chr(x) + ":")]

cur_dir = prev_cur_dir = ""
cur_list = prev_cur_list = drives

slider_dirs = {}
last_dir_id = 0

monitor_height = 0
monitor_width = 0
