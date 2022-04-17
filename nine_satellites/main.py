import numpy as np
from data_gen import N
from Point import Point
from interface_new import make_interface
#
points = [Point(k) for k in range(N)]  # массив точек
# #
# # I = 100  # число итераций
# # u0 = [point.u for point in points]
# # for i in range(I):
# #     u = [point.u for point in points]
# #     for point in points:
# #         if point.u != 1 and point.u != -1:
# #             point.u = -np.dot(point.alpha[1:], [u[neib[0]] for neib in point.neighbours]) / point.alpha[0]
# #
# # r = np.zeros(N)
# # for i in range(N):
# #     r[i] = points[i].u
#
# # МПИ
# points = [Point(k) for k in range(N)]  # массив точек
#
# A = np.eye(N)
# F = np.zeros(N)
# u0 = [point.u for point in points]
# u = u0
# for point in points:
#     if point.u != 1 and point.u != -1:
#         # A[point.number, point.number] = 0
#         for j in range(point.bounds):
#             A[point.number, point.number] = point.alpha[0]
#             A[point.number, point.neighbours[j][0]] = point.alpha[j + 1]
#     else:
#         F[point.number] = point.u
#
# # U = np.triu(A, 1)
# # L = np.tril(A, -1)
# # D = np.diag(np.diag(A))
# # B = np.linalg.inv(L + D)
#
# I = 2  # число итераций
# tau = 0.001
# for i in range(I):
#     # u_new = -np.dot(np.dot(B, (L+D)), u)
#     u_new = np.dot(np.eye(N) - tau*A, u) + tau*F
#     # u_new = - np.dot(np.dot(B, U), u) + np.dot(B, F)
#     u = u_new
#
# # for i in range(N):
# #     print((i, u[i], r[i], F[i]))
#
# # print(np.linalg.eig(np.eye(N)-tau*A))
# # print([points[0].neighbours[i][0] for i in range(len(points[0].neighbours))])
# #make_interface(points)
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

make_interface(points)