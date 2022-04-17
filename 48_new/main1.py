import numpy as np
from data_gen_new import N
from data_gen_new import data
from Point1 import points
import pandas as ps
from interface_new import make_interface
# заполнение матрицы системы А для каждой точки, не являющейся стоком/источником (чтобы найти коэффициенты
# разложения лапласиана)
# points = [Point(k) for k in range(N)]  # массив точек

# data[7, 2] = 1
# print(data[0, 2], data[7, 2], data[40, 2], data[47, 2])
for i in range(N):
    points[i].u = data[i, 2]
    if points[i].u == 0:
        dx = np.zeros(points[i].bounds)
        dy = np.zeros(points[i].bounds)

        for j in range(points[i].bounds):
            dx[j] = data[points[i].neighbours[j][0], 0] - (points[i].x + points[i].neighbours[j][1])
            dy[j] = data[points[i].neighbours[j][0], 1] - points[i].y

        points[i].A = np.zeros((points[i].bounds + 1, points[i].bounds + 1))
        points[i].A[0, :] = np.ones(points[i].bounds + 1)
        points[i].A[1, 1:] = dx
        points[i].b = np.array([0, 0])

        if points[i].bounds == 2:
            points[i].A[2, 1:] = dy
            points[i].b = np.array([0, 0, 0])

        if points[i].bounds == 3:
            points[i].A[2, 1:] = dy
            points[i].A[3, 1:] = dx ** 2
            points[i].b = np.array([0, 0, 0, 2])

        if points[i].bounds == 4:
            points[i].A[2, 1:] = dy
            points[i].A[3, 1:] = dx ** 2
            points[i].A[4, 1:] = dy ** 2
            points[i].b = np.array([0, 0, 0, 2, 2])


        if points[i].bounds == 5:
            points[i].A[2, 1:] = dy
            points[i].A[3, 1:] = dx ** 2
            points[i].A[4, 1:] = dy ** 2
            points[i].A[5, 1:] = dx ** 2 * dy ** 2
            points[i].b = np.array([0, 0, 0, 2, 2, 0])
            # if np.linalg.det(points[i].A) == 0:
            #     points[i].A[2, 1:] = dy
            #     points[i].A[3, 1:] = dx ** 2
            #     points[i].A[4, 1:] = dy ** 2
            #     points[i].A[5, 1:] = dx ** 3
            #     points[i].b = np.array([0, 0, 0, 2, 2, 0, 0])

        if points[i].bounds == 6:
            points[i].A[2, 1:] = dy
            points[i].A[3, 1:] = dx ** 2
            points[i].A[4, 1:] = dy ** 2
            points[i].A[5, 1:] = dx ** 2 * dy ** 2
            points[i].A[6, 1:] = dy * dx
            points[i].b = np.array([0, 0, 0, 2, 2, 0, 0])
            # if np.linalg.det(points[i].A) == 0:
            #     points[i].A[2, 1:] = dy
            #     points[i].A[3, 1:] = dx ** 2
            #     points[i].A[4, 1:] = dy ** 2
            #     points[i].A[5, 1:] = dx ** 3
            #     points[i].A[6, 1:] = dx ** 2 * dy
            #     points[i].b = np.array([0, 0, 0, 2, 2, 0, 0])

        if points[i].bounds == 7:
            points[i].A[2, 1:] = dy
            points[i].A[3, 1:] = dx ** 2
            points[i].A[4, 1:] = dy ** 2
            points[i].A[5, 1:] = dx ** 3
            points[i].A[6, 1:] = dy ** 3
            points[i].A[7, 1:] = dx ** 4
            points[i].b = np.array([0, 0, 0, 2, 2, 0, 0, 0])

        if points[i].bounds == 8:
            points[i].A[2, 1:] = dy
            points[i].A[3, 1:] = dx ** 2
            points[i].A[4, 1:] = dy ** 2
            points[i].A[5, 1:] = dx ** 3
            points[i].A[6, 1:] = dy ** 3
            points[i].A[7, 1:] = dx ** 4
            points[i].A[8, 1:] = dy ** 4
            points[i].b = np.array([0, 0, 0, 2, 2, 0, 0, 0, 0])

        if points[i].bounds == 9:
            points[i].A[2, 1:] = dy
            points[i].A[3, 1:] = dx ** 2
            points[i].A[4, 1:] = dy ** 2
            points[i].A[5, 1:] = dx ** 3
            points[i].A[6, 1:] = dy ** 3
            points[i].A[7, 1:] = dx ** 4
            points[i].A[8, 1:] = dy ** 4
            points[i].A[9, 1:] = dx ** 5
            points[i].b = np.array([0, 0, 0, 2, 2, 0, 0, 0, 0, 0])

        if points[i].bounds == 10:
            points[i].A[2, 1:] = dy
            points[i].A[3, 1:] = dx ** 2
            points[i].A[4, 1:] = dy ** 2
            points[i].A[5, 1:] = dx ** 3
            points[i].A[6, 1:] = dy ** 3
            points[i].A[7, 1:] = dx ** 4
            points[i].A[8, 1:] = dy ** 4
            points[i].A[9, 1:] = dx ** 5
            points[i].A[10, 1:] = dy ** 5
            points[i].b = np.array([0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0])

        print(f'Number: {points[i].number} \nNeighbours: {points[i].neighbours} \nMatrix with det {np.linalg.det(points[i].A)}: \n{points[i].A}')
        points[i].alpha = np.linalg.solve(points[i].A, points[i].b)  # коэффициенты разложения лапласиана
        print(points[i].alpha)
# make_interface(points)
u0 = [point.u for point in points]

A = np.eye(N)
F = np.zeros(N)
u = u0
for point in points:
    if point.u != 1 and point.u != -1:
        # A[point.number, point.number] = 0
        for j in range(point.bounds):
            A[point.number, point.number] = point.alpha[0]
            A[point.number, point.neighbours[j][0]] = point.alpha[j + 1]
    else:
        F[point.number] = point.u

# matrix_A = ps.DataFrame(A)
# matrix_A.to_excel("matrix_A.xlsx")

A_abs = np.fabs(A)
bad_lines = 0
good_lines = 0
ist_st = 0
none = 0
for i in range(N):
    if points[i].u != 1 and points[i].u != -1:
        none += 1
        if 2*A_abs[i, i] - sum(A_abs[i]) > 0:
            good_lines += 1
            # print(i, 2*A_abs[i, i] - sum(A_abs[i]))
        else:
            bad_lines += 1
            # print(i, 2*A_abs[i, i] - sum(A_abs[i]))
    else:
        ist_st += 1

print(f'sources/drains:   {ist_st}')
print(f'nones:            {none}')
print(f'good lines:       {good_lines}')
print(f'bad lines:        {bad_lines}')

U = np.triu(A, 1)
L = np.tril(A, -1)
D = np.diag(np.diag(A))
B = np.linalg.inv(D)
I = 1000  # число итераций

for i in range(I):
    u_new = - np.dot(np.dot(B, L + U), u) + np.dot(B, F)
    u = u_new

for i in range(N):
    points[i].u = u[i]
    print((i, u[i]))

