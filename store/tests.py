import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Заданные параметры задачи
L = 10.0  # Длина стержня
T_center = 50.0  # Начальная температура в центре стержня (градусов Цельсия)
T_initial = 0.0  # Начальная температура на остальных частях стержня (градусов Цельсия)
alpha = 0.01  # Коэффициент температуропроводности
dx = 1.0  # Шаг по пространству
dt = 0.5  # Увеличенный шаг по времени для ускорения
time_steps = 5000  # Максимальное количество временных шагов
tolerance = 0.1  # Порог равномерного распределения температуры
positions = np.arange(0, L + dx, dx)

# Количество ячеек вдоль стержня
N = int(L / dx) + 1

# Условие устойчивости для явной схемы
r = alpha * dt / (dx ** 2)
if r >= 0.5:
    raise ValueError("Схема неустойчива: уменьшите dt или увеличьте dx")

# Инициализация массива температур
T = np.full(N, T_initial)
T[N // 2] = T_center  # Начальная температура в центре

# Массив для записи результатов для каждого временного шага до полной сходимости
uniform_results_fast = []

# Численное решение методом конечных разностей с ускоренным шагом
for step in range(time_steps):
    T_new = T.copy()
    for i in range(1, N - 1):
        T_new[i] = T[i] + r * (T[i + 1] - 2 * T[i] + T[i - 1])

    # Применение граничных условий (теплоизоляция на концах)
    T_new[0] = T_new[1]
    T_new[-1] = T_new[-2]

    # Сохранение текущего состояния температуры
    uniform_results_fast.append(T_new.copy())
    T = T_new

    # Проверка равномерности распределения температуры
    if np.max(T) - np.min(T) < tolerance:
        break

# Создание DataFrame для сохранения данных
uniform_results_fast_df = pd.DataFrame(uniform_results_fast, columns=[f"Position {i}" for i in range(N)])
uniform_results_fast_df.index.name = "Time Step"

# Сохранение данных в CSV для последующего анализа, если потребуется
uniform_results_fast_df.to_csv("temperature_distribution.csv")

# Подготовка фигуры для анимации
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, L)
ax.set_ylim(0, T_center)
ax.set_xlabel("Position along the rod")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Cooling Process of the Heated Rod Over Time")

# Линия для обновления в анимации
line, = ax.plot([], [], lw=2)


# Функция инициализации для анимации
def init():
    line.set_data([], [])
    return line,


# Функция обновления кадров анимации
def animate(i):
    x = positions
    y = uniform_results_fast[i]
    line.set_data(x, y)
    return line,


# Создание анимации
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(uniform_results_fast), interval=50, blit=True)

# Сохранение анимации как GIF
ani.save("rod_cooling_animation.gif", writer='pillow', fps=20)

plt.show()

