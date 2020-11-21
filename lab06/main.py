import random
from numpy.random import uniform
from math import sin, pi
import matplotlib.pyplot as plt


def hill_climb(get_random_sol, get_all_neighbours, goal_fun, max_iter):
    current_solution = get_random_sol(-5, 5)
    for iteration in range(max_iter):
        next_solutions = get_all_neighbours(current_solution)
        next_solutions.append(current_solution[:])
        current_solution = min(next_solutions, key=goal_fun)
    return current_solution


def random_sampling(goal_fun, max_iter=5, domain=(-10, 10)):
    min_d, max_d = domain
    current_solution = init(min_d, max_d)
    iterations = []
    for i in range(max_iter):
        sol = [init(min_d, max_d), current_solution[:]]
        current_solution = min(sol, key=goal_fun)
        # print(goal_fun(current_solution))
        iterations.append(goal_fun(current_solution))
    return current_solution, iterations


def sphere_fun(vector):
    sum = 0
    for x in vector:
        sum += x * x
    return sum


def himmelblau_fun(vector):
    x = vector[0]
    y = vector[1]
    return pow(x * x + y - 11, 2.0) + pow(x + y * y - 7, 2)


# # # My Functions of Choice # # #
def levi_fun(vector):
    x = vector[0]
    y = vector[1]
    return sin(3*pi*x)**2 + (x-1)**2 * (1+(sin(3*pi*y)**2)) + (y-1)**2 * (1+(sin(2*pi*y)))


def matyas_fun(vector):
    x = vector[0]
    y = vector[1]
    return 0.26 * (x**2 + y**2) - 0.48*x*y


def booth_fun(vector):
    x = vector[0]
    y = vector[1]
    return (x + 2*y - 7)**2 + (2*x + y - 5)**2


def neighbours(x, dx=0.001):
    ret = []
    for i in range(len(x)):
        nx = x[:]
        nx[i] += dx
        ret.append(nx[:])
        nx[i] -= 2.0 * dx
        ret.append(nx[:])
    return ret


def init(min_d, max_d):
    x = [uniform(min_d, max_d), uniform(min_d, max_d)]
    return x


if __name__ == '__main__':
    max_iterations = 1000
    goal_fun = levi_fun

    wyniki_iteracji = []

    for i in range(20):
        solution, iterations = random_sampling(goal_fun, max_iter=max_iterations)
        wyniki_iteracji.append(iterations)

    srednia = 0
    wyniki_srednie = []
    for j in range(max_iterations):
        for i in range(20):
            srednia += wyniki_iteracji[i][j]
        srednia /= 20
        wyniki_srednie.append(srednia)

    print(wyniki_srednie)

    plt.plot(wyniki_srednie)
    plt.xlabel("liczba iteracji")
    plt.ylabel("średni wynik dla 20 testów")
    plt.show()

    # plot_y = []
    # for i in range(20):
    #     solution = random_sampling(goal_fun)
    #     score = goal_fun(solution)
    #     plot_y.append(score)

