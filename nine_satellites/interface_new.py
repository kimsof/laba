from Point import Point
from data_gen import N
from tkinter import *


class MapWindow:

    def __init__(self, master, size, points):  # root = root
        self.root = master
        self.size = size
        self.points = points
        self.create_outlook()
        self.create_widgets()
        self.satellites = []
        self.create_satellites_and_connections()

    def create_outlook(self):
        self.root.title('Карта спутников')
        self.root.geometry(f'{self.size}x{self.size}')

    def search(self):
        self.search_window = Toplevel(self.root)
        self.search_window.title('Поиск')
        self.search_number = Entry(self.search_window)
        self.search_number.pack()

        def get_entry():
            value = self.search_number.get()
            self.satellites[int(value)].highlight()

        button = Button(self.search_window, text='Найти', command=get_entry)
        button.pack()

    def exit(self):
        self.root.destroy()

    def create_widgets(self):
        self.canvas = Canvas(self.root, bg='lightgrey', height=self.size, width=self.size)
        self.canvas.pack()
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.actions = Menu(self.menu)
        self.menu.add_cascade(label='Действия', menu=self.actions)
        self.actions.add_command(label='Поиск по номеру', command=self.search)
        self.actions.add_command(label='Выход', command=self.exit)

    def create_satellites_and_connections(self):
        for point in self.points:
            for neighbour in point.neighbours:
                if point.number < neighbour[0]:
                    Connection(self, point.number, neighbour[0])
        for point in self.points:
            self.satellites.append(Satellite(point, self))


class Satellite:
    def __init__(self, point, window):
        self.point = point
        self.window = window
        self.id = 0
        self.radius = 8
        if self.point.u == -1:
            self.colour = 'aquamarine'
        elif self.point.u == 1:
            self.colour = 'plum'
        else:
            self.colour = 'white'
        self.create_satellite()


    def get_info(self, event):
        self.id += 1
        if self.id % 2 == 0:
            self.info_window = Toplevel(self.window.root)
            self.info_window.title(f'Спутник № {self.point.number}')
            Label(self.info_window, text='Номер').grid(row=0, column=0)
            Label(self.info_window, text='Координаты').grid(row=1, column=0)
            Label(self.info_window, text='Соседи').grid(row=2, column=0)
            Label(self.info_window, text='Значение u').grid(row=3, column=0)
            for j in range(4):
                Label(self.info_window, text=f'{self.point.inp()[j]}').grid(row=j, column=1)
            for neighbour in self.point.neighbours:
                Connection(self.window, self.point.number, neighbour[0]).create_connection('red')
                Satellite(self.window.points[neighbour[0]], self.window).highlight()
            self.highlight()
        else:
            for neighbour in self.point.neighbours:
                Connection(self.window, self.point.number, neighbour[0])
                Satellite(self.window.points[neighbour[0]], self.window).create_satellite()
            self.create_satellite()


    def create_satellite(self):
        self.button = self.window.canvas.create_oval(self.point.x * self.window.size - self.radius,
                                                     self.point.y * self.window.size + self.radius,
                                                     self.point.x * self.window.size + self.radius,
                                                     self.point.y * self.window.size - self.radius, fill=self.colour,
                                                     outline='ivory')
        self.number = self.window.canvas.create_text(self.point.x * self.window.size, self.point.y * self.window.size,
                                                     text=f'{self.point.number}', font='Arial3 10', fill='black')
        self.window.canvas.tag_bind(self.button, '<Button-1>', func=self.get_info)
        self.window.canvas.tag_bind(self.number, '<Button-1>', func=self.get_info)

    def highlight(self):
        self.button = self.window.canvas.create_oval(self.point.x * self.window.size - self.radius,
                                                     self.point.y * self.window.size + self.radius,
                                                     self.point.x * self.window.size + self.radius,
                                                     self.point.y * self.window.size - self.radius, fill='red', outline='red')
        self.number = self.window.canvas.create_text(self.point.x * self.window.size, self.point.y * self.window.size,
                                                     text=f'{self.point.number}', font='Arial3 10')
        self.window.canvas.tag_bind(self.button, '<Button-1>', func=self.get_info)
        self.window.canvas.tag_bind(self.number, '<Button-1>', func=self.get_info)


class Connection:
    def __init__(self, window, n1, n2):
        self.n1 = n1
        self.n2 = n2
        self.id = 0
        self.window = window
        self.create_connection('white')

    def get_info(self, event):
        self.id += 1
        if self.id % 2 == 0:
            self.create_connection('white')
            self.window.satellites[self.n1].create_satellite()
            self.window.satellites[self.n2].create_satellite()
        else:
            self.create_connection('red')
            self.window.satellites[self.n1].highlight()
            self.window.satellites[self.n2].highlight()

    def create_connection(self, colour):
        button = self.window.canvas.create_line(self.window.points[self.n1].x * self.window.size,
                                                self.window.points[self.n1].y * self.window.size,
                                                self.window.points[self.n2].x * self.window.size,
                                                self.window.points[self.n2].y * self.window.size,
                                                fill=colour)
        self.window.canvas.tag_bind(button, '<Button-1>', func=self.get_info)


def make_interface(points):
    root = Tk()
    root.resizable(0,0)
    MapWindow(root, 700, points)
    root.mainloop()