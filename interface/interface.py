from tkinter import *


#  from tkinter import Canvas

def make_interface(points):
    map_window = Tk()
    map_window.title('Карта спутников')
    map_window.geometry('700x700')

    def get_info(number):
        dot_window = Toplevel(map_window)
        dot_window.title(f'Спутник № {number}')
        Label(dot_window, text='Номер').grid(row=0, column=0)
        Label(dot_window, text='Координаты').grid(row=1, column=0)
        Label(dot_window, text='Соседи').grid(row=2, column=0)
        Label(dot_window, text='Значение u').grid(row=3, column=0)
        for i in range(4):
            Label(dot_window, text=f'{points[number].inp()[i]}').grid(row=i, column=1)

    dot_buttons = []

    for i in range(len(points)):
        dot = Button(map_window, text=f'{i}', font='Arial 10', width=3, height=1,
                     command=lambda i=i: get_info(i))
        dot_buttons.append(dot)
        dot.place(relx=points[i].x, rely=points[i].y)
        if points[i].u == 1:
            dot.config(highlightbackground='pink')
        elif points[i].u == -1:
            dot.config(highlightbackground='yellow')

    def search():
        search_window = Toplevel(map_window)
        search_window.title('Поиск')
        search_number = Entry(search_window)
        search_number.pack()

        def get_entry():
            value = search_number.get()
            dot_buttons[int(value)].config(highlightbackground='red')

        button = Button(search_window, text='Найти', command=get_entry)
        button.pack()

    def exit_app():
        map_window.destroy()

    main_menu = Menu(map_window)
    map_window.config(menu=main_menu)

    actions = Menu(main_menu)
    main_menu.add_cascade(label='Действия', menu=actions)
    actions.add_command(label='Поиск по номеру', command=search)
    actions.add_command(label='Выход', command=exit_app)
    #  canvas = Canvas()
    #  canvas.pack()
    #  canvas.create_line(points[1].x, points[1].y, points[2].x, points[2].y)
    map_window.mainloop()
