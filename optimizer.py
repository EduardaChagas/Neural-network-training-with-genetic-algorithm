from functools import reduce
from operator import add
import random
from network import Network

class Optimizer():

    def __init__(self, nn_param_choices, retain=0.25, random_select=0.1, mutate_chance=0.2):
        self.mutate_chance = mutate_chance
        self.random_select = random_select
        self.retain = retain
        self.nn_param_choices = nn_param_choices

    def create_population(self, count):

        pop = []
        for _ in range(0, count):
            # Create a random network.
            network = Network(self.nn_param_choices)
            network.create_random()

            # Add the network to our population.
            pop.append(network)

        return pop

    @staticmethod
    def fitness(network):
        return network.accuracy

    def grade(self, pop):

        summed = reduce(add, (self.fitness(network) for network in pop))
        return summed / float((len(pop)))

    def breed(self, mother, father):

        children = []
        for _ in range(2):

            child = {}

            for param in self.nn_param_choices:
                child[param] = random.choice(
                    [mother.network[param], father.network[param]]
                )

            # create a network.
            network = Network(self.nn_param_choices)
            network.create_set(child)

            # Randomly mutate some of the children.
            if self.mutate_chance > random.random():
                network = self.mutate(network)

            children.append(network)

        return children

    def mutate(self, network):

        # random param.
        mutation = random.choice(list(self.nn_param_choices.keys()))

        # mutate the params.
        network.network[mutation] = random.choice(self.nn_param_choices[mutation])

        return network

    def evolve(self, pop):

        # Get scores for each network.
        graded = [(self.fitness(network), network) for network in pop]

        # Sorting.
        graded = [x[1] for x in sorted(graded, key=lambda x: x[0], reverse=True)]

        retain_length = int(len(graded)*self.retain)

        parents = graded[:retain_length]

        # Random choice some individuals
        for individual in graded[retain_length:]:
            if self.random_select > random.random():
                parents.append(individual)

        # Now find out how many spots we have left to fill.
        parents_length = len(parents)
        desired_length = len(pop) - parents_length
        children = []


        while len(children) < desired_length:

            male = random.randint(0, parents_length-1)
            female = random.randint(0, parents_length-1)

            if male != female:
                male = parents[male]
                female = parents[female]

                babies = self.breed(male, female)

                for baby in babies:
                    if len(children) < desired_length:
                        children.append(baby)

        parents.extend(children)

        return parents
