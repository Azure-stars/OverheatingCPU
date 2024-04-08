import subprocess
import heapq
import time

# run in 4-6 minutes, 900 turn, every turn cost 0.2-0.4 sec
Iteration = 900
Running_Time = 0.2
OLD_FILE = "main.s"
BEST_FILE = "best.s"
TEST_INSTRUCTION_FILE = "main_best.s"      # 填写测试的指令片段文件名
TEMPERATURE_COMMAND = "cat /sys/class/thermal/thermal_zone0/temp"  # 读取温度
temperature_list = []

# 将指令序列写入文件
def write_instructions_to_file(instruction_filename, old_filename, new_filename):
    # main.s 源文件
    old_file = open(old_filename, 'r')
    old_file_lines = old_file.readlines()
    replace_index = old_file_lines.index("\tYour instruction code\n")
    old_file.close()

    # main_best.s 新生成的指令序列文件
    new_file = open(new_filename, 'w')
    for i in range(0, replace_index):
        new_file.write(old_file_lines[i])

    with open (instruction_filename, 'r') as f:
        new_file.write(f.read())

    for i in range(replace_index + 1, len(old_file_lines)):
        new_file.write(old_file_lines[i])

    new_file.close()


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

write_instructions_to_file(BEST_FILE, OLD_FILE, TEST_INSTRUCTION_FILE)

for i in range(Iteration):
    temperature = measure_temperature()
    temperature_list.append(temperature)

# 挑选20个较高的温度记录值，取平均
temperature_list = heapq.nlargest(20, temperature_list)
print(f"The average maximum temperature result of the test is:{round(sum(temperature_list) / len(temperature_list), 3)}")
