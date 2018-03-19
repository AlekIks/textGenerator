# textGenerator
Создание модели и генерация текста

Модель создает train.py.

#### Структура модели (построчно):
1) Некоторое число n - количество различных слов (а1,...,аn), с которых может начинаться пара
2) Далее идут n слов (ai) с описанием пар, которые начинаются с этих слов:

    2.1: Второе слово пары (bj)
    
    2.2: Количество пар <ai-bj> в тесте.
    
Удобство выбранного формата модели заключается в том, что её легко считывать и восстанавливать для последующей генерации текста. 
Кроме того, хранение количества пар вместо частоты позволит избежать возможных неточностей (количество - целое число, в отличие от частоты) и удобно для random.choice

