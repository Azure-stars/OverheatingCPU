#!/bin/bash

mkdir -p logs/max_generations

for max_generations in $(seq 20 20 100)
do
    echo MAX_GENERATIONS=$max_generations
    python genetic_algorithm.py \
        --max_generations $max_generations \
        --log logs/max_generations/$max_generations.json
    sleep 300
done
