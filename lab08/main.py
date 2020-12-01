
# parametry:
# funkcja oceny
# funkcja dekodujaca


# populacja := generuj_populacje początkową_rozmiaru(n)
# oceń(populacja)

# powtarzaj( !warunek_zakonczenia(populacja) )
#     populacja_rodziców = selekcja(populacja)      #selekcja nie wybiera tylko najlepszych
#     populacja_potomków = krzyżowanie(populacja_rodziców)
#     populacja_potomków = mutacja(populacja_potomkow)
#     oceń(populacja_potomkow)
#     populacja = populacja_potomkow

# zwracamy najlepszego, albo całą populacje

from numpy.random import uniform


class specimen:
    def __init__(self, n):
        self.chromosome = [0] * n
        self.fit = -1

    def randomize(self):
        for i in range(len(self.chromosome)):
            self.chromosome[i] = round(uniform(), 3)


def fitness(genotype):

    # decode
    # fenotyp = decode(genotyp)
    # calculate = fitness(fenotyp)

    s = 0
    for e in genotype.chromosome:
        s += e
    return s


def calculate_pop_fitness(population):
    ret = []
    for e in population:
        e.fit = fitness(e)
        ret.append(e)
    return ret


def generate_init_pop(chromosome_size):
    ret = []
    for i in range(10):
        spec = specimen(chromosome_size)
        spec.randomize()
        print(spec.chromosome)
        ret.append(spec)
        # print(ret[i].chromosome)
    return ret


def get_term_condition_iterations(iterations_max):

    def term_condition():
        nonlocal iterations_max
        iterations_max -= 1
        # print("iterations to go ", iterations_max)
        if iterations_max > 0: return True
        return False
    return term_condition


def selection(population):
    return population


def crossover(population):
    return population


def mutation(population):
    return population


def genetic_algorithm(calculate_pop_fitness, generate_init_pop, stop_condition, selection, crossover, mutation):
    population = generate_init_pop(8)       # lista / vector
    population = calculate_pop_fitness(population)
    while stop_condition():
        # for e in population:
        #     print(e.chromosome)
        parents = selection(population)
        offspring = crossover(parents)
        offspring = mutation(offspring)
        population = calculate_pop_fitness(offspring)
    return population


if __name__ == '__main__':
    ret = genetic_algorithm(calculate_pop_fitness, generate_init_pop, get_term_condition_iterations(20), selection, crossover, mutation)
