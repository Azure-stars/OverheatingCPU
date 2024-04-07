import subprocess
import heapq
import time

# run in 2 minutes, 600 turn, every turn cost 0.2-0.4 sec
Iteration = 600
Running_Time = 0.2
TEST_INSTRUCTION_FILE = ""  # 修改所要测试的目标文件
TEMPERATURE_COMMAND = "cat /sys/class/thermal/thermal_zone0/temp"  # 读取温度
temperature_list = []


def measure_temperature():
    subprocess.run(["gcc", TEST_INSTRUCTION_FILE, "-o", "individual"])
    subprocess.run('taskset -c 0 ./individual & taskset -c 1 ./individual & '
                   'taskset -c 2 ./individual & taskset -c 3 ./individual &', shell=True)
    time.sleep(Running_Time)
    subprocess.run(["killall individual"], shell=True)
    temperature_output = subprocess.check_output(TEMPERATURE_COMMAND, shell=True)
    temperature = float(temperature_output) / 1000.0
    subprocess.run(["rm -f individual"], shell=True)
    return temperature


for i in range(Iteration):
    temperature = measure_temperature()
    temperature_list.append(temperature)

# 挑选20个较高的温度记录值，取平均
temperature_list = heapq.nlargest(20, temperature_list)
print(f"The average maximum temperature result of the test is:{round(sum(temperature_list) / len(temperature_list), 3)}")
