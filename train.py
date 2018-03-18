import argparse
import sys
import re
from collections import defaultdict

r_alphabet = re.compile(u'[a-zA-Z0-9-]+|[.,:;?!]+')


parser = argparse.ArgumentParser(description='Создать модель текста',
                                 prog='train', fromfile_prefix_chars='@')
parser.add_argument('--input', '--input-dir', action='store',
                    help='Путь к директории, в которой лежит коллекция документов',
                    default=False)
parser.add_argument('--model', action='store',
                    help='Путь к файлу, в который сохраняется модель',
                    default=False)
parser.add_argument('--lc', action='store_true', default=False)

args = parser.parse_args()


def gen_tokens(s):
    for elem in s:
        for token in r_alphabet.findall(elem):
            print(token)
            yield token


def gen_trigrams(tokens):
    t0, t1 = '$', '$'
    for t2 in tokens:
        yield t0, t1, t2
        if t2 in '.!?':
            yield t1, t2, '$'
            yield t2, '$', '$'
            t0, t1 = '$', '$'
        else:
            t0, t1 = t1, t2


def train_itself(s):
    tokens = gen_tokens(s)
    trigrams = gen_trigrams(tokens)
    print(trigrams)
    bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

    for t0, t1, t2 in trigrams:
        bi[t0, t1] += 1
        tri[t0, t1, t2] += 1

    model = {}
    for (t0, t1, t2), freq in tri.items():
        if (t0, t1) in model:
            model[t0, t1].append((t2, freq / bi[t0, t1]))
        else:
            model[t0, t1] = [(t2, freq / bi[t0, t1])]
    print(model)


if args.model:
    g = open(args.model, 'w')
else:
    print('Пожалуйста, укажите название файла, в который нужно сохранить модель')
    sys.exit()

if args.input:
    f = open(args.input, 'r')
    for line in f:
        if args.lc:
            line = line.lower()
        train_itself(line)
else:
    for line in sys.stdin:
        if args.lc:
            line = line.lower()
        train_itself(line)
