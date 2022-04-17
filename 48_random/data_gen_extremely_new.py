import numpy as np
from scipy.spatial import Voronoi

# ДОРАБОТАТЬ ДЛЯ ПРОИЗВОЛЬНОГО ЧИСЛА ЯЧЕЕК
np.random.seed(6)
nc = 16  # число ячеек
n = 1  # число спутников в ячейке
N = n * nc  # число спутников
k = int(np.sqrt(nc))  # корень из числа ячеек
l = 1 / k  # длина стороны ячейки

data = np.zeros((N, 6), dtype=object)  # массив со всей информацией

# заполнение х и у
for i in range(k):
    for j in range(k):
        data[((k * i + j) * n):((k * i + j + 1) * n), 0] = np.random.random_sample(n) * l + l * j
        data[((k * i + j) * n):((k * i + j + 1) * n), 1] = np.random.random_sample(n) * l + l * i
data[:, 1] = -data[:, 1] + 1

# заполнение neighbours
mapped_data = np.zeros((N, 2))
mapped_data[:, :] = data[:, :2]

neighbours, mapped_neighbours = [], []

for n in range(N):
    neighbours.append([])
    mapped_neighbours.append([])

    if data[n, 0] < 0.5:
        mapped_data[n, 0] += 1

vor = Voronoi(data[:, :2])
mapped_vor = Voronoi(mapped_data)

ridges = vor.ridge_points
mapped_ridges = mapped_vor.ridge_points

for ridge in ridges:
    neighbours[ridge[0]].append([ridge[1], 0])
    neighbours[ridge[1]].append([ridge[0], 0])

for mapped_ridge in mapped_ridges:
    mapped_neighbours[mapped_ridge[0]].append([mapped_ridge[1], 0])
    mapped_neighbours[mapped_ridge[1]].append([mapped_ridge[0], 0])

for n in range(N):
    #     w = ''
    #     if n in [0, 6, 7, 12, 13, 14, 20, 21, 27,28,34,35,36,41,42,48]:
    #         w = ' *'
    #     print(str(n) + w)
    #     print(f'before: {sorted(neighbours[n], key=lambda j: j[0])}')
    if 0.8 < mapped_data[n, 0] < 1.2:
        for i in range(len(mapped_neighbours[n])):
            if mapped_neighbours[n][i] not in neighbours[n]:

                # 1
                if mapped_data[mapped_neighbours[n][i][0], 0] > 1:
                    mapped_neighbours[n][i][1] = -1
                else:
                    mapped_neighbours[n][i][1] = 1

                # 2
                if not [n, -mapped_neighbours[n][i][1]] in neighbours[mapped_neighbours[n][i][0]]:
                    neighbours[mapped_neighbours[n][i][0]].append([n, -mapped_neighbours[n][i][1]])

        neighbours[n] = mapped_neighbours[n]
#     print(f'after:  {sorted(neighbours[n], key=lambda j: j[0])}\n')

check = 0
to_delete = []
for n in range(N):
    for i in range(len(neighbours[n])):
        if [n, -neighbours[n][i][1]] not in neighbours[neighbours[n][i][0]]:
            check += 1
            to_delete.append([n, i])

for i in to_delete:
    del neighbours[i[0]][i[1]]

# s = []
# for n in range(N // 3):
#     s += list(np.random.randint(-1, 2, 3))
# s += list(np.random.randint(-1, 2, N % 3))
data[:, 2] = np.random.randint(-1, 2, N)  # источник/сток/ничего
# for_data_2 = [1]*10 + [-1]*10 + [0]*(N - 20)
# np.random.shuffle(for_data_2)
# data[:, 2] = for_data_2
# data[:, 2] = [0, -1, 1, 0, 0, -1, -1, -1, 0, -1, 0, 0, 1, -1, 1, -1, 0, 0, 0, -1, -1, 1, 1, 1, 0, 1, -1, -1, 0, -1, 1,
#               -1, 0, -1, 0, 1, 0, -1, -1, 0, 0, 0, -1, 0, -1, 0, 1, 0, 0]
# data[:, 2] = list(np.random.choice([1, -1], 7)) + [0]*7 + list(np.random.choice([1, -1], 7)) + [0]*7 + list(np.random.choice([1, -1], 7)) \
#              + [0]*7 + list(np.random.choice([1, -1], 7))
# data[:, 2] = np.random.randint(-1, 2, N) + [0]*7 + [-1]*7 + [0]*7 + [1]*7 + [0]*7 + [-1]*7

# data[:, 2] = [1, 1, 0, 1, 0, -1, -1, -1, -1, 0, -1, 0, 1, 1, 1, 1, 0, 1, 0, -1, -1, -1, -1, 0, -1, 0, 1, 1, 1, 1, 0, 1, 0,
# -1, -1, -1, -1, 0, -1, 0, 1, 1, 1, 1, 0, 1, 0, -1, -1]

# data[:, 2] = [-1, -1, 0, 1, -1, 1, 1, 0, 0, 0, 1, -1, -1, 0, -1, 1, 1, -1, 1, 1, 1, 0, 0, -1, -1, -1, 1, 1, 0, 0, -1,
#  -1, 1, 0, 0, 1, -1, 0, 0, 0, 0, 0, 1, 1, 1, -1, 0, 1, 0]



for n in range(N):
    data[n, 4] = sorted(neighbours[n], key=lambda j: j[0])
    data[n, 3] = len(data[n, 4])


# настройка data вручную

def status_change(point_number, value):
    data[point_number, 2] = value


def add_neighbour(n1, n2, period=0):
    data[n1, 3] += 1
    data[n2, 3] += 1
    data[n1, 4] = sorted(np.vstack((data[n1, 4], [n2, period])), key=lambda j: j[0])
    data[n2, 4] = sorted(np.vstack((data[n2, 4], [n1, -period])), key=lambda j: j[0])


def del_neighbour(n1, n2):
    data[n1, 3] -= 1
    data[n2, 3] -= 1
    data[n1, 4] = np.delete(data[n1, 4], [neib[0] for neib in data[n1, 4]].index(n2), 0)
    data[n2, 4] = np.delete(data[n2, 4], [neib[0] for neib in data[n2, 4]].index(n1), 0)


# np.random.seed(6)
# del_neighbour(48, 43)
# add_neighbour(43, 48, 1)
# status_change(10, -1)
# status_change(11, -1)










































































































































































































































































































































































# np.random.seed(0)
# del_neighbour(1, 4)
# del_neighbour(1, 5)
# del_neighbour(42, 46)
# status_change(17, 1)


