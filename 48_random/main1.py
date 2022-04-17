import numpy as np
# from data_gen_new import N
# from data_gen_new import data
from data_gen_extremely_new import data
from data_gen_extremely_new import N
import scipy.sparse.linalg
from Point1 import points
import pandas as ps
from interface_extremely_new import make_interface


# заполнение матрицы системы А для каждой точки, не являющейся стоком/источником (чтобы найти коэффициенты
# разложения лапласиана)

def mu_counter(array):
    array_inv = np.linalg.inv(array)
    array_norm = np.linalg.norm(array)
    array_inv_norm = np.linalg.norm(array_inv)
    return array_norm * array_inv_norm


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

        if points[i].bounds == 6:
            points[i].A[2, 1:] = dy
            points[i].A[3, 1:] = dx ** 2
            points[i].A[4, 1:] = dy ** 2
            points[i].A[5, 1:] = dx ** 2 * dy ** 2
            points[i].A[6, 1:] = dy * dx
            points[i].b = np.array([0, 0, 0, 2, 2, 0, 0])

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

        # print(f'Number: {points[i].number} \nNeighbours: {points[i].neighbours} \nMatrix with det {np.linalg.det(points[i].A)}: \n{points[i].A}')
        # print(points[i].number, points[i].A.shape, len(points[i].b), points[i].b, points[i].bounds)
        points[i].alpha = np.linalg.solve(points[i].A, points[i].b)  # коэффициенты разложения лапласиана
        # points[i].mu = mu_counter(points[i].A)
        # print(f'number: {points[i].number}, mu: {points[i].mu}')
        # print(points[i].alpha)

u0 = [point.u for point in points]
# print(u0)
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
print(f'mu BEFORE of matrix A is {mu_counter(A)}')

for i in range(len(F)):
    m = A[i, i]
    A[i, :] = A[i, :] / m
    F[i] = F[i] / m

print(f'mu AFTER of matrix A is {mu_counter(A)}')
matrix_A = ps.DataFrame(A)
matrix_A.to_excel("matrix_A.xlsx")
# A_t = A.transpose()
# A_new = np.dot(A_t, A)
# A = A_new
# F = np.dot(A_t, F)

# A_abs = np.fabs(A)
# bad_lines = 0
# good_lines = 0
# ist = 0
# st = 0
# none = 0
# for i in range(N):
#     if points[i].u != 1 and points[i].u != -1:
#         none += 1
#         if 2 * A_abs[i, i] - sum(A_abs[i]) > 0:
#             good_lines += 1
#             # print(i, 2*A_abs[i, i] - sum(A_abs[i]))
#         else:
#             bad_lines += 1
#             # print(i, 2*A_abs[i, i] - sum(A_abs[i]))
#     elif points[i].u == 1:
#         ist += 1
#     else:
#         st += 1

# print(f'sources:   {ist}')
# print(f'drains:    {st}')
# print(f'nones:     {none}')
# print(f'good lines:       {good_lines}')
# print(f'bad lines:        {bad_lines}')

U = np.triu(A, 1)
L = np.tril(A, -1)
D = np.diag(np.diag(A))
B = np.linalg.inv(D)
I = 100  # число итераций

for i in range(I):
    u_new = - np.dot(np.dot(B, L + U), u) + np.dot(B, F)
    u[:] = u_new[:]
    # print(i, u)
    r = np.dot(A, u) - F
    # print(f'iteration {i}: max|r| = {np.fabs(np.amax(r))}')


bad = 0
for i in range(N):
    points[i].u = u[i]
    if u[i] > 1 or u[i] < -1:
        bad += 1
        # print((i, np.round(u[i], 3)), '                      ',
        #       [(points[i].neighbours[j][0], np.round(points[i].distances, 3)[j]) for j in range(points[i].bounds)])

aux = []
for n in range(N):
    aux.append(max(points[n].distances))

# print(f'sources:   {ist}')
# print(f'drains:    {st}')
# print(f'nones:     {none}')
# print(f'bad:       {bad}')
# print(f'max dist:  {max(aux)}')

# for i in range(N):
#     print(i, np.amax(points[i].distances))

# for i in range(N):
#     print(i, points[i].neighbours)
bicgtab_solution = scipy.sparse.linalg.bicgstab(A, F, x0=F)
simple_solution = np.linalg.solve(A, F)
gmres_solution = scipy.sparse.linalg.gmres(A, F, x0=F)
print(np.linalg.norm(bicgtab_solution[0] - np.dot(np.linalg.inv(A), F)), np.linalg.norm(np.dot(A, bicgtab_solution[0]) - F))
print(bicgtab_solution[1], gmres_solution[1])
for n in range(N):
    print(f'Satellite {n}, bic = {bicgtab_solution[0][n]}, gmres: = {gmres_solution[0][n]}')

make_interface(points)
