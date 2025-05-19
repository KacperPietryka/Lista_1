from scipy.integrate import solve_ivp
import numpy
from matplotlib import pyplot
import sys
import argparse
import networkx
import imageio.v2 as im
import random

y0 = []
t_span = (0, 100)
t_eval = numpy.linspace(0, 100, 100)

def task_1():
    if len(sys.argv) != 8:
        S0 = 999
        E0 = 1
        I0 = 0
        R0 = 0
        beta = 1.34 # im wieksza wartosc, tym szybciej choroba sie rozprzestrzenia
        sigma = 2.2 # tempo inkubacji
        gamma = 0.14 # czas potrzebny do wyzdrowienia
        N = 1000
        y0 = [S0, E0, I0, R0]
    else:
        for i in sys.argv:
            y0.append(i)
    solution = solve_ivp(fun_SEIR, t_span, y0, args = (beta, sigma, gamma, N), t_eval=t_eval)
    return solution

param_sets = [
    (999, 1, 0, 0, 1.34, 2.2, 0.14),
    (950, 30, 10, 10, 1.5, 2.0, 2),
    (990, 5, 3, 2, 0.2, 1.8, 0.10),
    (400, 550, 30, 20, 2.0, 2.5, 0.15),
    (800, 100, 50, 50, 2.5, 1.5, 0.20),
    (700, 150, 100, 50, 1.8, 2.8, 0.25),
    (990, 5, 3, 2, 8, 1.2, 0.05),
    (995, 2, 2, 1, 1.7, 7.0, 0.01),
    (980, 10, 5, 5, 1.6, 1.6, 4),
]

def task_2():
    parser = argparse.ArgumentParser(description="Parametry opcjonalne")
    parser.add_argument('-S0', '--S0',  type = int, help="Parameter S0", default=999)
    parser.add_argument('-E0', '--E0', type = int, help="Parameter E0", default=1)
    parser.add_argument('-I0', '--I0', type = int, help="Parameter I0", default=0)
    parser.add_argument('-R0', '--R0', type = int, help="Parameter R0", default=0)
    parser.add_argument('-N', '--N', type = int, help="Parameter N", default=1000)

    parser.add_argument('-beta', '--BETA', type = int, help="Parameter beta", default=1.34)
    parser.add_argument('-sigma', '--SIGMA', type = int, help="Parameter S0", default=2.2)
    parser.add_argument('-gamma', '--GAMMA', type = int, help="Parameter S0", default=0.14)
    args = parser.parse_args()
    y0 = [args.S0, args.E0, args.I0, args.R0]
    solution = solve_ivp(fun_SEIR, t_span, y0, args = (args.BETA, args.SIGMA, args.GAMMA, args.N), t_eval=t_eval)
    return solution

def fun_SEIR(t, y, beta, sigma, gamma, N):
    S, E, I, R = y
    ds_dt = -beta * S * I / N
    de_dt = beta * S * I / N - sigma * E
    di_dt = sigma * E - gamma * I
    dr_dt = gamma * I
    return [ds_dt, de_dt, di_dt, dr_dt]

def graph(nodes = 20, prob = 0.5):
    G = networkx.erdos_renyi_graph(nodes, prob)
    layout = networkx.spring_layout(G, seed=0)
    travel = random.randint(0, nodes)
    gif_path = 'Graph.gif'

    for i in range (25):
        for node in G.nodes:
            G.nodes[node]['color'] = 'red'
        G.nodes[travel]['color'] = 'green'
        # color variable
        colors = [G.nodes[n]['color'] for n in G.nodes]
        pyplot.figure()
        networkx.draw(G, with_labels=True, pos = layout, node_color=colors)
        pyplot.savefig(f'graph{i}.jpg')
        pyplot.close()

        bordering = list(G.neighbors(travel))

        len_ = len(bordering)
        if len_ == 0:
            print('Brak polaczen')
            break

        travel_index = random.randint(0, len_ - 1)
        travel = bordering[travel_index]
       
        
    frames = [im.imread(f'graph{x}.jpg') for x in range(25)]
    im.mimsave(gif_path, frames, duration=0.9)

# task 1
tables = []
tables.append(task_1())
tables.append(task_2())

graph()

def drawing(index):
    S, E, I, R = solution.y
    pyplot.plot(solution.t, S, label = "Suspectible")
    pyplot.plot(solution.t, E, label = "Exposed")
    pyplot.plot(solution.t, I, label = "Infectious")
    pyplot.plot(solution.t, R, label = "Recovered")
    pyplot.xlabel('Time')
    pyplot.ylabel('People')
    pyplot.legend()
    pyplot.savefig(f'table{index}.png')
    pyplot.close()

ind = 0

for solution in tables:
    drawing(ind)
    ind+=1

for index, (S0, E0, I0, R0, beta, sigma, gamma) in enumerate(param_sets, start=1):
    N = S0 + E0 + I0 + R0
    y0 = [S0, E0, I0, R0]
    solution = solve_ivp(fun_SEIR, t_span, y0, args=(beta, sigma, gamma, N), t_eval=t_eval)
    drawing(ind)
    ind+=1


