import argparse
import sys
import re
from collections import defaultdict

r_alphabet = re.compile(u'[a-zA-Z_]+')


parser = argparse.ArgumentParser(description='Создать модель текста',
                                 prog='train', fromfile_prefix_chars='@')
parser.add_argument('--input', '--input-dir', action='store',
                    help='Путь к директории, в которой лежит коллекция документов',
                    default=False)
parser.add_argument('--model', action='store',
                    help='Путь к файлу, в который сохраняется модель',
                    default=False)
parser.add_argument('--lc', action='store_true',
                    help='Приводить тексты к lowercase', default=False)

args = parser.parse_args()


def gen_lines():
    if args.input:
        f = open(args.input, 'r')
        for line in f:
            if args.lc:
                yield line.lower()
            else:
                yield line
        f.close()
    else:
        for line in sys.stdin:
            if args.lc:
                yield line.lower()
            else:
                yield line


def gen_tokens(s):
    for elem in s:
        for token in r_alphabet.findall(elem):
            yield token


def gen_bigrams(tokens):
    t1 = '$'
    for t2 in tokens:
        if t1 != '$':
            yield t1, t2
        t1 = t2


def train_itself():
    lines = gen_lines()
    tokens = gen_tokens(lines)
    b_grams = gen_bigrams(tokens)
    bi = defaultdict(int)

    for t0, t1 in b_grams:
        bi[t0, t1] += 1

    model = defaultdict(set)
    for t0, t1 in bi.keys():
        model[t0].add((t1, bi[t0, t1]))

    g.write(str(len(model)) + '\n')

    for key in model.keys():
        g.write(str(key) + '\n')
        g.write(str(len(model[key])) + '\n')
        for elem in model[key]:
            g.write(elem[0] + '\n')
            g.write(str(elem[1]) + '\n')


if args.model:
    g = open(args.model, 'w')
else:
    print('Пожалуйста, укажите название файла, в который нужно сохранить модель')
    sys.exit()

train_itself()
g.close()
