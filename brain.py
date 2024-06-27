class Brain:
    def __init__(self, multipliers = []) -> None:
        self.neurons:list[BrainWeightChangingNeuron] = []
        self.multipliers = multipliers
    
    def simulate_step(self):
        values = []
        multiplier_changes = []
        #get changes
        for neuron in self.neurons:
            values.append(neuron.calculate_value())
            multiplier_changes.append(neuron.calculate_multiplier_changes())

        #apply changes
        for neuron_index in range(len(self.neurons)):
            self.neurons[neuron_index].value = values[neuron_index]
        
        for change in multiplier_changes:
            for multi_index in range(len(change)):
                self.multipliers[multi_index] *= change[multi_index]

        

    
    #used for loading. doesn't call neuron added because it's index should already be on the other neuron's lists. 
    def add_neuron_with_data(self,weights,multipliers,value,other_neurons:list[dict]):
        neuron = BrainWeightChangingNeuron(self)
        neuron.weights = weights
        neuron.multipliers = multipliers
        neuron.value = value
        for other in other_neurons:
            n = Neuron(self)
            n.weights = other["weights"]
            n.multipliers = other["multi"]
            n.value = other["value"]
            neuron.brain_weight_changers.append(n)

        self.neurons.append(neuron)
    
    def add_neuron(self):
        self.neurons.append(BrainWeightChangingNeuron(self))

        for neuron in self.neurons:
            neuron.neuron_added()



class Neuron:
    def __init__(self, brain:Brain) -> None:
        self.weights = []
        for i in range(len(brain.neurons)):
            self.weights.append(1.0)
        
        self.multipliers = []
        for i in range(len(brain.multipliers)):
            self.multipliers.append(1.0)
        
        self.brain = brain
        self.value = 1
    
    def calculate_value(self) -> float:
        to_return = 1

        for neuron in self.brain.neurons:
            to_return *= neuron.value
        
        for multiplier_index in range(len(self.brain.multipliers)):
            to_return *= ((1-self.multipliers[multiplier_index])*(self.brain.multipliers[multiplier_index]-1))+1
        
        return to_return

    def neuron_added(self):
        self.weights.append(1.0)
        self.multipliers.append(1.0)


class BrainWeightChangingNeuron(Neuron):
    def __init__(self, brain: Brain) -> None:
        super().__init__(brain)

        self.brain_weight_changers:list[Neuron] = []
        for i in range(len(brain.multipliers)):
            self.brain_weight_changers.append(Neuron(self.brain))

    def calculate_multiplier_changes(self):
        to_return = []
        for neuron in self.brain_weight_changers:
            to_return.append(neuron.calculate_value())

        return to_return
    
    def neuron_added(self):
        super().neuron_added()
        
        for neuron in self.brain_weight_changers:
            neuron.neuron_added()