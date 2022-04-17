import numpy as np
from data_gen_new import data
from data_gen_new import N
from interface_new import make_interface


class Point:

    def __init__(self, number):
        self.number = number  # номер точки
        self.x = data[number, 0]  # х
        self.y = data[number, 1]  # у
        self.bounds = data[number, 3]  # число соседей
        self.neighbours = data[number, 4]  # соседи
        self.distances = [((data[neib[0], 0] - (data[self.number, 0] + neib[1])) ** 2 +
                           (data[neib[0], 1] - data[self.number, 1]) ** 2) ** (1 / 2) for neib in
                          self.neighbours]


    # функция для вывода информации о точке через интерфейс
    def inp(self):
        data_neighbours = ''
        for i in range(self.bounds):
            neib = self.neighbours[i][0]
            data_neighbours += f'\n{(neib, np.round(data[neib, 0], 3), np.round(data[neib, 1], 3), np.round(self.distances[i], 3), data[neib, 2])} '
        return [self.number, (np.round(self.x, 3), np.round(self.y, 3)), data_neighbours]


points = [Point(k) for k in range(N)]  # массив точек
make_interface(points)
data[1, 2] = 1
data[7, 2] = -1
data[30, 2] = 0
data[20, 2] = 0
data[25, 2] = 0
data[33, 2] = 0
data[14, 2] = 0
data[36, 2] = 1
data[40, 2] = -1
data[43, 2] = 1
