import numpy as np
from data_gen import data


class Point:

    def __init__(self, number):
        self.number = number  # номер точки
        self.x = np.round(data[number, 0], 3)  # х
        self.y = np.round(data[number, 1], 3)  # у
        self.u = data[number, 2]  # значение функции u
        self.bounds = data[number, 3]  # число соседей
        self.neighbours = data[number, 4]  # соседи

        # заполнение матрицы системы А для каждой точки, не являющейся стоком/источником (чтобы найти коэффициенты
        # разложения лапласиана)
        if self.u == 0:
            dxdy = np.zeros((self.bounds, 2))
            for i in range(self.bounds):
                # print(self.neighbours)
                dxdy[i, 0] = (data[self.neighbours[i][0], 0] + self.neighbours[i][1][0]) - self.x
                dxdy[i, 1] = (data[self.neighbours[i][0], 1] + self.neighbours[i][1][1]) - self.y
            self.A = np.zeros((self.bounds + 1, self.bounds + 1))
            self.A[0, :] = np.ones(self.bounds + 1)
            self.A[1, 1:] = dxdy[:, 0]
            self.A[2, 1:] = dxdy[:, 1]
            self.A[3, 1:] = dxdy[:, 0] ** 2
            self.A[4, 1:] = dxdy[:, 1] ** 2

            if self.bounds == 4:
                self.b = np.array([0, 0, 0, 2, 2])

            if self.bounds == 5:
                self.A[5, 1:] = dxdy[:, 0] * dxdy[:, 1]
                self.b = np.array([0, 0, 0, 2, 2, 0])

            if self.bounds == 6:
                self.A[5, 1:] = dxdy[:, 0] * dxdy[:, 1]
                self.A[6, 1:] = dxdy[:, 0] ** 3 * dxdy[:, 1]  # dxdy[:, 0] ** 3
                self.b = np.array([0, 0, 0, 2, 2, 0, 0])

            if self.bounds == 7:
                self.A[5, 1:] = dxdy[:, 0] * dxdy[:, 1]
                self.A[6, 1:] = dxdy[:, 0] ** 3 * dxdy[:, 1]  # dxdy[:, 0] ** 3
                self.A[7, 1:] = dxdy[:, 0] ** 2 * dxdy[:, 1]
                self.b = np.array([0, 0, 0, 2, 2, 0, 0, 0])

            if self.bounds == 8:
                self.A[5, 1:] = dxdy[:, 0] * dxdy[:, 1]
                self.A[6, 1:] = dxdy[:, 0] ** 3 * dxdy[:, 1]  # dxdy[:, 0] ** 3
                self.A[7, 1:] = dxdy[:, 0] ** 2 * dxdy[:, 1]
                self.A[8, 1:] = dxdy[:, 0] * dxdy[:, 1] ** 2
                self.b = np.array([0, 0, 0, 2, 2, 0, 0, 0, 0])

            if self.bounds == 9:
                self.A[5, 1:] = dxdy[:, 0] * dxdy[:, 1]
                self.A[6, 1:] = dxdy[:, 0] ** 3 * dxdy[:, 1]  # dxdy[:, 0] ** 3
                self.A[7, 1:] = dxdy[:, 0] ** 2 * dxdy[:, 1]
                self.A[8, 1:] = dxdy[:, 0] * dxdy[:, 1] ** 2
                self.A[9, 1:] = dxdy[:, 1] ** 3 * dxdy[:, 0]  # dxdy[:, 1] ** 3
                self.b = np.array([0, 0, 0, 2, 2, 0, 0, 0, 0, 0])

            if self.bounds == 10:
                self.A[5, 1:] = dxdy[:, 0] * dxdy[:, 1]
                self.A[6, 1:] = dxdy[:, 0] ** 3 * dxdy[:, 1]  # dxdy[:, 0] ** 3
                self.A[7, 1:] = dxdy[:, 0] ** 2 * dxdy[:, 1]
                self.A[8, 1:] = dxdy[:, 0] * dxdy[:, 1] ** 2
                self.A[9, 1:] = dxdy[:, 1] ** 3 * dxdy[:, 0]  # dxdy[:, 1] ** 3
                self.A[10, 1:] = dxdy[:, 0] ** 2 * dxdy[:, 1] ** 2  # dxdy[:, 0] ** 4
                self.b = np.array([0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0])
            # print(f'matrix A: {self.A}, \ndet: {np.linalg.det(self.A)}')
            self.alpha = np.linalg.solve(self.A, self.b)  # коэффициенты разложения лапласиана
            # print(f'alpha: {self.alpha}, point: {self.number}')

    # функция для вывода информации о точке через интерфейс
    def inp(self):
        data_neighbours = ''
        for i in range(self.bounds):
            neib = self.neighbours[i][0]
            data_neighbours += f'\n{(neib, np.round(data[neib, 0], 3), np.round(data[neib, 1], 3), np.round(self.neighbours[i][2], 3), data[neib, 2])} '
        return [self.number, (self.x, self.y), data_neighbours, self.u]

# print(a)
