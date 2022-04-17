import numpy as np

np.random.seed(100)

N = 48  # np.random.randint(100, 201)          # число спутников
q = 0.1

x = list(np.zeros(8))
for i in range(8):
    x[i] = q*(i+1)
x = x*6

y = []
for i in range(6):
    y += [q*(i+1)]*8

data = np.zeros((N, 6), dtype=object)  # массив со всей информацией
data[:, 0] = x  # np.random.random_sample((N, 2))  # x и y каждой точки
data[:, 1] = y
data[:, 2] = np.random.randint(-1, 2, N)  # источник/сток/ничего

def r(x, y):
    return ((data[x, 0] - (data[y, 0])) ** 2 +
     (data[x, 1] - data[y, 1]) ** 2) ** (1 / 2)

def y(x, z):
    return [x, array[0], r(x, z)]

neighbour = np.zeros(N, dtype=object)
array = np.array([[0, 0], [0, 0], [0, 0]])
neighbour[0] = [y(1, 0), y(8, 0)]
for i in range(1, 7):
    neighbour[i] = [y(i - 1, i), y(i + 1, i), y(i + 8, i)]
neighbour[7] = [y(6, 7), y(15, 7)]
for i in range(8, 40):
    if i % 8 == 0:
        neighbour[i] = [y(i - 8, i), y(i + 1, i), y(i + 8, i)]
    elif (i + 1) % 8 == 0:
        neighbour[i] = [y(i - 8, i), y(i - 1, i), y(i + 8, i)]
    else:
        neighbour[i] = [y(i - 8, i), y(i - 1, i), y(i + 1, i), y(i + 8, i)]
neighbour[40] = [y(32, 40), y(41, 40)]
for i in range(41, 47):
    neighbour[i] = [y(i - 1, i), y(i + 1, i), y(i - 8, i)]
neighbour[47] = [y(39, 47), y(46, 47)]

data[:, 4] = neighbour
for i in range(N):
    #print(i, neighbour[i])
    data[i, 3] = len(neighbour[i])  # число связей (соседей) каждой точки
print(sum(data[:, 3]))

# if sum(data[:, 3]) % 2 != 0:
#     data[np.argmax(data[:, 3]), 3] -= 1
#
# #array = np.array([[-1, 0], [0, 0], [1, 0]])
array = np.array([[0, 0], [0, 0], [0, 0]])


# функция, рандомно генерирующая соседей для каждой точки
def get_neighbours():
    bonds = np.zeros(N, dtype=object)
    bonds += data[:, 3]
    sorted_bonds = sorted([[i, bonds[i]] for i in range(N)], key=lambda i: i[1], reverse=True)

    keys = []
    neighbours_total = []
    for i in range(N):
        keys.append(sorted_bonds[i][0])
        neighbours_total.append([])

    while len(keys) > 0:
        n = keys[0]
        del keys[0]
        x_n = data[n, 0]
        y_n = data[n, 1]
        distances = np.zeros(N, dtype=object)

        for i in range(N):
            distance_variants = np.zeros(3)
            for j in range(3):
                distance_variants[j] = ((x_n - (data[i, 0] + array[j][0])) ** 2 +
                                        (y_n - (data[i, 1] + array[j][1])) ** 2) ** (1 / 2)
            distances[i] = [np.argmin(distance_variants), distance_variants[np.argmin(distance_variants)]]

        radius = 0
        points_in_radius = []
        while len(points_in_radius) < bonds[n]:
            for i in range(N):
                if (distances[i][1] < radius) and not (i in points_in_radius) and not (
                        i in [neib[0] for neib in neighbours_total[n]]) and (i in keys) and (i != n):
                    points_in_radius.append(i)
            radius += 0.01
            if radius > 2 ** (1 / 2):
                raise OverflowError

        neighbours = np.random.choice(points_in_radius, int(bonds[n]), False)

        neighbours_total[n] += [[neib, array[distances[neib][0]], distances[neib][1]] for neib in neighbours]

        for neib in neighbours:
            neighbours_total[neib].append([n, array[distances[neib][0]] * -1, distances[neib][1]])
            bonds[neib] -= 1
            if bonds[neib] == 0:
                del keys[keys.index(neib)]

    return neighbours_total


# не всегда функции get_neighbours() удается распределить соседей корректно для всех точек c 1 раза, поэтому:
# for i in range(100):
#     try:
#         neighbours = get_neighbours()
#         break
#     except OverflowError:
#         continue

# for i in range(N):
#     neighbours[i] = sorted(neighbours[i], key=lambda i: i[0])
#     #print(neighbours[i])

