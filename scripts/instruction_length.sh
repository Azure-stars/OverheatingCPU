#!/bin/bash

mkdir -p logs/instruction_length

for instruction_length in $(seq 10 10 50)
do
    echo INSTRUCTION_LENGTH=$instruction_length
    python genetic_algorithm.py \
        --instruction_length $instruction_length \
        --log logs/instruction_length/$instruction_length.json
    sleep 300
done
