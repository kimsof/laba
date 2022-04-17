import numpy as np

np.random.seed(3)
N = 45  # число спутников
# n = 2
# # size = N // parts
# # if N % parts:
# #     real_parts = parts + 1
data = np.zeros((N, 6), dtype=object)  # массив со всей информацией
# # for part in range(p):
# #     data[part*size:(part + 1)*size, 0] = np.random.random_sample(int(size)) * 1/(parts/2) + 1/(parts/2) * part
# #     data[part*size:(part + 1)*size, 0] = np.random.random_sample(int(size)) * 1/(parts/2) + 1/(parts/2) * part
n = 5
k = 3
l = 1/k
data[:n, 0] = np.random.random_sample(n) * 1/k
data[n:2 * n, 0] = np.random.random_sample(n) * 1/k + l * 1
data[2 * n:3 * n, 0] = np.random.random_sample(n) * 1/k + l * 2
data[3 * n:4 * n, 0] = np.random.random_sample(n) * 1/k + l * 0
data[4 * n:5 * n, 0] = np.random.random_sample(n) * 1/k + l * 1
data[5 * n:6 * n, 0] = np.random.random_sample(n) * 1/k + l * 2
data[6 * n:7 * n, 0] = np.random.random_sample(n) * 1/k + l * 0
data[7 * n:8 * n, 0] = np.random.random_sample(n) * 1/k + l * 1
data[8 * n:9 * n, 0] = np.random.random_sample(n) * 1/k + l * 2
# data[9 * n:48, 0] = np.random.random_sample(3)

data[:n, 1] = np.random.random_sample(n) * 1/k
data[n:2 * n, 1] = np.random.random_sample(n) * 1/k + l * 0
data[2 * n:3 * n, 1] = np.random.random_sample(n) * 1/k + l * 0
data[3 * n:4 * n, 1] = np.random.random_sample(n) * 1/k + l * 1
data[4 * n:5 * n, 1] = np.random.random_sample(n) * 1/k + l * 1
data[5 * n:6 * n, 1] = np.random.random_sample(n) * 1/k + l * 1
data[6 * n:7 * n, 1] = np.random.random_sample(n) * 1/k + l * 2
data[7 * n:8 * n, 1] = np.random.random_sample(n) * 1/k + l * 2
data[8 * n:9 * n, 1] = np.random.random_sample(n) * 1/k + l * 2
# data[9 * n:48, 1] = np.random.random_sample(3)
# print(data)
# data[:12, 0] = np.random.random_sample(int(N/parts)) * 0.5
# data[12:24, 0] = np.random.random_sample(12) * 0.5 + 0.5
# data[24:36, 0] = np.random.random_sample(12) * 0.5
# data[36:48, 0] = np.random.random_sample(12) * 0.5 + 0.5
# data[:12, 1] = np.random.random_sample(12) * 0.5
# data[12:24, 1] = np.random.random_sample(12) * 0.5
# data[24:36, 1] = np.random.random_sample(12) * 0.5 + 0.5
# data[36:48, 1] = np.random.random_sample(12) * 0.5 + 0.5


# N = 49   # число спутников
# n = 1    # число спутников в ячейке
# k = 7    # корень из числа ячеек
# l = 1/k  # длина стороны ячейки
#
# data = np.zeros((N, 6), dtype=object)  # массив со всей информацией
# for i in range(k):
#     for j in range(k):
#         data[((k * i + j) * n):((k * i + j + 1) * n), 0] = np.random.random_sample(n) * l + l * j
#         data[((k * i + j) * n):((k * i + j + 1) * n), 1] = np.random.random_sample(n) * l + l * i
data[:, 2] = np.random.randint(-1, 2, N)  # источник/сток/ничего
data[:, 3] = np.random.randint(4, 7, N)  # число связей (соседей) каждой точки


# функция, рандомно генерирующая соседей для каждой точки
def get_neighbours():
    # коррекция общего число связей
    if sum(data[:, 3]) % 2 != 0:
        data[np.argmax(data[:, 3]), 3] -= 1

    bonds = np.zeros(N, dtype=object)
    bonds += data[:, 3]
    sorted_bonds = sorted([[j, bonds[j]] for j in range(N)], key=lambda j: j[1], reverse=True)
    keys = []
    neighbours_total = []

    for k in range(N):
        keys.append(sorted_bonds[k][0])
        neighbours_total.append([])

    for p in range(N):
        if bonds[p] == 0:
            del keys[keys.index(p)]
    array = np.array([-1, 0, 1])
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
                        (k in [neib[0] for neib in neighbours_total[n]]) and (k in keys) and \
                        (k != n):  # and not(k in [m[0] for m in data[n, 4]]):
                    points_in_radius.append(k)
            radius += 0.01
            # print(n, radius)
            if radius > 2 ** (1 / 2):
                raise OverflowError
        aux = [[p, distances[p]] for p in points_in_radius]
        sorted_aux = sorted(aux, key=lambda j: j[1])
        # print(aux)
        points_in_radius = [a[0] for a in aux[:bonds[n]]]

        neibs = np.random.choice(points_in_radius, int(bonds[n]), False)
        neighbours_total[n] += [[neib, array[distances[neib][0]]] for neib in neibs]

        for neib in neibs:
            neighbours_total[neib].append([n, array[distances[neib][0]] * -1])
            bonds[neib] -= 1
            if bonds[neib] == 0:
                del keys[keys.index(neib)]
        print(
            f'Number: {n}\nNeighbours ({data[n, 3]}):\n{[[v[0], np.round(distances[v[0]][1], 4)] for v in neighbours_total[n]]}')
        print(points_in_radius)
        # print(n, data[n, 3], [[v[0], distances[v[0]][1]] for v in neighbours_total[n]])
        # print(distances[38])

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
