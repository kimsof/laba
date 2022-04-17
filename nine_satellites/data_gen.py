import numpy as np

np.random.seed(100)

N = 9  # np.random.randint(100, 201)          # число спутников
# l = 50
# yy = np.zeros(N)
# yy[:l] = np.ones(l)
# yy[:int(l/2)] = np.ones(int(l/2))
# np.random.shuffle(yy)
q = 0.1
coordinates = np.zeros((N, 2))
coordinates[0] = [0.5, 0.5]
coordinates[1] = [0.5 + q, 0.5]
coordinates[2] = [0.5, 0.5 + q]
coordinates[3] = [0.5 - q, 0.5]
coordinates[4] = [0.5, 0.5 - q]
coordinates[5] = [0.5 + 2*q, 0.5]
coordinates[6] = [0.5, 0.5 + 2*q]
coordinates[7] = [0.5 - 2*q, 0.5]
coordinates[8] = [0.5, 0.5 - 2*q]

data = np.zeros((N, 6), dtype=object)  # массив со всей информацией
data[:, :2] = coordinates  # np.random.random_sample((N, 2))  # x и y каждой точки
data[:, 2] = [0, 1, -1, 1, -1, -1, 1, 1, 1]  # np.random.randint(-1, 2, N)  # источник/сток/ничего
data[:, 3] = [N - 1, 1, 1, 1, 1, 1, 1, 1, 1]  # np.random.randint(4, 11, N)  # число связей (соседей) каждой точки
if sum(data[:, 3]) % 2 != 0:
    data[np.argmax(data[:, 3]), 3] -= 1

# array = np.array([[-1, 0], [0, 0], [1, 0]])
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
for i in range(100):
    try:
        neighbours = get_neighbours()
        break
    except OverflowError:
        continue

for i in range(N):
    neighbours[i] = sorted(neighbours[i], key=lambda i: i[0])
    #print(neighbours[i])

    data[i, 4] = neighbours[i]
    # print(i, data[i, 4])
