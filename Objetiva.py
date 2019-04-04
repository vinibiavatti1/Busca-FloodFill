# FURB Universidade Regional de Blumenau
# 
# Algoritmo de busca para inteligência artificial objetiva
# baseado no algoritmo de pathfinding floodfill.
# 
# Alunos:
# Vinícius Reif Biavatti
# Bryan Leite

# Importações
from tkinter import *
from copy import copy, deepcopy
import time
import random


# Classe Node. Esta classe serve para armazenar as posições
# de cada nó da matriz e também armazenar a referência para
# o nó pai. Por exemplo, dada a matriz abaixo, o caminho
# estabelecido por uma lista de nós seria:
# 1 - Agente
# 2 - Sugeira
# 
# 1, 0, 0, 0
# 0, 0, 2, 0
# 0, 0, 0, 0
# 0, 0, 0, 0
#
# Lista de nós:
# Nó 1 (x = 0, y = 0)
# Nó 2 (x = 1, y = 0, pai = Nó 1)
# Nó 3 (x = 2, y = 0, pai = Nó 2)
# Nó 4 (x = 2, y = 1, pai = Nó 3)
#
# Com isto, podemos percorrer a lista até a origem para obter
# um caminho
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


# Gerar um mapa em matriz 4x4 com sugeiras aleatórias. A chance de cada
# posição da matriz para se ter uma sugeira é de 25%. Um exemplo de retorno
# de matriz é:
# 1 - Sugeira
#
# 0, 1, 0, 0
# 0, 0, 0, 1
# 0, 0, 0, 0
# 0, 0, 1, 0
def generate_map():
    map = [[None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None]]
    for i in range(4):
        for j in range(4):
            if i == 0 and j == 0:
                map[i][j] = 0
                continue
            if random.randint(0, 1) == 1:
                map[i][j] = random.randint(0, 1)
            else:
                map[i][j] = 0
    return map

# Variáveis Globais. Abaixo segue uma coleção de variáveis utilizadas
# no algoritmo. Estas variáveis são acessadas por todos os métodos
# deste arquivo

# Mapa (Matriz 4x4)
map = generate_map()

# Mapa Manual (Matriz 4x4)
#map = [[0,0,0,0],
#       [1,0,0,1],
#       [0,1,0,0],
#       [0,0,0,1]]

# Cópia de mapa para realização da busca
process_map = deepcopy(map)

# Cópia de mapa para renderização da tela
window_map = deepcopy(map)

# Pilha utilizada para busca
list = [Node(0, 0)]

# Lista com todos os nós contendo a solução do caminho mais próximo
solution = [Node(0,0)]

# Tempo para cada movimento do agente
delay = 0.5

# Largura de cada posição da grade
tile_width = 100

# Altura de cada posição da grade
tile_height = 100

# Cores
floor_color = "#CCCCCC"
dirt_color = "orange"
robot_color = "blue"

# Variáveis para armazenar posição do agente
x = 0
y = 0
x_pos = x
y_pos = y

# Índice de interação da lista de solução
index_solution = 0

# Pontuação
score = 0

# Esta rotina verifica se o mapa (Matriz) está sem nenhuma sugeira. Caso existir
# uma sugeira, a função retorna False, senão True.
# Exemplo de retorno True da função:
#
# 0, 0, 0, 0
# 0, 0, 0, 0
# 0, 0, 0, 0
# 0, 0, 0, 0
def map_clean():
    for i in range(len(map)):
        for j in range(len(map[i])):
            if (map[i][j] == 1):
                return False
    return True


# Mostrar matriz no console. Esta função é utilizada somente para fins de
# depuração.
def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end=" ")
        print("")


# Verificar se determinada posição da matriz existe. Retorna True caso
# existir, senão False caso for uma posição inválida.
# Exemplos de retorno:
#
# has_position( 1, 2) : True
# has_position( 4, 0) : False
# has_position(-1, 2) : False
def has_position(x, y):
    if (x < 0 or y < 0):
        return False
    try:
        t = map[x][y]
        return True
    except IndexError:
        return False


