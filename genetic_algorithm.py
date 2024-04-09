from argparse import ArgumentParser
import json
import random
import os
import subprocess
import time
import shutil
import xml.etree.ElementTree as ET

parser = ArgumentParser()
parser.add_argument('--neon', action='store_true', default=False)
parser.add_argument('--population_size', type=int, default=20)
parser.add_argument('--max_generations', type=int, default=20)
parser.add_argument('--crossover_rate', type=float, default=0.8)
parser.add_argument('--mutation_rate', type=float, default=0.1)
parser.add_argument('--elitism_rate', type=float, default=0.1)
parser.add_argument('--instruction_length', type=int, default=20)
parser.add_argument('--log', type=str, default=None)

args = parser.parse_args()

# 遗传算法参数
POPULATION_SIZE = args.population_size  # 每一代种群数量
MAX_GENERATIONS = args.max_generations  # 最大迭代次数
CROSSOVER_RATE = args.crossover_rate  # 交叉概率
MUTATION_RATE = args.mutation_rate  # 变异概率
ELITISM_RATE = args.elitism_rate  # 精英保留比例

# 指令相关参数
INSTRUCTION_LENGTH = args.instruction_length  # 指令序列长度

# 文件格式声明
ORIGIN_INSTRUCTION_FILE = "main_neon.s" if args.neon else "main.s"  # 初始指令序列文件（为空）
NEW_INSTRUCTION_FILE = "new.s"  # 算法迭代生成的指令序列文件
BEST_INSTRUCTION_FILE = 'best.s'  # 最优指令序列文件
SAVE_FOLDER = "save"  # 指令序列文件保存目录
TMP_FOLDER = 'tmp'  # 指令序列文件临时目录
TEMPERATURE_COMMAND = "cat /sys/class/thermal/thermal_zone0/temp"  # 读取温度

# 不可修改Running_Time
Running_Time = 0.2


# 加载指令格式
def load_instructions():
    instructions = []
    tree = ET.parse('instructions.xml')
    root = tree.getroot()
    for instruction_node in root.iter('instruction'):
        opcode = instruction_node.find('opcode').text
        operands = [operand.text for operand in instruction_node.iter('operand')]
        instructions.append((opcode, operands))
    return instructions

# 生成一条随机的指令
def generate_one_instruction(instructions):
    general_register_numbers = [f"r{i}" for i in range(13)]
    double_register_numbers = [f"d{i}" for i in range(32)]
    quad_register_numbers = [f"q{i}" for i in range(16)]

    instruction = random.choice(instructions)
    opcode = instruction[0]
    operands = []
    for operand in instruction[1]:
        if operand.startswith("reg"):
            operands.append(random.choice(general_register_numbers))
        elif operand.startswith("num"):
            operand_values = operand.split("T")
            min_value = int(operand_values[0][3:])
            max_value = int(operand_values[1])
            operand_value = random.randint(min_value, max_value)
            operands.append(f"#{operand_value}")
        elif operand.startswith("stack point"):
            operands.append("[r13]")
        elif operand.startswith("dreg"):
            operands.append(random.choice(double_register_numbers))
        elif operand.startswith("qreg"):
            operands.append(random.choice(quad_register_numbers))
        elif operand.startswith("nop"):
            pass

    return opcode, operands

# 生成随机的指令序列
def generate_random_instructions(instructions, length):
    random_instructions = []
    for _ in range(length):
        opcode, operands = generate_one_instruction(instructions)
        random_instructions.append((opcode, operands))
    return random_instructions


# 将指令序列写入文件
def write_instructions_to_file(instructions, old_filename, new_filename):
    # main.s 源文件
    old_file = open(old_filename, 'r')
    old_file_lines = old_file.readlines()
    replace_index = old_file_lines.index("\tYour instruction code\n")
    old_file.close()

    # new.s 新生成的指令序列文件
    new_file = open(new_filename, 'w')
    for i in range(0, replace_index):
        new_file.write(old_file_lines[i])

    for instruction in instructions:
        opcode, operands = instruction
        instruction_code = f"\t{opcode}\t{' ,'.join(operands)}\n"
        new_file.write(instruction_code)

    for i in range(replace_index + 1, len(old_file_lines)):
        new_file.write(old_file_lines[i])

    new_file.close()


def write_best_instructions_to_file(instructions, filename):
    file = open(filename, 'w')
    for instruction in instructions:
        opcode, operands = instruction
        instruction_code = f"\t{opcode}\t{' ,'.join(operands)}\n"
        file.write(instruction_code)
        print(f"{opcode}\t{' ,'.join(operands)}")
    file.close()


