import matplotlib.pyplot as plt

fig, ax = plt.subplots()

x1 = (20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000)
y1 = (0, 0, 5, 10, 20, 30, 25, 25, 7)
x2 = (80000, 90000, 100000, 110000, 120000, 130000, 140000, 150000, 160000)
y2 = (5, 5, 10, 15, 20, 30, 20, 25, 5)
x3 = (150000, 160000, 170000, 180000, 190000, 200000, 210000, 220000, 230000)
y3 = (10, 10, 5, 15, 15, 20, 20, 10, 15)

ax.plot(x1, y1, label='Junior')
ax.plot(x2, y2, label="Middle")
ax.plot(x3, y3, label="Senior")

ax.legend()

ax.set_ylabel("Количество вакансий")
ax.set_xlabel("Зарплата")
ax.set(title='График распределения вакансий по ЗП')
ax.grid()

plt.show()