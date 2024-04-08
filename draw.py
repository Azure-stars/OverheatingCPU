## 这个文件是用于画图的文件，大家可以复用

import matplotlib.pyplot as plt

xdata = list(range(1, 21))

temperature_data_sets = [
    [50.464, 53.692, 55.306, 56.382, 56.92, 57.996, 57.996, 58.534, 58.534, 59.072, 59.072, 59.61, 60.148, 60.148, 60.148, 59.61, 59.61, 60.148, 59.61, 60.148],
    [50.464, 54.23, 56.382, 56.92, 57.458, 57.996, 58.534, 59.072, 59.072, 59.61, 60.148, 60.148, 60.148, 60.148, 60.148, 60.148, 60.148, 60.148, 60.148, 60.148]
]

colors = ['blue', 'green', 'red', 'orange', 'purple']
for i, data in enumerate(temperature_data_sets):
    plt.plot(xdata, data, marker='o', linestyle='-', color=colors[i])

plt.xlabel('Generation')
plt.ylabel('Temperature')
plt.title('Relation between temperature and generations')

legends = [['before', 'after'][i] for i in range(len(temperature_data_sets))]
plt.legend(legends, loc='upper left')
plt.xticks(range(1, 21))
plt.grid(True)
plt.show()
