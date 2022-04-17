# from tkinter import *
# from tkinter import messagebox
# from data_gen import N
# from Point import Point
# import numpy as np
# 
# pi = np.pi
# tk = Tk()
# tk.title("Мое приложение")
# tk.resizable(0, 0)
# size = 700
# canvas = Canvas(tk, width=size, height=size, bg="grey", highlightthickness=0)
# canvas.pack()
# 
# points = [Point(k) for k in range(N)]
# # for point in points:
# #     canvas.create_oval(20, 20, point.x*10, point.y*10, fill="white", outline="")
# radius = 7
# canvas.create_line(points[0].x * size, points[0].y * size, points[1].x * size, points[1].y * size, fill="orange")
# a = canvas.create_oval(points[0].x * size - radius, points[0].y * size + radius, points[0].x * size + radius,
#                        points[0].y * size - radius, fill="white", outline="")
# canvas.create_oval(points[1].x * size - radius, points[1].y * size + radius, points[1].x * size + radius,
#                    points[1].y * size - radius, fill="white", outline="")
# print(points[0].x, points[0].y)
# 
# 
# def oval_func(event):
#     canvas.delete(a)
#     canvas.create_text(80, 50,
#                        text="Круг")
# 
# 
# canvas.tag_bind(a, '<Button-1>', oval_func)
# 
# # canvas.create_text(200,500,text="Hello World!", font=("Arial", 40),fill="white")
# 
# tk.mainloop()
points = ['maroon', 'darkred', 'brown', 'crimson', 'red', 'coral', 'salmon', 'darkorange', 'orange', 'khaki', 'yellow',
          'wheat', 'beige', 'lightyellow', 'lavender', 'pink', 'lightpink', 'plum', 'violet', 'hotpink', 'magenta',
          'darkmagenta', 'purple', 'indigo', 'navyblue', 'darkblue', 'blue', 'royalblue', 'lightblue', 'lightcyan',
          'azure', 'cyan', 'turquoise', 'darkturquoise', 'darkcyan', 'teal', 'darkgreen', 'green', 'lime', 'lightgreen',
          'aquamarine', 'ivory', 'lightgrey', 'silver', 'grey', 'darkgrey', 'olive']
for i in [39, 17]:
    print(points[i])