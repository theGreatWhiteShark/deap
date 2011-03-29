
#    This file is part of EAP.
#
#    EAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    EAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with EAP. If not, see <http://www.gnu.org/licenses/>.

import array
import random

from eap import base
from eap import creator
from eap import toolbox

IND_SIZE = 10

tools = toolbox.Toolbox()

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", array.array, fitness=creator.FitnessMin)

def update(ind, mu, std):
    for i, mu_i in enumerate(mu):
        ind[i] = random.gauss(mu_i,std)

def evalSphere(individual):
    return sum(x*x for x in individual),
                   
tools.register("individual", creator.Individual, "d",)
tools.register("update", update)
tools.register("evaluate", evalSphere)

def main():
    """Implements the One-Fifth rule algorithm as expressed in :
    Kern, S., S.D. Muller, N. Hansen, D. Buche, J. Ocenasek and P. Koumoutsakos (2004). 
    Learning Probability Distributions in Continuous Evolutionary Algorithms - 
    A Comparative Review. Natural Computing, 3(1), pp. 77-112.

    However instead of parent and offspring the algorithm is expressed in terms of
    best and worst. Best is equivalent to the parent, and worst to the offspring.
    Instead of producing a new individual each time, we have defined a function which
    updates the worst individual using the best one as the mean of the gaussian and 
    the sigma computed as the standard deviation.
    """
    random.seed(64)

    interval = (-3,7)
    mu = (random.uniform(interval[0], interval[1]) for _ in xrange(IND_SIZE))
    sigma = (interval[1] - interval[0])/2.0
    alpha = 2.0**(1.0/IND_SIZE)

    best = tools.individual(mu)
    best.fitness.values = tools.evaluate(best)
    worst = tools.individual((0.0,)*IND_SIZE)

    NGEN = 1500
    for g in xrange(NGEN):
        tools.update(worst, best, sigma) 
        worst.fitness.values = tools.evaluate(worst)
        if best.fitness <= worst.fitness:
            sigma = sigma * alpha
            best, worst = worst, best
        else:
            sigma = sigma * alpha**(-0.25)

        print "Generation", g, "- Fitness:", best.fitness.values[0]
 
    print "Best individual is ", best, best.fitness.values[0]
    
    return best
    
if __name__ == "__main__":
    main()
