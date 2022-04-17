import numpy as np

np.random.seed(6)
nc = 49  # число ячеек
k = int(np.sqrt(nc))  # корень из числа ячеек
n = 1  # число спутников в ячейке
N = n * nc  # число спутников
l = 1 / k  # длина стороны ячейки
data = np.zeros((N, 6), dtype=object)  # массив со всей информацией
for i in range(k):
    for j in range(k):
        data[((k * i + j) * n):((k * i + j + 1) * n), 0] = np.random.random_sample(n) * l + l * j
        data[((k * i + j) * n):((k * i + j + 1) * n), 1] = np.random.random_sample(n) * l + l * i
data[:, 2] = np.random.randint(-1, 2, N)  # источник/сток/ничего


data[:, 3] = np.random.randint(4, 8, N)  # число связей (соседей) каждой точки


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
    # max_distance = 0.3
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
            if radius > 2 ** (1 / 2):
                raise OverflowError
        aux = [[p, distances[p]] for p in points_in_radius]
        sorted_aux = sorted(aux, key=lambda j: j[1])
        points_in_radius = [a[0] for a in sorted_aux[:bonds[n]]]

        neibs = np.random.choice(points_in_radius, int(bonds[n]), False)
        neighbours_total[n] += [[neib, array[distances[neib][0]]] for neib in neibs]
        # print(f'Number: {n}')
        # print([(element, distances[element[0]][1]) for element in neighbours_total[n]] )
        for neib in neibs:
            bonds[neib] -= 1
            if bonds[neib] == 0:
                del keys[keys.index(neib)]

            # if distances[neib][1] < max_distance:

            neighbours_total[neib].append([n, array[distances[neib][0]] * -1])
            # else:
            #     data[n, 3] -= 1
            #     data[neib, 3] -= 1
            #     del neighbours_total[n][neighbours_total[n].index([neib, array[distances[neib][0]]])]

        # print(f'Number: {n}')  #}\nNeighbours ({data[n, 3]}):\n{[[v[0], np.round(distances[v[0]][1], 4)] for v in neighbours_total[n]]}')
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

# from scipy.spatial import Voronoi, voronoi_plot_2d
# yey = data[:, :2]
# vor = Voronoi(yey)
#
# ridges = vor.ridge_points
# neibs = []
# for i in range(N):
#     neibs.append([])
# for ridge in ridges:
#     neibs[ridge[0]].append([ridge[1], 0])
#     neibs[ridge[1]].append([ridge[0], 0])

for i in range(N):
    data[i, 4] = sorted(neighbours[i], key=lambda j: j[0])

# for i in range(N):
#     data[i, 4] = sorted(neibs[i], key=lambda j: j[0])
#     data[i, 3] = len(data[i, 4])

