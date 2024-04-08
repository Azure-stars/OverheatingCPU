## 这个文件是用于画图的文件，大家可以复用

import argparse
from argparse import FileType
import json
from pathlib import Path

import matplotlib.pyplot as plt

def check_dir(path: str):
    if not Path(path).is_dir():
        raise NotADirectoryError(path)
    else:
        return Path(path)

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=check_dir)
parser.add_argument('--output', type=str)
parser.add_argument('--title', type=str)
parser.add_argument('--legend', type=str)
args = parser.parse_args()

input_dir: Path = args.input

temperature_data_sets = []
files = sorted(list(input_dir.iterdir()), key=lambda x: int(x.stem))
for file in files:
    with file.open() as f:
        temperature_data_sets.append(json.load(f))

plt.figure(dpi=600)
colors = ['blue', 'green', 'red', 'orange', 'purple']
for i, data in enumerate(temperature_data_sets):
    xdata = range(1, len(data) + 1)
    plt.plot(xdata, data, marker='o', linestyle='-', color=colors[i])

plt.xlabel('Generation')
plt.ylabel('Temperature')
plt.title(args.title)

legends = [f'{args.legend}={file.stem}' for file in files]
plt.legend(legends, loc='lower right')
plt.xticks(range(0, max(map(len, temperature_data_sets)) + 1, 5))
plt.grid(True)
plt.savefig(args.output)
