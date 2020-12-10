from numpy import exp, sin, cos, sqrt, pi
import random


def himmelblau_fun(vector):
    x = vector[0]
    y = vector[1]
    return pow(x * x + y - 11, 2.0) + pow(x + y * y - 7, 2)


def holder_table_fun(vector):
    x = vector[0]
    y = vector[1]
    return -abs(sin(x)*cos(y)*exp(abs(1 - sqrt(x*x + y*y)/pi)))


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
    # print(len(frac))
    # print(frac)

    frac_num = 0
    twos = 1

    for i in frac:
        frac_num += int(i) * (1 / (2 ** twos))
        twos += 1

    return int(dec, 2) + frac_num


def get_fitness_fun(goal_fun):

    def fitness_fun(vector):
        return 1/(1+goal_fun(vector))

    return fitness_fun


def genotype_to_fenotype(genotype):
    # part1 = genotype[0:8]
    # part2 = genotype[8:16]
    # part3 = genotype[24:32]
    # part4 = genotype[32:]
    # dec1 = ""
    # frac1 = ""
    # dec2 = ""
    # frac2 = ""
    #
    # for bit in part1:
    #     dec1 += str(bit)
    #
    # for bit in part2:
    #     frac1 += str(bit)
    #
    # X = dec1 + "." + frac1
    # if DEBUG: print(X)
    #
    # for bit in part3:
    #     dec2 += str(bit)
    #
    # for bit in part4:
    #     frac2 += str(bit)
    #
    # Y = dec2 + "." + frac2
    # if DEBUG: print(Y)
    #
    # X = bin2float(X)
    # Y = bin2float(Y)

    length = len(genotype)
    part1 = genotype[:length//2]
    part2 = genotype[length//2:]

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


if __name__ == '__main__':
    DEBUG = True
    genotype = [random.randint(0, 1) for i in range(16)]
    if DEBUG: print(genotype)

    X, Y = genotype_to_fenotype(genotype)

    print(X)
    print(Y)

    # genotype = fenotype_to_genotype(X, Y)
    # print(genotype)


    # X = bin2float(X)
    # print(X)
    # print(Y)

    # X = bin2float(X)
    # print(X)

    # number = "101.1101"
    # dec = number[:3]
    # frac = number[-4:]
    #
    # frac_num = 0
    # twos = 1
    #
    # for i in frac:
    #     frac_num += int(i) * (1/(2**twos))
    #     twos += 1

    # new_number = bin2float(number)
    # print(new_number)
    #
    # print(float2bin(new_number, 4))

