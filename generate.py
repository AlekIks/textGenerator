import argparse
import sys
import re
from collections import defaultdict
import random

r_alphabet = re.compile(u'[a-zA-Z0-9-]+|[.,:;?!]+')

# ########################################
# Здесь описано консольное взаимодействие

parser = argparse.ArgumentParser(description='Генерация текст',
                                 prog='generate', fromfile_prefix_chars='@')
parser.add_argument('--length', action='store',
                    help='длина генерируемой последовательности',
                    default=False)
parser.add_argument('--model', action='store',
                    help='Путь к файлу, из которого загружается модель',
                    default=False)
parser.add_argument('--seed', action='store_true', default=False,
                    help='Начальное слово. Если не указано, выбираем слово '
                         'случайно из всех слов (не учитывая частоты)')
parser.add_argument('--output', action='store_true', default=False,
                    help='Файл, в который будет записан результат. '
                         'Если аргумент отсутствует, выводить в stdout.')

args = parser.parse_args()

# ARGS
if args.model:
    f = open(args.model, 'r')
else:
    print('Пожалуйста, укажите файл, из которого нужно загрузить модель')
    sys.exit()

if args.length:
    n = args.length
else:
    print('Пожалуйста, укажите длину последовательности')
    sys.exit()

# ########################################
# ЧТЕНИЕ МОДЕЛИ

model = defaultdict(list)

t = int(f.readline())

for i in range(t):
    name = f.readline()
    num = int(f.readline())
    lines = []
    for j in range(num):
        line = f.readline()
        freq_line = int(f.readline())
        lines.append([line[0:len(line)-1], freq_line])
    model[name[0:len(name)-1]] = lines

# ########################################
# ПЕЧАТЬ ТЕКСТА В ФАЙЛ/STDOUT

t0 = ''
if args.seed:
    t0 = args.seed
else:
    t0 = random.choice([k for k in model.keys()])

if args.output:
    g = open(args.output, 'w')

s = ''
for j in range(int(args.length)):
    if args.output:
        g.write(t0 + ' ')
    else:
        s += t0 + ' '
    loc = model[t0]
    t0 = random.choice([loc[k][0] for k in range(len(loc)) for num in range(loc[k][1])])

if args.output:
    g.close()
else:
    print(s)
f.close()
