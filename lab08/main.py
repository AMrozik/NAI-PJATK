from numpy import exp, sin, cos, sqrt, pi

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

def float2bin(number, precision=32):
    whole, dec = str(number).split(".")

    whole = int(whole)
    dec = int(dec)

    res = bin(whole).lstrip("0b") + "."

    for x in range(precision):
        whole, dec = str((decimal_converter(dec)) * 2).split(".")
        dec = int(dec)
        res += whole

    return res


def bin2float(bin_number):
    dec = bin_number[:3]
    frac = bin_number[-4:]

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

if __name__ == '__main__':
    # ret = genetic_algorithm(calculate_pop_fitness, generate_init_pop, get_term_condition_iterations(30), selection, crossover, mutation)
    number = "101.1101"
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

