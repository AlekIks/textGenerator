import argparse
import sys
import re
from collections import defaultdict

r_alphabet = re.compile(u'[a-zA-Z_]+') # нет кириллицы, но есть зачем-то нижнее подчеркивание

# ########################################
# Здесь описано консольное взаимодействие

parser = argparse.ArgumentParser(description='Создание модель текста',
                                 prog='train', fromfile_prefix_chars='@')
parser.add_argument('--input', '--input-dir', action='store',
                    help='Путь к директории, в которой лежит коллекция документов',
                    
                    # а читаешь из файла только!
                    # написано же про папку, нужно читать все .txt файлы из папки
                    
                    default=False)
parser.add_argument('--model', action='store',
                    help='Путь к файлу, в который сохраняется модель',
                    default=False)
parser.add_argument('--lc', action='store_true',
                    help='Приводить тексты к lowercase', default=False)

args = parser.parse_args()

# ########################################
# GENERATOR OF LINES


def gen_lines():
    """
    :rtype: gen_lines
    Генератор считывания текста из файла,
    либо из stdin (в зависимости от того,
    как пользователем задан input)
    """
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

# ########################################
# GENERATOR OF CLEAR WORDS


def gen_tokens(s):
    """
    :rtype: gen_tokens
    Генератор, возвращает "очищенные" от неалфавитных символов слова из строк
    """
    for elem in s:  # оставила бы line in lines, так же понятнее
        for token in r_alphabet.findall(elem):
            yield token

# ########################################
# GENERATOR OF WORD PAIRS


def gen_bigrams(tokens):
    """
    :param tokens:
    Генератор пар слов (предыдущее-последующее)
    :return: пара
    """
    t1 = '$'
    for t2 in tokens:
        if t1 != '$':
            yield t1, t2
        t1 = t2

# ########################################
# MODEL CREATING


def train_itself():  # сюда передавать файл в который пишешь, а не глобально его определять
    """
    Функция, создающая словарь (model),
    где ключ - слово,
    а значение - пара (следующее слово + частота встречаемости пары)
    :return:
    """
    lines = gen_lines()
    tokens = gen_tokens(lines)
    b_grams = gen_bigrams(tokens)
    bi = defaultdict(int)

    for t0, t1 in b_grams:  # t0, t1 переназвать
        bi[t0, t1] += 1

    model = defaultdict(set)
    for t0, t1 in bi.keys():
        model[t0].add((t1, bi[t0, t1]))

    g.write(str(len(model)) + '\n')

    for key in model.keys():   # используй здесь pickle
        g.write(str(key) + '\n')
        g.write(str(len(model[key])) + '\n')
        for elem in model[key]:
            g.write(elem[0] + '\n')
            g.write(str(elem[1]) + '\n')


# ########################################
# CALL OF FUNCTIONS

if args.model:
    g = open(args.model, 'w')
else:
    print('Пожалуйста, укажите название файла, в который нужно сохранить модель')
    sys.exit()

train_itself()
g.close()
