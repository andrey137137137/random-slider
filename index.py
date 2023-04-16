import time

while True:
    i = 0
    ii = 0
    iii = 0
    time_user = int(input("Введите кол-во секунд: "))
    comment = str(input("Введите комментарий: "))
    for q in range(time_user):
        time.sleep(1)
        i += 1
        print("Прошло секунд:", i)
        if i % 60 == 0:
            ii += 1
            print("Прошло минут:", ii)
        if i % 3600 == 0:
            iii += 1
            print("Прошло часов:", iii)
    print("Время окончено!")
    print("Ваш комментарий:", comment)
