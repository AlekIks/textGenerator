import argparse
import sys
import re
from collections import defaultdict

r_alphabet = re.compile(u'[a-zA-Z0-9-]+|[.,:;?!]+')


parser = argparse.ArgumentParser(description='Сгенерировать текст',
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
