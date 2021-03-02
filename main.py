import networkx as nx
import matplotlib.pyplot as plt
import itertools
import math

t = 10
if t<=0:
    print("Помилка: час повинен бути більше 0")
    raise SystemExit

P = [0, 0.59, 0.34, 0.15, 0.14, 0.36, 0.57, 0.89, 0.93 ,0]
len_P = len(P)
for i in P:
    if i<0 or i>1:
        print("Помилка: ймовірності повинні бути в межах від 0 до 1")
        raise SystemExit

matrix_conn = [ [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                ]

for i in range(len(matrix_conn)):
    if len(matrix_conn) != len(matrix_conn[i]):
        print("Помилка: матриця не квадратна")
        raise SystemExit
if len(matrix_conn) != len_P:
    print("Помилка: розмірність матриці та кількість введених ймовірностей не співпадають")
    raise SystemExit
for i in matrix_conn:
    for j in i:
        if j!=1 and j!=0:
            print("Помилка: значення в таблиці звязків повинні бути 0 або 1")
            raise SystemExit

G = nx.DiGraph()
for i in range(len(matrix_conn)):
    for j in range(len(matrix_conn[0])):
        if matrix_conn[i][j] == 1:
            G.add_edge(i,j)
#nx.draw_networkx(G)
#plt.show()

def find_paths(G, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not G.has_node(start):
        return []
    paths = []
    for i in G[start]:
        if i not in path:
            paths_new = find_paths(G, i, end, path)
            for path_new in paths_new:
                paths.append(path_new)
    return paths

paths = find_paths(G, 0, len(P) - 1)

print("Усі можливі шляхи (всього",len(paths),"):")
for i in paths:
    print(i[1:len(i)-1])
print("\n")

def get_working_cond(paths):
    cond = []
    for path in paths:
        tmp = path[1:len(path) - 1]
        cond.append(tmp)
    node_max = max([max(path) for path in cond])
    nodes = list(range(1, node_max + 1))
    cond.append(nodes)
    for i in cond:
        nodes_new = nodes.copy()
        i_nodes = [x for x in nodes_new if x not in i]
        for j in range(1, len(i_nodes)):
            comb_i_nodes = list(itertools.combinations(i_nodes, j))
            for k in comb_i_nodes:
                i_new = i.copy()
                i_new.extend(k)
                i_new.sort()
                if i_new not in cond:
                    cond.append(i_new)
    return sorted(cond,key=len), node_max

cond, node_max = get_working_cond(paths)

def get_P_states(cond, node_max, P):
    nodes = list(range(1, node_max + 1))
    P_states = []
    for i in cond:
        p_tmp = 1
        i_nodes = [x for x in nodes if x not in i]
        for node in i:
            p_tmp *= P[node]
        for node in i_nodes:
            tmp = 1 - P[node]
            p_tmp *= tmp
        P_states.append(round(p_tmp,6))
    return P_states

P_states = get_P_states(cond,node_max,P)
print("Працездатні стани системи та ймовірності знаходження системи у цьому стані:")
for i in range(len(cond)):
    print(cond[i],P_states[i])
print("\n")

P_sum = round(sum(P_states),6)
print("Ймовірність безвідмовної роботи протягом ",t,"годин Psystem = ",P_sum)

l = -math.log(P_sum)/t
print("Значення ітенсивності відмов λ = ",round(l,6))

T_ndv = 1/l
print("Середній наробіток до відмови Тндв = ", round(T_ndv,6))
