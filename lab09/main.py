from numpy import exp, sin, cos, sqrt, pi
import random


def himmelblau_fun(vector):
    x = vector[0]
    y = vector[1]
    return pow(x * x + y - 11, 2.0) + pow(x + y * y - 7, 2)


def holder_table_fun(vector):
    x = vector[0]
    y = vector[1]
    return -abs(sin(x) * cos(y) * exp(abs(1 - sqrt(x * x + y * y) / pi)))


def decimal_converter(num):
    while num > 1:
        num /= 10
    return num


def float2bin(number, precision=16):
    whole, dec = str(number).split(".")

    whole = int(whole)
    dec = int(dec)

    res = bin(whole).lstrip("0b") + "."

    for x in range(precision):
        whole, dec = str((decimal_converter(dec)) * 2).split(".")
        dec = int(dec)
        res += whole

    return res


# 100100101 -> 123
#
# wynik = 0
# for i in licza_binarna
#     wynik = wynik * 2 +1
#
# wynik = wynik / 2**5


def bin2float(bin_number):
    dec = bin_number[:8]
    print(dec)
    frac = bin_number[-8:]

    frac_num = 0
    twos = 1

    for i in frac:
        frac_num += int(i) * (1 / (2 ** twos))
        twos += 1

    return int(dec, 2) + frac_num


def get_fitness_fun(goal_fun):
    def fitness_fun(vector):
        return 1 / (1 + goal_fun(vector))

    return fitness_fun


def genotype_to_fenotype(genotype):
    length = len(genotype)
    part1 = genotype[:length // 2]
    part2 = genotype[length // 2:]

    X = 0
    for i in part1[1:]:
        X = X * 2 + i

    X = X / (2 ** (length // 7))
    if part1[0] == 1: X = -X

    Y = 0
    for i in part2[1:]:
        Y = Y * 2 + i

    Y = Y / (2 ** (length // 7))

    if part2[0] == 1: Y = -Y

    return X, Y


def fenotype_to_genotype(X, Y):
    X = float2bin(X)
    Y = float2bin(Y)

    tab = []

    for bit in X:
        if bit != ".":
            tab.append(int(bit))

    for bit in Y:
        if bit != ".":
            tab.append(int(bit))

    return tab


def one_point_crossing(X1, X2):
    c = len(X1) // 2
    return X1[:c] + X2[c:]


def point_mutation(X1):
    r = random.randint(0, len(X1) - 1)
    # print(r)
    s = X1[r]
    if s == 0:
        s = 1
    else:
        s = 0
    X1[r] = s
    return X1


def tournament_selection(pop, k, fitness=himmelblau_fun):
    best = None
    for i in range(k):
        ind = pop[random.randint(1, len(pop)-1)]
        if best is None or (fitness(genotype_to_fenotype(ind)) > fitness(genotype_to_fenotype(best))):
            best = ind
    return best


def init_pop(n):
    pop = []
    for i in range(n):
        genotype = [random.randint(0, 1) for i in range(16)]
        pop.append(genotype)
    return pop


def GA(k=16, p=20, fitness=himmelblau_fun):
    population = init_pop(p)
    for i in range(k):
        selected = []
        for j in range(p*2):
            selected.append(tournament_selection(population, p//4, fitness=fitness))
        new_pop = [point_mutation(one_point_crossing(selected.pop(), selected.pop())) for i in range(p)]
    return max(new_pop, key=fitness)


if __name__ == '__main__':
    # DEBUG = True
    # genotype = [random.randint(0, 1) for i in range(16)]
    # if DEBUG: print(genotype)
    #
    # X, Y = genotype_to_fenotype(genotype)
    #
    # print(X)
    # print(Y)

    # X1 = [random.randint(0, 1) for i in range(16)]
    # X2 = [random.randint(0, 1) for i in range(16)]
    # print("krzyżowanie: ")
    # print("X1: ", X1)
    # print("X2: ", X2)
    # X3 = one_point_crossing(X1, X2)
    # print("po krzyżowaniu: ", X3)
    # X4 = point_mutation(X3)
    # print("po mutacji: ", X4)
    #
    # pop = [X1, X2, X3, X4]
    # print(tournament_selection(pop, 5))

    print(GA())
