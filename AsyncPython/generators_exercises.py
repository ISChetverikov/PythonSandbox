def running_average(iterable, n):
    i = 0
    result = 0

    while True:
        if i >= len(iterable):
            return

        result += iterable[i]

        if i >= n:
            result -= iterable[i - n]

        i += 1
        yield result / n


def frange(start, stop, step):
    cur = start
    
    factor = -1 if step < 0 else 1
    while (cur - stop) * factor < 0:
        yield cur
        cur += step

    return

import random
def bit_stream():
    p = 0.5

    while True:
        p_new = yield 1 if random.random() < p else 0
        p = p if p_new is None else p_new

b = bit_stream()
print(next(b))

b.send(0.1)

r = []
for i in range(30):
    r.append(b.__next__())

print(r)