# 编译指令文件并测量温度
def measure_temperature():
    subprocess.run(["gcc", NEW_INSTRUCTION_FILE, "-o", "individual"])
    subprocess.run('taskset -c 0 ./individual & taskset -c 1 ./individual & '
                   'taskset -c 2 ./individual & taskset -c 3 ./individual &', shell=True)
    time.sleep(Running_Time)
    subprocess.run(["killall individual"], shell=True)
    temperature_output = subprocess.check_output(TEMPERATURE_COMMAND, shell=True)
    temperature = float(temperature_output) / 1000.0
    subprocess.run(["rm -f individual"], shell=True)
    return temperature


# 交叉操作
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


# 变异操作
def mutate(individual, instructions):
    mutation_point = random.randint(0, len(individual) - 1)
    opcode, operands = generate_one_instruction(instructions)
    individual[mutation_point] = (opcode, operands)
    return individual


# 遗传算法
def genetic_algorithm():
    # 加载指令并创建初始种群
    instructions = load_instructions()
    population = [generate_random_instructions(instructions, INSTRUCTION_LENGTH) for _ in range(POPULATION_SIZE)]

    # 创建指令序列文件的保存目录
    subprocess.run(["rm -rf tmp/"], shell=True)
    subprocess.run(["rm -rf save/"], shell=True)
    if not os.path.exists(TMP_FOLDER):
        os.makedirs(TMP_FOLDER)
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)

    # 记录最高的测量温度和指令序列个体
    best_fitness = float('-inf')
    best_individual = None
    final_data = []

    max_fitnesses = []

    for generation in range(MAX_GENERATIONS):
        print(f"Generation {generation + 1}")

        # 评估适应度并测量温度
        
        fitness_scores = []
        for itemindex in range(len(population)):
            individual = population[itemindex]
            write_instructions_to_file(individual, ORIGIN_INSTRUCTION_FILE, NEW_INSTRUCTION_FILE)
            temperature = measure_temperature()
            fitness_scores.append(temperature)
            # 保存每一代的临时指令序列文件
            shutil.copyfile(NEW_INSTRUCTION_FILE, f"{TMP_FOLDER}/{generation + 1}_{itemindex + 1}_{temperature}.s")

        # 保存当前轮的最佳指令序列文件
        max_fitness = max(fitness_scores)
        max_fitness_index = fitness_scores.index(max_fitness)
        final_data.append(round(max_fitness, 3))
        print(f"max temperature is:{round(max_fitness, 3)}")
        shutil.copyfile(f"{TMP_FOLDER}/{generation + 1}_{max_fitness_index + 1}_{max_fitness}.s",
                        f"{SAVE_FOLDER}/generation_{generation + 1}_best_{max_fitness}.s")

        # 更新最佳个体
        max_fitnesses.append(max_fitness)
        if max_fitness > best_fitness:
            best_fitness = max_fitness
            best_individual = population[fitness_scores.index(max_fitness)]

        # 选择下一代种群
        new_population = []

        # 精英保留
        elitism_count = int(ELITISM_RATE * POPULATION_SIZE)
        elite_individuals = sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)[:elitism_count]
        new_population.extend([individual for individual, _ in elite_individuals])

        # 交叉操作
        crossover_count = int(CROSSOVER_RATE * POPULATION_SIZE)
        for _ in range(crossover_count):
            parent1, parent2 = random.choices(population, k=2)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([child1, child2])

        # 变异操作
        mutation_count = int(MUTATION_RATE * POPULATION_SIZE)
        for _ in range(mutation_count):
            individual = random.choice(population)
            mutated_individual = mutate(individual, instructions)
            new_population.append(mutated_individual)

        # 填充剩余个体
        while len(new_population) < POPULATION_SIZE:
            new_population.append(generate_random_instructions(instructions, INSTRUCTION_LENGTH))

        population = new_population
        
    print(final_data)

    # 输出最佳指令序列
    print("Best Individual:")
    # 将最佳指令序列写入文件
    write_best_instructions_to_file(best_individual, BEST_INSTRUCTION_FILE)
    # 输出最高温度
    print("Best Temperature:")
    print(best_fitness)

    return max_fitnesses


# 运行遗传算法
max_fitnesses = genetic_algorithm()

if args.log:
    with open(args.log, 'w') as f:
        json.dump(max_fitnesses, f)
