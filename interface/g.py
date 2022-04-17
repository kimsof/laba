from tkinter import *

map_window = Tk()
map_window.title('Карта спутников')
s = 1200
map_window.geometry(f'{s}x{600}')

canvas = Canvas(map_window, width=s, height=s, highlightthickness=0)
canvas.pack()

points = ['maroon', 'darkred', 'brown', 'crimson', 'red', 'coral', 'salmon', 'darkorange', 'orange', 'khaki', 'yellow',
          'wheat', 'beige', 'lightyellow', 'lavender', 'pink', 'lightpink', 'plum', 'violet', 'hotpink', 'magenta',
          'darkmagenta', 'purple', 'indigo', 'navyblue', 'darkblue', 'blue', 'royalblue', 'lightblue', 'lightcyan',
          'azure', 'cyan', 'turquoise', 'darkturquoise', 'darkcyan', 'teal', 'darkgreen', 'green', 'lime', 'lightgreen',
          'aquamarine', 'ivory', 'lightgrey', 'silver', 'grey', 'darkgrey', 'olive']
for i in [11,17, 27]:
    print(points[i])
a = len(points)
for i in range(len(points)):
    canvas.create_rectangle(i / a * s, 0, (i + 1) / a * s, s, fill=f'{points[i]}')
    canvas.create_text(s / a * i + s / a / 2, 600 / 2, text=f'{i}')

map_window.mainloop()


