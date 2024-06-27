import sys
import brain as b
import copy

max_steps = 2
brain_amount = 3
starting_neurons = 1
multiplier_amount = 1
generations = 1
winners = 1
winner_copys = 3

def main():
    if input("try load? y/n").find("n") > -1:
        pass
    #load a file
    else:
        brains = restart()
        
    print("starting simulation")
    

    for gen in range(generations):
        print(f"Simulating gen {gen}")
        brains = generation(brains)

def generation(brains):
    fitnesses = []
    for i in range(brain_amount):
        fitnesses.append(0.0)

    steps = 0
    while steps < max_steps:
        for brain in brains:
            brain.simulate_step()
    
        #use brain neurons to calculate a simulation
        
        for brain_index in range(len(brains)):
            fitnesses[brain_index] += fitness(brains[brain_index])

        steps += 1
    
    #select fittest
    won = []
    for w in range(winners):
        won.append(brains[fitnesses.index(max(fitnesses))])
        brains.pop(fitnesses.index(max(fitnesses)))
        fitnesses.pop(fitnesses.index(max(fitnesses)))

    next_gen = []

    for w in won:
        for i in range(winner_copys):
            next_gen.append(copy.deepcopy(w))

    return next_gen


def restart():
    multipliers = []
    for i in range(multiplier_amount):
        multipliers.append(1.0)#one is the new zero

    brains:list[b.Brain] = []
    for i in range(brain_amount):
        br = b.Brain(multipliers)
        for i in range(starting_neurons):
            br.add_neuron()
        brains.append(br)
    
    return brains


#write this yourself
def fitness(brain:b.Brain) -> float:
    return 0.0

if __name__ == '__main__':
    sys.exit(main())