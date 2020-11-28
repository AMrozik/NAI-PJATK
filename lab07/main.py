from numpy.random import uniform, randint
from math import sin, pi
import matplotlib.pyplot as plt
import sys


class OutOfDomainException(Exception):
    def __init__(self, domain, message):
        self.domain = domain
        self.message = message


def hill_climb(get_random_sol, get_all_neighbours, goal_fun, max_iter=10, domain=(-10, 10)):
    min_d, max_d = domain
    current_solution = get_random_sol(min_d, max_d)
    iterations = []
    for iteration in range(max_iter):
        next_solutions = get_all_neighbours(current_solution)
        next_solutions.append(current_solution[:])
        current_solution = min(next_solutions, key=goal_fun)
        iterations.append(goal_fun(current_solution))
    return current_solution, iterations


def random_hill_climb(get_random_sol, get_r_neighbour, goal_fun, max_iter=10, domain=(-10, 10)):
    min_d, max_d = domain
    current_solution = get_random_sol(min_d, max_d)
    iterations = []
    for iteration in range(max_iter):
        next_sol = get_r_neighbour(current_solution)
        if goal_fun(current_solution) > goal_fun(next_sol):
            current_solution = next_sol
        iterations.append(goal_fun(current_solution))
    return current_solution, iterations


def random_sampling(get_random_sol, get_all_neighbours, goal_fun, max_iter=10, domain=(-10, 10)):
    min_d, max_d = domain
    current_solution = get_random_sol(min_d, max_d)
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
    if x > 10 or x < -10 or y > 10 or y < -10:
        raise Exception("punkt z poza dziedziny")
    return sin(3*pi*x)**2 + (x-1)**2 * (1+(sin(3*pi*y)**2)) + (y-1)**2 * (1+(sin(2*pi*y)))


def matyas_fun(vector):
    x = vector[0]
    y = vector[1]
    if x > 10 or x < -10 or y > 10 or y < -10:
        raise Exception("punkt z poza dziedziny")
    return 0.26 * (x**2 + y**2) - 0.48*x*y


def booth_fun(vector):
    x = vector[0]
    y = vector[1]
    if x > 10 or x < -10 or y > 10 or y < -10:
        raise Exception()
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


def random_neighbour(x, dx=0.001):
    ret = []
    for i in range(len(x)):
        nx = x[:]
        nx[i] += dx
        ret.append(nx[:])
        nx[i] -= 2.0 * dx
        ret.append(nx[:])
    return ret[randint(0, len(ret)-1)]


def init(min_d, max_d):
    x = [uniform(min_d, max_d), uniform(min_d, max_d)]
    return x


if __name__ == '__main__':

    if len(sys.argv) > 3:
        max_iterations = int(sys.argv[1])
        choose_goal = sys.argv[2]
        neighbour_fun = neighbours
        if choose_goal == "levi":
            goal_fun = levi_fun
        elif choose_goal == "Matyas":
            goal_fun = matyas_fun
        elif choose_goal == "Booth":
            goal_fun = booth_fun
        else:
            print("nieznany argument: ", choose_goal)
            exit(1)

        choose_opt = sys.argv[3]
        if choose_opt == "sampling":
            opt_fun = random_sampling
        elif choose_opt == "hill_climb":
            opt_fun = hill_climb
        elif choose_opt == "r_hill_climb":
            opt_fun = random_hill_climb
            neighbour_fun = random_neighbour
        else:
            print("nieznany argument: ", choose_opt)
            exit(2)

    else:
        max_iterations = int(input("podaj maksymalną liczbę iteracji: "))

        choose = int(input("Wybierz funkcje optymalizowaną:\n1: Lévi function\n2: Matyas function\n3: Booth function\n>"))

        if choose == 1:
            goal_fun = levi_fun
        elif choose == 2:
            goal_fun = matyas_fun
        elif choose == 3:
            goal_fun = booth_fun
        else:
            goal_fun = levi_fun

        choose = int(input("Wybierz funkcje optymalizacyjną:\n1: Random Sampling\n2: Random Hill Climb\n3: Hill Climb\n>"))
        neighbour_fun = neighbours

        if choose == 1:
            opt_fun = random_sampling
        elif choose == 2:
            opt_fun = random_hill_climb
            neighbour_fun = random_neighbour
        elif choose == 3:
            opt_fun = hill_climb
        else:
            opt_fun = random_sampling

    wyniki_iteracji = []

    try:
        for i in range(5):
            solution, iterations = opt_fun(init, neighbour_fun, goal_fun, max_iter=max_iterations)
            wyniki_iteracji.append(iterations)
    except Exception as ex:
        print("Przechwycono wyjątek: ", ex)
        exit(3)

    wyniki_srednie = []
    for j in range(max_iterations):
        srednia = 0
        for i in range(5):
            srednia += wyniki_iteracji[i][j]
        srednia /= 20
        wyniki_srednie.append(srednia)

    # print(wyniki_srednie)

    plt.plot(wyniki_srednie)
    plt.xlabel("liczba iteracji")
    plt.ylabel("średni wynik dla 20 testów")
    plt.show()