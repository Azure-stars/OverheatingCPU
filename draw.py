## 这个文件是用于画图的文件，大家可以复用

import matplotlib.pyplot as plt

xdata = [i for i in range(1, 21)]

temperature_data_sets = [
    [46.16, 47.774, 49.388, 49.388, 49.926, 51.54, 51.54, 52.078, 52.078, 52.078, 52.616, 53.154, 53.154, 53.692, 53.692, 53.692, 53.692, 53.692, 54.23, 54.23],
    [46.698, 48.312, 49.926, 51.54, 52.078, 52.616, 53.692, 53.692, 54.23, 54.768, 54.768, 55.306, 55.306, 55.844, 55.844, 55.844, 55.844, 55.844, 55.844, 55.844],
    [46.698, 49.388, 51.002, 52.078, 53.154, 53.692, 54.23, 54.768, 54.768, 54.768, 55.306, 55.306, 55.844, 55.844, 56.382, 56.382, 56.382, 56.382, 56.382, 56.382],
    [47.774, 50.464, 52.616, 53.154, 53.692, 54.23, 54.768, 54.768, 55.306, 55.306, 55.844, 55.844, 55.844, 55.844, 55.844, 56.382, 55.844, 56.382, 56.382, 56.382],
    [48.312, 51.54, 53.154, 53.692, 54.23, 55.306, 55.844, 55.844, 55.844, 55.844, 56.382, 56.382, 56.382, 56.382, 56.92, 56.92, 56.92, 56.92, 56.92, 56.92]
]

colors = ['blue', 'green', 'red', 'orange', 'purple']
for i, data in enumerate(temperature_data_sets):
    plt.plot(xdata, data, marker='o', linestyle='-', color=colors[i])

plt.xlabel('Generation')
plt.ylabel('Temperature')
plt.title('Relation between temperature and popularation size')

legends = ['size={}'.format(10 * (i + 1)) for i in range(len(temperature_data_sets))]
plt.legend(legends, loc='upper left')
plt.xticks(range(1, 21))
plt.grid(True)
plt.show()
