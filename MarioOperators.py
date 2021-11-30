import autograd.numpy as anp
import numpy as np
from pymoo.core.crossover import Crossover
from pymoo.core.problem import ElementwiseProblem
from pymoo.core.sampling import Sampling
from pymoo.core.selection import Selection
from pymoo.util.display import Display
from pymoo.util.misc import random_permuations
from MarioExample import MarioExample
from pymoo.core.mutation import Mutation
import data, math




# Creates a 2d array of individuals for the population where each row represents an individual of length 3000
# Also puts numbers at the beginning of each row to signify which individual is which when evaluating their fitness
class MarioSampling(Sampling):
    def _do(self, problem, n_samples, **kwargs):
        #X = np.random.randint(7, size=(data.pop_size, data.size))
        #stack = np.arange(1, data.pop_size + 1)
        #stack = np.reshape(stack, (data.pop_size, 1))
        #final = np.hstack((stack, X))
        with open('NumpyData.npy', 'rb') as f:
            X = np.load(f)

        #X = final
        print("OG", X)
        return X


class MarioProblemDistance(ElementwiseProblem):
    
    def __init__(self):
        super().__init__(n_var=data.size, n_obj=1, xl=0, xu=6, type=anp.integer)

    def _evaluate(self, x, out, *args, **kwargs):
        #gameplay = np.delete(x, 0)
        #id = x[0]

        dist, time, death = MarioExample().playGame(x)

        data.ids[id] = death

        out["F"] = dist

class MarioMutationFurthest(Mutation):
    def __init__(self):
        super().__init__()

    def _do(self, problem, X, **kwargs):
        print ("Furthest: ", data.furthest)
         # X is the array of indivs
         # Row is indiv
         # Col is genes
        for i in range(len(X)):
            for x in range(len(X[i])):
                if x > data.furthest - 50 and x < data.furthest:
                    r = np.random.random()

                    # Add duplicate detection
                    # Current mutation chance is below
                    if r < 0.8:
                        X[i,x] = np.random.randint(0,6)
                
                # Still has a (much) smaller chance of mutating genes outside of the "death range"
                else:
                    s = np.random.random()
                    if s < .025:
                        X[i,x] = np.random.randint(0,6)

        return X

class MarioMutation(Mutation):

    def __init__(self):
        super().__init__()

    def _do(self, problem, X, **kwargs):
        x = 1

        print("Mutant", X)

        for i in range(len(X)):

            id = X[i, 0]
            dist = data.ids.get(id)
            print("Id: ", id)
            # print("I: ", i)
            print("Dist: ", dist)
            print("Indiv: ", X[i])            

            x = 1
            for x in range(len(X[i])):

                if x > dist - 25 and x <= dist:
                    r = np.random.random()

                    if r < 0.4:
                        X[i, x] = np.random.randint(0, 6)

                s = np.random.random()
                if s < .025:
                    X[i, x] = np.random.randint(0, 6)
            
            # print("New Indiv: ", X[i])

        stack = np.arange(1, data.pop_size + 1)
        stack = np.reshape(stack, (data.pop_size, 1))
        final = np.hstack((stack, X))

        print("XM", X)
        print("F", final)
        final = np.delete(final, 3001)
        print("F2", final)
        return X

# class MarioCrossover(Crossover):
    
#     def __init__(self):
#         super().__init__(2, 2)

#     def _do(self, problem, X, **kwargs):

#         return Y

class MarioSelection(Selection):
    
    def __init__(self):
        super().__init__()

    def _do(self, pop, n_select, n_parents, **kwargs):
        print("Pop", pop)

        # number of random individuals needed
        n_random = n_select * n_parents

        # number of permutations needed
        n_perms = math.ceil(n_random / len(pop))

        # get random permutations and reshape them
        P = random_permuations(n_perms, len(pop))[:n_random]

        print(np.reshape(P, (n_select, n_parents)))

        return np.reshape(P, (n_select, n_parents))