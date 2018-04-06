import argparse
import sys
import re
from collections import defaultdict
import os
import pickle

r_alphabet = re.compile(u'[а-яА-Яa-zA-Z]+')

# ########################################
# КОНСОЛЬНОЕ ВЗАИМОДЕЙСТВИЕ


def deal_with_console():
    """
    Аргументы для запуска из консоли
    :return: доступ к ним
    """
    parser = argparse.ArgumentParser(description='Создание модель текста',
                                     prog='train', fromfile_prefix_chars='@')
    parser.add_argument('--input', '--input-dir', action='store',
                        help='Путь к директории, в которой лежит коллекция документов',
                        default=False)
    parser.add_argument('--model', action='store',
                        help='Путь к файлу, в который сохраняется модель',
                        default=False)
    parser.add_argument('--lc', action='store_true',
                        help='Приводить тексты к lowercase', default=False)

    return parser.parse_args()

# ########################################
# GENERATOR OF LINES FROM STDIN


def gen_lines_from_stdin(args):
    """
    Генератор строк из консоли
    :param args: то, что ввели в консоли
    :return: строки
    """
    for line in sys.stdin:
        if args.lc:
            yield line.lower()
        else:
            yield line


# ########################################
# GENERATOR OF LINES FROM DIRECTORY


def gen_lines_from_directory(args):
    """
    Генератор строк из файлов, которые находятся в директории
    :param args: то, что ввели в консоли
    :return: строки
    """
    directory = os.listdir(args.input)
    for file in directory:
        f = open(os.path.join(args.input, file), 'r')
        for line in f:
            if args.lc:
                yield line.lower()
            else:
                yield line


# ########################################
# GENERATOR OF CLEAR WORDS


def gen_tokens(lines):
    """
    :rtype: gen_tokens
    Генератор, возвращает "очищенные" от неалфавитных символов слова из строк
    """
    for line in lines:
        for token in r_alphabet.findall(line):
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


def train_itself():
    """
    Функция, создающая словарь (model),
    где ключ - слово,
    а значение - пара (следующее слово + частота встречаемости пары)
    :return:
    """
    args = deal_with_console()
    if not args.model:
        print('Пожалуйста, укажите название файла, в который нужно сохранить модель')
        sys.exit()

    g = open(args.model, 'wb')
    if args.input:
        lines = gen_lines_from_directory(args)
    else:
        lines = gen_lines_from_stdin(args)

    tokens = gen_tokens(lines)
    b_grams = gen_bigrams(tokens)
    bi = defaultdict(int)

    for word0, word1 in b_grams:
        bi[word0, word1] += 1

    model = defaultdict(set)
    for word0, word1 in bi.keys():
        model[word0].add((word1, bi[word0, word1]))

    pickle.dump(model, g)


# ########################################
# CALL OF FUNCTIONS

if __name__ == '__main__':
    train_itself()
