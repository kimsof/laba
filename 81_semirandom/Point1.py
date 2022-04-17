import numpy as np
from data_gen_new import data
from data_gen_new import N
# from data_gen_bad import data
# from data_gen_bad import N
from interface_new import make_interface


class Point:

    def __init__(self, number):
        self.number = number  # номер точки
        self.x = data[number, 0]  # х
        self.y = data[number, 1]  # у
        self.bounds = data[number, 3]  # число соседей
        self.neighbours = data[number, 4]  # соседи
        self.calculate_distance()
        # self.distances = [self.calculate_distance(neib[0], neib[1]) for neib in self.neighbours]
        # self.distances = [((data[neib[0], 0] - (data[self.number, 0] + neib[1])) ** 2 +
        #                    (data[neib[0], 1] - data[self.number, 1]) ** 2) ** (1 / 2) for neib in
        #                   self.neighbours]

    def calculate_distance(self):
        self.distances = [((data[neib[0], 0] - (data[self.number, 0] + neib[1])) ** 2 +
                           (data[neib[0], 1] - data[self.number, 1]) ** 2) ** (1 / 2) for neib in self.neighbours]

    def add_neighbour(self, neighbour, period=0):
        neighbour.bounds += 1
        self.bounds += 1
        self.neighbours = np.vstack((self.neighbours, [neighbour.number, period]))
        neighbour.neighbours = np.vstack((neighbour.neighbours, [self.number, -period]))
        self.calculate_distance()
        neighbour.calculate_distance()

    def delete_neighbour(self, neighbour):
        neighbour.bounds -= 1
        self.bounds -= 1

        self.neighbours = np.delete(self.neighbours, [neib[0] for neib in self.neighbours].index(neighbour.number), 0)
        neighbour.neighbours = np.delete(neighbour.neighbours,
                                         [neib[0] for neib in neighbour.neighbours].index(self.number), 0)
        self.calculate_distance()
        neighbour.calculate_distance()

    # функция для вывода информации о точке через интерфейс
    def inp(self):
        data_neighbours = ''
        for i in range(self.bounds):
            neib = self.neighbours[i][0]
            data_neighbours += f'\n{(neib, np.round(data[neib, 0], 3), np.round(data[neib, 1], 3), np.round(self.distances[i], 3), data[neib, 2])} '
        return [self.number, (np.round(self.x, 3), np.round(self.y, 3)), data_neighbours]


points = [Point(k) for k in range(N)]  # массив точек
points[25].add_neighbour(points[26])
points[60].add_neighbour(points[43])
points[60].add_neighbour(points[43])
points[25].add_neighbour(points[34])
points[26].add_neighbour(points[35])
points[40].add_neighbour(points[41])
points[10].add_neighbour(points[11])
points[10].add_neighbour(points[0])
points[7].delete_neighbour(points[26])
points[20].delete_neighbour(points[28])
points[27].add_neighbour(points[28])
points[27].delete_neighbour(points[19])
points[60].add_neighbour(points[52])
points[65].add_neighbour(points[47])
points[3].add_neighbour(points[12])
points[44].delete_neighbour(points[27])

# points[60].add_neighbour(points[59])
# points[60].add_neighbour(points[69])
# points[60].delete_neighbour(points[79])

# make_interface(points)
data[1, 2] = 1
data[73, 2] = -1
data[6, 2] = -1
data[0, 2] = 1
data[2, 2] = 0
data[20, 2] = 0
data[41, 2] = 0
data[18, 2] = 1
data[56, 2] = 1
data[66, 2] = -1
data[61, 2] = -1
data[51, 2] = -1
data[15, 2] = 0
data[25, 2] = 1
data[9, 2] = -1
data[23, 2] = -1
data[60, 2] = 1
data[44, 2] = 0