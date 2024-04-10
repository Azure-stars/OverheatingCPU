#!/bin/bash

for instr_seq in example/example4.s best_1.s example/example4.s best_fuyuki.s example/example4.s best.s
do
    TEMP=$(cat /sys/class/thermal/thermal_zone0/temp)
    echo TEMP=$TEMP
    while [[ $TEMP > 41000 ]]
    do
        echo "Temperature is too high. Waiting for it to cool down..."
        sleep 10
        TEMP=$(cat /sys/class/thermal/thermal_zone0/temp)
        echo TEMP=$TEMP
    done
    echo INSTR_SEQ=$instr_seq
    if [[ $instr_seq == "best.s" ]]
    then
        python temperature_test.py $instr_seq --neon
    elif [[ $instr_seq == "example/example4.s" ]]
    then
        python example/exp_test.py $instr_seq
    else
        python temperature_test.py $instr_seq
    fi
done