# Algoritmo Floodfill
# Este algoritmo realiza a busca através de um objetivo da matriz e retorna 
# um caminho formado por Nós (Classe Node) com o caminho mais próximo até a
# sugeira mais próxima. O algoritmo utiliza uma pilha para armazenar os nós
# que precisam ser processados. Para cada nós, é obtida as posições
# adjacentes (x-1,y) (x+1,y) (x,y-1) (x,y+1). Cada um destes nós adjacentes
# recebe como pai, o nó principal que está sendo processado. Caso uma
# destas posições adjacentes possuirem uma sugeira, a função retorna este
# nó, que possui como pai o caminho para a posição do robô. Por exemplo:
# 1 - Sugeira
# 2 - Agente
# 3 - Rota
#
# Mapa
# 2, 3, 3, 0
# 0, 0, 3, 0
# 0, 0, 1, 0
# 0, 0, 0, 0
#
# Retorno:
# Nó 1 (x = 0, y = 0)
# Nó 2 (x = 1, y = 0, pai = Nó 1)
# Nó 3 (x = 2, y = 0, pai = Nó 2)
# Nó 4 (x = 2, y = 1, pai = Nó 3)
# Nó 5 (x = 2, y = 2, pai = Nó 4)
def floodfill():

    # Interação pela pilha até encontrar uma sugeira, ou percorrer a matriz por
	# inteiro
    while (len(list) != 0):
        node = list.pop(0)
        x = node.get_x()
        y = node.get_y()

        # Verifica posição X - 1, Y
        if (has_position(x - 1, y)):
            new_node = Node(x - 1, y, node)
            if (process_map[x - 1][y] == 1):
                return new_node
            if (process_map[x - 1][y] != 2):
                list.append(new_node)
                process_map[x - 1][y] = 2

        # Verifica posição X, Y - 1
        if (has_position(x, y - 1)):
            new_node = Node(x, y - 1, node)
            if (process_map[x][y - 1] == 1):
                return new_node
            if (process_map[x][y - 1] != 2):
                list.append(new_node)
                process_map[x][y - 1] = 2

        # Verifica posição X + 1, Y
        if (has_position(x + 1, y)):
            new_node = Node(x + 1, y, node)
            if (process_map[x + 1][y] == 1):
                return new_node
            if (process_map[x + 1][y] != 2):
                list.append(new_node)
                process_map[x + 1][y] = 2

        # Verifica posição X, Y + 1
        if (has_position(x, y + 1)):
            new_node = Node(x, y + 1, node)
            if (process_map[x][y + 1] == 1):
                return new_node
            if (process_map[x][y + 1] != 2):
                list.append(new_node)
                process_map[x][y + 1] = 2


# Criar label na posicao determinada com largura e altura definidas
# por parâmetro. Esta função é utilizada para renderizar a matriz
# na tela.
def make_label(master, x, y, h, w, *args, **kwargs):
    f = Frame(master, height=h, width=w)
    f.pack_propagate(0)  # don't shrink
    f.place(x=x, y=y)
    label = Label(f, *args, **kwargs)
    label.pack(fill=BOTH, expand=1)
    return label


# Loop executado pela biblioteca TKInter. Este loop renderiza o agente
# na posição da da tela conforme a lista de solução. Caso o agente
# encontrar uma sugeira, ela é limpa na tela
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


# Início da execução do algoritmo. Fluxo de execução:
#
# 1 - Realiza a busca com floodfill partindo da posição do agente
# 2 - Encontra a primeira sugeira e retorna o caminho mais curto até ela
# 3 - Adiciona este caminho na lista de solução
# 4 - Verifica se o mapa está limpo, se não estiver, executa a ação 1, 2 e 3 novamente
# 5 - Se o mapa estiver limpo, a lista de solução estará completa, então a tela será renderizada
print("Mapa")
print_matrix(map)

# Enquanto o mapa não estiver limpo, executa o algoritmo de busca
while (not map_clean()):
    path = floodfill()
    x = path.get_x()
    y = path.get_y()
	
	# Lista auxiliar utilizada somente para armazenar a solução e e reverter
    aux_list = []
	
	# Interação pelo caminho de nós até chegar na posição inicial (posição do agente)
    while (path.get_parent() is not None):
		# Destaca a posição na matriz para finds de depuração
        process_map[path.get_x()][path.get_y()] = 3
		
		# Incluir posição na lista auxiliar
        aux_list.append(path)
		
		# Obter pai
        path = path.get_parent()
		
	# Reverter lista para adicionar na lista de solução na ordem correta
    aux_list.reverse()
	
	# Adiciona na lista de solução
    solution.extend(aux_list)
	
	# Lista a sugeira
    map[x][y] = 0
	
	# Atribuir a posição nova do agente na pilha de nós
    list = [Node(x, y)]
	
	# Copia o mapa novamente com a sugeira limpa para executar o próximo processamento
    process_map = deepcopy(map)

# Mostrar Solução no console
print("")
print("Solução")
for path in solution:
    print("%s %s" % (path.get_x(), path.get_y()))

# Criar tela
window = Tk()
window.title("Inteligência Artificial - Objetiva")
window.geometry('500x400')

# Matriz de label conforme mapa 
label_matrix = [[None, None, None, None],
                [None, None, None, None],
                [None, None, None, None],
                [None, None, None, None]]

# Gerar grid com labels e cores para representar Agente ou Sugeira
for i in range(4):
    x = 0
    for j in range(4):
        bg = floor_color
        if window_map[i][j] == 1:
            bg = dirt_color
        label_matrix[i][j] = make_label(window, x, y, tile_width, tile_height, background=bg)
        x += 100
    y += 100

# Mostrar pontuação na tela
l_score = make_label(window, 400, 0, tile_width, tile_height, background="white", text="10")
l_score.config(font=("Arial", 44))

# Executar loop de processamento da tela (Método run())
count = 0.0
run()
window.mainloop()

# Main
if __name__ == '__main__':
    pass
