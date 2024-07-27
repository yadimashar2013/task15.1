
import random

# Количество особей в каждом поколении
POPULATION_SIZE = 100

# Валидные гены
GENES = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP
QRSTUVWXYZ 1234567890, .-;:_!"#%&/()=?@${[]}'''

# Измененная целевая строка для генерации
TARGET = "In finem erat Verbum"


class Individual(object):
    '''
    Класс, представляющий отдельную особь (индивида) в популяции
    '''

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.cal_fitness()

    @classmethod
    def mutated_genes(self):
        '''
        Создаем случайные гены для мутации
        '''
        global GENES
        gene = random.choice(GENES)
        return gene

    @classmethod
    def create_gnome(self):
        '''
        Создаем хромосому или набор генов
        '''
        global TARGET
        gnome_len = len(TARGET)
        return [self.mutated_genes() for _ in range(gnome_len)]

    def gene_transfer(self, par2):
        '''
        Передаем гены новому поколению индивидов
        '''

        child_chromosome = []
        for gp1, gp2 in zip(self.chromosome, par2.chromosome):

            prob = random.random()

            # если вероятность меньше 0,45, берем ген
            # от родителя 1
            if prob < 0.45:
                child_chromosome.append(gp1)

            # если вероятность между 0.45 и 0.90, берем
            # ген от родителя 2
            elif prob < 0.90:
                child_chromosome.append(gp2)

            # в противном случае берем случайный ген (мутация),
            else:
                child_chromosome.append(self.mutated_genes())

        return Individual(child_chromosome)

    def cal_fitness(self):
        '''
        Рассчитываем показатель соответствия, это количество
        символов в строке, которые отличаются от целевой
        строки.
        '''
        global TARGET
        fitness = 0
        for gs, gt in zip(self.chromosome, TARGET):
            if gs != gt: fitness += 1
        return fitness


# Driver code
def main():
    global POPULATION_SIZE

    # Текущее поколение
    generation = 1

    found = False
    population = []

    # Новое поколение
    for _ in range(POPULATION_SIZE):
        gnome = Individual.create_gnome()
        population.append(Individual(gnome))

    while not found:

        # Отсортируем популяцию в порядке возрастания оценки соответствия целевой функции
        population = sorted(population, key=lambda x: x.fitness)

        # Если у нас появился индивид, достигший целевой функции
        # цикл совершенствования можно прервать
        if population[0].fitness <= 0:
            found = True
            break

        # В противном случае - продолжаем создавать новые поколения
        new_generation = []

        # Определяем 10% популяции, наиболее соответствующих целевой фукнции
        # чтобы передать их гены будущим поколениям
        s = int((10 * POPULATION_SIZE) / 100)
        new_generation.extend(population[:s])

        s = int((90 * POPULATION_SIZE) / 100)
        for _ in range(s):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            child = parent1.gene_transfer(parent2)
            new_generation.append(child)

        population = new_generation

        print("Generation: {}\tString: {}\tFitness: {}".
              format(generation,
                     "".join(population[0].chromosome),
                     population[0].fitness))

        generation += 1

    print("Generation: {}\tString: {}\tFitness: {}".
          format(generation,
                 "".join(population[0].chromosome),
                 population[0].fitness))


if __name__ == '__main__':
    main()
