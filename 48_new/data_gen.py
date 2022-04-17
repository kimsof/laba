import numpy as np

np.random.seed(100)

a = 8
b = 6
N = a * b  # число спутников
q = 1 / a
w = 1 / (b - 1)
x = [0] * a  # list(np.zeros(a))
for i in range(a):
    x[i] = q * i
x = x * b
y = []
for i in range(b):
    y += [w * i] * a

data = np.zeros((N, 6), dtype=object)  # массив со всей информацией
data[:, 0] = x  # np.random.random_sample((N, 2))  # x и y каждой точки
data[:, 1] = y
data[:, 2] = np.random.randint(-1, 2, N)  # источник/сток/ничего
data[:, 3] = np.random.randint(0, 3, N)

# def y(t, z):
#     return [t, array[z]]
# array = np.array([[-1, 0], [0, 0], [1, 0]])
# neighbour = np.zeros(N, dtype=object)
# neighbour[0] = [y(1, 1), y(a - 1, 2), y(a, 1)]
# for i in range(1, a - 1):
#     neighbour[i] = [y(i - 1, 1), y(i + 1, 1), y(i + a, 1)]
# neighbour[a - 1] = [y(0, 0), y(a - 2, 1), y(2 * a - 1, 1)]
# for i in range(a, a * (b - 1)):
#     if i % a == 0:
#         neighbour[i] = [y(i - a, 1), y(i + 1, 1), y(i + a - 1, 2), y(i + a, 1)]
#     elif (i + 1) % a == 0:
#         neighbour[i] = [y(i - a, 1), y(i - (a - 1), 0), y(i - 1, 1), y(i + a, 1)]
#     else:
#         neighbour[i] = [y(i - a, 1), y(i - 1, 1), y(i + 1, 1), y(i + a, 1)]
# neighbour[a * (b - 1)] = [y(a * (b - 2), 1), y(a * (b - 1) + 1, 1), y(a * b - 1, 2)]
# for i in range(a * (b - 1) + 1, a * b - 1):
#     neighbour[i] = [y(i - 1, 1), y(i + 1, 1), y(i - a, 1)]
# neighbour[a * b - 1] = [y(a * (b - 1) - 1, 1), y(a * (b - 1), 1), y(a * b - 2, 1)]
# data[:, 4] = neighbour
# for i in range(N):
#     data[i, 3] = len(neighbour[i])  # число связей (соседей) каждой точки


# функция, рандомно генерирующая соседей для каждой точки
def get_neighbours():
    # коррекция общего число связей
    if sum(data[:, 3]) % 2 != 0:
        data[np.argmax(data[:, 3]), 3] -= 1
    array = np.array([[-1, 0], [0, 0], [1, 0]])

    bonds = np.zeros(N, dtype=object)
    bonds += data[:, 3]
    sorted_bonds = sorted([[j, bonds[j]] for j in range(N)], key=lambda j: j[1], reverse=True)

    keys = []
    neighbours_total = []
    for k in range(N):
        keys.append(sorted_bonds[k][0])
        neighbours_total.append([])

    for v in range(N):
        x_n = data[v, 0]
        y_n = data[v, 1]
        distances = np.zeros(N, dtype=object)

        for s in range(N):
            distance_variants = np.zeros(3)
            for j in range(3):
                distance_variants[j] = ((x_n - (data[s, 0] + array[j][0])) ** 2 +
                                        (y_n - (data[s, 1] + array[j][1])) ** 2) ** (1 / 2)
            distances[s] = [np.argmin(distance_variants), distance_variants[np.argmin(distance_variants)]]

        aux = sorted([[j, distances[j][1]] for j in range(N)], key=lambda j: j[1])
        aux1 = list(np.array(aux)[:, 0][1:5])
        # print(aux1[2])
        # print(distances[8][0])
        # print(distances[aux1[2]][0])
        aux2 = [[aux1[p], array[distances[int(aux1[p])][0]]] for p in range(len(aux1))]
        # print(list(np.array(aux)[:, 0][1:5]))
        neighbours_total[v] += aux2
        # print(neighbours_total[v])

    while len(keys) > 0:
        n = keys[0]
        print(bonds[n], n)
        del keys[0]
        x_n = data[n, 0]
        y_n = data[n, 1]
        distances = np.zeros(N, dtype=object)

        for l in range(N):
            distance_variants = np.zeros(3)
            for j in range(3):
                distance_variants[j] = ((x_n - (data[l, 0] + array[j][0])) ** 2 +
                                        (y_n - (data[l, 1] + array[j][1])) ** 2) ** (1 / 2)
            distances[l] = [np.argmin(distance_variants), distance_variants[np.argmin(distance_variants)]]

        radius = 0
        points_in_radius = []
        while len(points_in_radius) < bonds[n]:
            for k in range(N):
                if (distances[k][1] < radius) and not (k in points_in_radius) and not \
                        (k in [neib[0] for neib in neighbours_total[n]]) and (k in keys) and (k != n):
                    points_in_radius.append(k)
            radius += 0.01
            if radius > 2 ** (1 / 2):
                raise OverflowError
        if len(points_in_radius) > 2:
            neibs = np.random.choice(points_in_radius, int(bonds[n]), False)
        else:
            neibs = points_in_radius
        # print(neibs)
        neighbours_total[n] += [[neib, array[distances[neib][0]]] for neib in neibs]

        for neib in neibs:
            neighbours_total[neib].append([n, array[distances[neib][0]] * -1])
            bonds[neib] -= 1
            if bonds[neib] == 0:
                del keys[keys.index(neib)]

    return neighbours_total


# N = 100
# data = np.zeros((N, 6), dtype=object)  # массив со всей информацией
# data[:, :2] = np.random.random_sample((N, 2))  # x и y каждой точки
# data[:, 2] = np.random.randint(-1, 2, N)  # источник/сток/ничего
# data[:, 3] = np.random.randint(4, 11, N)  # число связей (соседей) каждой точки
# if sum(data[:, 3]) % 2 != 0:
#     data[np.argmax(data[:, 3]), 3] -= 1

  # число связей (соседей) каждой точки
# не всегда функции get_neighbours() удается распределить соседей корректно для всех точек c 1 раза, поэтому:
for i in range(1000):
    try:
        neighbours = get_neighbours()
        break
    except OverflowError:
        continue
#
for i in range(N):
    neighbours[i] = sorted(neighbours[i], key=lambda i: i[0])
    data[i, 4] = neighbours[i]
