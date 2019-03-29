#
# Importações
#
from tkinter import *
from copy import copy, deepcopy
import time
import random


#
# Classe Nó
#
class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent


#
# Gerar mapa com sugeira aleatório
#
def generate_map():
    map = [[None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None]]
    for i in range(4):
        for j in range(4):
            if i == 0 and j == 0:
                continue
            if random.randint(0, 2) == 1:
                map[i][j] = random.randint(0, 2)
            else:
                map[i][j] = 0
    return map


#
# Globais
#
map = generate_map()

#Mapa Manual
#map = [[0,0,0,0],
#       [0,0,0,0],
#       [0,0,0,0],
#       [0,0,0,0]]

process_map = deepcopy(map)
window_map = deepcopy(map)
list = [Node(0, 0)]
solution = [Node(0,0),Node(1,0),Node(2,0),Node(3,0),Node(3,1),Node(2,1),Node(1,1),Node(0,1),Node(0,2),Node(1,2),Node(2,2),Node(3,2),Node(3,3),Node(2,3),Node(1,3),Node(0,3)]
delay = 0.5
tile_width = 100
tile_height = 100
floor_color = "#CCCCCC"
dirt_color = "orange"
robot_color = "blue"
x = 0
y = 0
x_pos = x
y_pos = y
index_solution = 0
score = 0

#
# Verifica se o mapa está limpo
#
def map_clean():
    for i in range(len(map)):
        for j in range(len(map[i])):
            if (map[i][j] == 1):
                return False
    return True


#
# Imprimir matriz
#
def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end=" ")
        print("")


#
# Verifica se existe posição
#
def has_position(x, y):
    if (x < 0 or y < 0):
        return False
    try:
        t = map[x][y]
        return True
    except IndexError:
        return False

#
# Criar label na posicao
#
def make_label(master, x, y, h, w, *args, **kwargs):
    f = Frame(master, height=h, width=w)
    f.pack_propagate(0)  # don't shrink
    f.place(x=x, y=y)
    label = Label(f, *args, **kwargs)
    label.pack(fill=BOTH, expand=1)
    return label


#
# Window Loop
#
def run():
    global count
    global index_solution
    global label_matrix
    global delay
    global robot_color
    global floor_color
    global dirt_color
    global x_pos
    global y_pos
    global l_score
    global score
    time.sleep(delay)
    count += 0.1

    if index_solution < len(solution):
        label_matrix[x_pos][y_pos].config(bg=floor_color)
        x_pos = solution[index_solution].get_x()
        y_pos = solution[index_solution].get_y()
        label_matrix[x_pos][y_pos].config(bg=robot_color)
        index_solution += 1
        l_score.config(text=score)
        score += 1

    if count < 100:
        window.after(100, run)


#
# Algoritmo
#
for path in solution:
    print("%s %s" % (path.get_x(), path.get_y()))

window = Tk()
window.title("Inteligência Artificial - Simples")
window.geometry('500x400')

label_matrix = [[None, None, None, None],
                [None, None, None, None],
                [None, None, None, None],
                [None, None, None, None]]

# Grid
for i in range(4):
    x = 0
    for j in range(4):
        bg = floor_color
        if window_map[i][j] == 1:
            bg = dirt_color
        label_matrix[i][j] = make_label(window, x, y, tile_width, tile_height, background=bg)
        x += 100
    y += 100

# Pontos
l_score = make_label(window, 400, 0, tile_width, tile_height, background="white", text="10")
l_score.config(font=("Arial", 44))

count = 0.0
run()
window.mainloop()

#
# Main
#
if __name__ == '__main__':
    pass
