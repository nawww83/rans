# Range ANS (rANS) кодирование с десятичным выходом
from collections import Counter
from functools import reduce
import bisect as bs

import string
import random
import time


base = 10 # Определяет основание выходной системы счисления


def encode(input):
    cc = Counter(input)
    alphabet = list(cc.keys())
    frequencies = list(cc.values())
    cumulative_frequencies = reduce(lambda x, y: x + [x[-1] + y], frequencies, [0])
    L = cumulative_frequencies[-1] # Сумма частот
    symbol_indexes = dict(zip(alphabet, range(len(alphabet)))) # Словарь "символ-индекс"
    x = 1          # Инициализация с единицы
    unit_count = 0 # Количество подряд идущих x = 1
    output = []
    for s in input:
        if x == 1:
            unit_count += 1
        #print(f'encode x: {x}')
        index = symbol_indexes[s]
        f = frequencies[index]
        while x >= base*f:
            output.append(x % base)
            x //= base
        x = (x // f) * L + (x % f) + cumulative_frequencies[index]
    #print(f'stopped at x: {x}')
    return "".join(map(str, output)), x, alphabet, frequencies, unit_count
    

def decode(input, x, alphabet, frequencies, unit_count):
    output = []
    cumulative_frequencies = reduce(lambda x, y: x + [x[-1] + y], frequencies, [0])
    L = cumulative_frequencies[-1]
    indexes_symbols = dict(zip(range(len(alphabet)), alphabet)) # Словарь "индекс-символ"
    i = len(input) - 1
    while unit_count > 0:
        #print(f'decode x: {x}')
        xmod = x % L
        # Поиск минимальной кумулятивной частоты, которая больше x 
        index = bs.bisect(cumulative_frequencies, xmod) - 1
        output.append(indexes_symbols[index])
        f = frequencies[index]
        x = (x // L) * f + xmod - cumulative_frequencies[index]
        while x < L:
            if i == -1:
                break
            x *= base
            x += int(input[i])
            i -= 1
        if x == 1:
            unit_count -= 1
    #print(f'stopped at x: {x}')
    return ''.join(output[::-1])



if __name__ == "__main__":
    rounds = 0
    while True:
        rounds += 1
        M = random.randint(1, len(string.ascii_lowercase))
        al = random.sample(string.ascii_lowercase, M)
        N = random.randint(1, 32)
        message = ''.join(random.choices(al, weights=[v*v*v for v in range(M,0,-1)], k=N))
        print(f'M:{M}, N: {N}, original message: {message}')
        output, x, a, f, uc = encode(message)
        print(f' rANS coded (init state "x", 10-digit stream): ({x}, {output})')
        print(f'  rounds: {rounds}')
        decoded_message = decode(output, x, a, f, uc)
        print(f' decoded message: {decoded_message}')
        assert(message == decoded_message)
        time.sleep(0.1)