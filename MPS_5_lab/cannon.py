import random
import math as m
import numpy as np
import matplotlib.pyplot as plt

# Настройки математической модели:
order = 8  # количество знаком после запятой во всех расчётах
step = 10  # шаг для построения гистограмм (ширина одного столбика)
step_shot = 30  # шаг между кол-м выстрелов
many_shot = 50000  # большое количество выстрелов для графика норм. распред.
# эталонный генератор: round(random.uniform(0, 1), order)

con = m.pi/180  # константа для перевода градусы в радианы

# Настройки параметров пушки:
L = 1000  # расстояние от начала координат до центра мишени (м)
d = 10  # диаметр мишени (м)
g = 9.8175  # ускорение свободного падения (м^2/с)
angle = 22.0  # угол стрельбы (градусы) - мат. ожидание
angle_spread = 2.0  # разброс угла стрельбы (градусы) - сигма
speed = m.sqrt((L*g)/m.sin(2*angle*con))  # скорость выстрела (м/с)
speed_spread = 2.0  # разброс скорости (м/с)


def ran_var_normal():
    # СВ с нормальным распределением. Мат. ожид = 0, сигма = 1
    # генерирует числа из отрезка [-6:6]
    summa = 0
    for _ in range(12):
        summa += round(random.uniform(0, 1), order)
    return summa - 6


def shoot_once():
    # рассчитывает точку, в которое упадёт ядро, по формуле
    sup_1 = speed + speed_spread * ran_var_normal()  # погрешности СВ
    sup_2 = angle + angle_spread * ran_var_normal()
    return round((pow(sup_1, 2)*m.sin(2*sup_2*con))/g, order)


def calc_multi_shot(quan):
    # выстрелить quan раз и посчитать для всех мат. ожди-е и дисп-ю
    shot_list = np.zeros(quan)
    for x in range(quan):
        shot_list[x] = shoot_once()
    mat_expect = np.sum(shot_list) / quan
    disp = np.sum((shot_list - mat_expect) ** 2) / (quan - 1)
    # Мат. ожид. вычитается из всех элементов массива
    return mat_expect, disp


if __name__ == "__main__":
    # Построение графиков мат. ожидания и дисперсии
    quan_shot = range(100, 4000, step_shot)
    # начиная с 100, потом 100 + step_shot до 4000
    mat_expects = []  # массив с математическими ожиданиями
    dispersions = []  # массив с дисперсиями

    for i in quan_shot:
        m_exp, disp = calc_multi_shot(i)
        mat_expects.append(m_exp)
        dispersions.append(disp)

    # Построение гистограммы выстрелов
    left = 500
    right = 1500
    arguments = np.arange(left, right, step)  # аргументы для гистограммы
    counters = np.zeros(int((right - left) / step))  # значения гистограммы
    shot_array = np.zeros(many_shot)  # массив всех выстрелов
    summa = 0
    hits = 0  # количество попаданий в мишень
    for i in range(many_shot):
        shot_array[i] = shoot_once()
        index = (shot_array[i] - left) // step
        counters[int(index)] += 1
        summa += shot_array[i]
        if (L - d/2) < shot_array[i] and shot_array[i] < (L + d/2):
            hits += 1

    counters /= (many_shot/100)

    mat_expect = summa/many_shot  # значение мат. ожидание
    dispersion = 0  # значение дисперсии
    for i in range(many_shot):
        dispersion += (shot_array[i] - mat_expect) ** 2
    dispersion /= (many_shot - 1)
    print(f'Математическое ожидание: {mat_expect}\nДисперсия: {dispersion}\nВероятность попасть в мишень: {(hits/many_shot)*100} %')

    # отображение графиков мат. ожидания и дисперсии
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(quan_shot, mat_expects)
    plt.axhline(y=mat_expect, color='green', linestyle='-.', linewidth=2, label='Ожидаемое')
    plt.xlabel("Количество выстрелов")
    plt.ylabel("Математическое ожидание")
    plt.title("Математическое ожидание от количества выстрелов")

    plt.subplot(1, 2, 2)
    plt.plot(quan_shot, dispersions)
    plt.axhline(y=dispersion, color='green', linestyle='-.', linewidth=2, label='Ожидаемое')
    plt.xlabel("Количество выстрелов")
    plt.ylabel("Дисперсия")
    plt.title("Дисперсия от количества выстрелов")
    plt.figure()

    # Отображение гистограммы
    plt.bar(arguments, counters, width=step, align='edge', alpha=0.7, color='blue')
    border = 3 * m.sqrt(dispersion)  # 3 * сигма
    temp_1 = mat_expect + border
    temp_2 = mat_expect - border
    plt.axvline(x=mat_expect, color='red', linestyle='-.', linewidth=2, label='ожидаемое')
    plt.plot([temp_1, temp_1], [0, 1], color='green', linestyle='-.', linewidth=2, label='Линия')
    plt.plot([temp_2, temp_2], [0, 1], color='green', linestyle='-.', linewidth=2, label='Линия')
    plt.title('Гистограмма распределения выстрелов')  # Добавление заголовка и меток осей
    plt.xlabel('Отрезки')
    plt.ylabel('Число попаданий в отрезов (%)')

    plt.tight_layout()
    plt.show()
