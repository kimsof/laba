import numpy as np

np.random.seed(2)

a = 8
b = 6
N = a * b  # число спутников
q = 1 / a
w = 1 / (b - 1)
x = [q * i for i in range(a)] * b
y = []
for i in range(b):
    y += [w * i] * a

data = np.zeros((N, 6), dtype=object)  # массив со всей информацией
data[:, 0] = x  # x каждой точки
data[:, 1] = y  # y каждой точки
data[:, 2] = np.random.randint(-1, 2, N)  # источник/сток/ничего
delta = np.random.randint(0, 3, N)
data[:, 3] = np.array([3] * 8 + [4] * 32 + [3] * 8) + delta  # число соседей

# data[7, 3] = 6
# delta[7] = 0
array = np.array([-1, 0, 1])

# dx = y[1] - x[0]
# print(dx)
def y(t, z):
    return [t, array[z]]


neighbour = np.zeros(N, dtype=object)
neighbour[0] = [y(1, 1), y(a - 1, 2), y(a, 1)]
for i in range(1, a - 1):
    neighbour[i] = [y(i - 1, 1), y(i + 1, 1), y(i + a, 1)]
neighbour[a - 1] = [y(0, 0), y(a - 2, 1), y(2 * a - 1, 1)]
for i in range(a, a * (b - 1)):
    if i % a == 0:
        neighbour[i] = [y(i - a, 1), y(i + 1, 1), y(i + a - 1, 2), y(i + a, 1)]
    elif (i + 1) % a == 0:
        neighbour[i] = [y(i - a, 1), y(i - (a - 1), 0), y(i - 1, 1), y(i + a, 1)]
    else:
        neighbour[i] = [y(i - a, 1), y(i - 1, 1), y(i + 1, 1), y(i + a, 1)]
neighbour[a * (b - 1)] = [y(a * (b - 2), 1), y(a * (b - 1) + 1, 1), y(a * b - 1, 2)]
for i in range(a * (b - 1) + 1, a * b - 1):
    neighbour[i] = [y(i - 1, 1), y(i + 1, 1), y(i - a, 1)]
neighbour[a * b - 1] = [y(a * (b - 1) - 1, 1), y(a * (b - 1), 1), y(a * b - 2, 1)]
data[:, 4] = neighbour


# функция, рандомно генерирующая соседей для каждой точки
def get_neighbours():
    # коррекция общего число связей
    if sum(data[:, 3]) % 2 != 0:
        data[np.argmax(data[:, 3]), 3] -= 1

    bonds = np.zeros(N, dtype=object)
    bonds += delta
    sorted_bonds = sorted([[j, bonds[j]] for j in range(N)], key=lambda j: j[1], reverse=True)
    # print(sorted_bonds)
    keys = []
    neighbours_total = []

    for k in range(N):
        keys.append(sorted_bonds[k][0])
        neighbours_total.append(data[k, 4])

    for p in range(N):
        if bonds[p] == 0:
            del keys[keys.index(p)]
    # print(keys)

    while len(keys) > 0:
        n = keys[0]
        del keys[0]
        x_n = data[n, 0]
        y_n = data[n, 1]
        distances = np.zeros(N, dtype=object)

        for l in range(N):
            distance_variants = np.zeros(3)
            for j in range(3):
                distance_variants[j] = ((data[l, 0] - (x_n + array[j])) ** 2 +
                                        (data[l, 1] - y_n) ** 2) ** (1 / 2)
            distances[l] = [np.argmin(distance_variants), distance_variants[np.argmin(distance_variants)]]

        radius = 0
        points_in_radius = []
        while len(points_in_radius) < bonds[n]:
            for k in range(N):
                if (distances[k][1] < radius) and not (k in points_in_radius) and not \
                        (k in [neib[0] for neib in neighbours_total[n]]) and (k in keys) and (
                        k != n):  # and not(k in [m[0] for m in data[n, 4]]):
                    points_in_radius.append(k)
            radius += 0.01
            if radius > 2 ** (1 / 2):# if radius > 2 * dx+0.05:  # radius > 2 ** (1 / 2):
                raise OverflowError

        neibs = np.random.choice(points_in_radius, int(bonds[n]), False)
        neighbours_total[n] += [[neib, array[distances[neib][0]]] for neib in neibs]

        for neib in neibs:
            neighbours_total[neib].append([n, array[distances[neib][0]] * -1])
            bonds[neib] -= 1
            if bonds[neib] == 0:
                del keys[keys.index(neib)]
        # print(n, neighbours_total[n])

    return neighbours_total


# число связей (соседей) каждой точки
# не всегда функции get_neighbours() удается распределить соседей корректно для всех точек c 1 раза, поэтому:
for i in range(1000):
    try:
        # print('e')
        neighbours = get_neighbours()
        break
    except OverflowError:
        continue

for i in range(N):
    data[i, 4] = sorted(neighbours[i], key=lambda j: j[0])

