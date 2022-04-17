import numpy as np
from data_gen import data


class Point:

    def __init__(self, number):
        self.number = number  # номер точки
        self.x = data[number, 0]  # х
        self.y = data[number, 1]  # у
        self.u = data[number, 2]  # значение функции u
        self.bounds = data[number, 3]  # число соседей
        self.neighbours = data[number, 4]  # соседи
        self.distances = [((data[self.number, 0] - (data[neib[0], 0] + neib[1][0])) ** 2 +
                           (data[self.number, 1] - (data[neib[0], 1] + neib[1][1])) ** 2) ** (1 / 2) for neib in
                          self.neighbours]

        # заполнение матрицы системы А для каждой точки, не являющейся стоком/источником (чтобы найти коэффициенты
        # разложения лапласиана)
        # if self.u == 0:
        #     dx = np.zeros(self.bounds)
        #     dy = np.zeros((self.bounds,))
        #
        #     for i in range(self.bounds):
        #         dx[i] = (data[self.neighbours[i][0], 0] + self.neighbours[i][1][0]) - self.x
        #         dy[i] = (data[self.neighbours[i][0], 1] + self.neighbours[i][1][1]) - self.y
        #
        #     self.A = np.zeros((self.bounds + 1, self.bounds + 1))
        #     self.A[0, :] = np.ones(self.bounds + 1)
        #     self.A[1, 1:] = dx
        #     self.b = np.array([0, 0])
        #
        #     if self.bounds == 2:
        #         self.A[2, 1:] = dy
        #         self.b = np.array([0, 0, 0])
        #
        #     if self.bounds == 3:
        #         self.A[2, 1:] = dy
        #         self.A[3, 1:] = dx ** 2
        #         self.b = np.array([0, 0, 0, 2])
        #
        #     if self.bounds == 4:
        #         self.A[2, 1:] = dy
        #         self.A[3, 1:] = dx ** 2
        #         self.A[4, 1:] = dy ** 2
        #         self.b = np.array([0, 0, 0, 2, 2])
        #
        #     if self.bounds == 5:
        #         self.A[2, 1:] = dy
        #         self.A[3, 1:] = dx ** 2
        #         self.A[4, 1:] = dy ** 2
        #         self.A[5, 1:] = dx ** 3
        #         self.b = np.array([0, 0, 0, 2, 2, 0])
        #
        #     if self.bounds == 6:
        #         self.A[2, 1:] = dy
        #         self.A[3, 1:] = dx ** 2
        #         self.A[4, 1:] = dy ** 2
        #         self.A[5, 1:] = dx ** 3
        #         self.A[6, 1:] = dy ** 3
        #         self.b = np.array([0, 0, 0, 2, 2, 0, 0])
        #
        #     if self.bounds == 7:
        #         self.A[2, 1:] = dy
        #         self.A[3, 1:] = dx ** 2
        #         self.A[4, 1:] = dy ** 2
        #         self.A[5, 1:] = dx ** 3
        #         self.A[6, 1:] = dy ** 3
        #         self.A[7, 1:] = dx ** 4
        #         self.b = np.array([0, 0, 0, 2, 2, 0, 0, 0])
        #
        #     if self.bounds == 8:
        #         self.A[2, 1:] = dy
        #         self.A[3, 1:] = dx ** 2
        #         self.A[4, 1:] = dy ** 2
        #         self.A[5, 1:] = dx ** 3
        #         self.A[6, 1:] = dy ** 3
        #         self.A[7, 1:] = dx ** 4
        #         self.A[8, 1:] = dy ** 4
        #         self.b = np.array([0, 0, 0, 2, 2, 0, 0, 0, 0])
        #
        #     if self.bounds == 9:
        #         self.A[2, 1:] = dy
        #         self.A[3, 1:] = dx ** 2
        #         self.A[4, 1:] = dy ** 2
        #         self.A[5, 1:] = dx ** 3
        #         self.A[6, 1:] = dy ** 3
        #         self.A[7, 1:] = dx ** 4
        #         self.A[8, 1:] = dy ** 4
        #         self.A[9, 1:] = dx ** 5
        #         self.b = np.array([0, 0, 0, 2, 2, 0, 0, 0, 0, 0])
        #
        #     if self.bounds == 10:
        #         self.A[2, 1:] = dy
        #         self.A[3, 1:] = dx ** 2
        #         self.A[4, 1:] = dy ** 2
        #         self.A[5, 1:] = dx ** 3
        #         self.A[6, 1:] = dy ** 3
        #         self.A[7, 1:] = dx ** 4
        #         self.A[8, 1:] = dy ** 4
        #         self.A[9, 1:] = dx ** 5
        #         self.A[10, 1:] = dy ** 5
        #         self.b = np.array([0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0])
        #
        #     print(f'Number: {self.number} \n {self.A}')
        #
        #     self.alpha = np.linalg.solve(self.A, self.b)  # коэффициенты разложения лапласиана
        #     print(self.alpha)

    # функция для вывода информации о точке через интерфейс
    def inp(self):
        data_neighbours = ''
        for i in range(self.bounds):
            neib = self.neighbours[i][0]
            data_neighbours += f'\n{(neib, np.round(data[neib, 0], 3), np.round(data[neib, 1], 3), np.round(self.distances[i], 3), data[neib, 2])} '
        return [self.number, (np.round(self.x, 3), np.round(self.y, 3)), data_neighbours, self.u]

