#!/usr/bin/env python
from argparse import ArgumentParser
import json
from pathlib import Path

parser = ArgumentParser()
parser.add_argument("--input", type=Path, default=Path("save"))
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()

input: Path = args.input
output: Path = args.output

pairs: list[tuple[int, float]] = []
for file in input.iterdir():
    stem = file.stem.split("_")
    id = int(stem[1])
    temperature = float(stem[3])
    pairs.append((id, temperature))

temperatures = list(map(lambda x: x[1], sorted(pairs, key=lambda x: x[0])))

output.mkdir(exist_ok=True)
with (output / "0.json").open("w") as f:
    json.dump(temperatures, f)
