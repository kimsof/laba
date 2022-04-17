import numpy as np

# from data_gen_new import N
# from data_gen_new import data
from data_gen_extremely_new import data
from data_gen_extremely_new import N
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

