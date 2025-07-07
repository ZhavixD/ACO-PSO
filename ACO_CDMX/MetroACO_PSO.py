import numpy as np
import pandas as pd
from MetroACO import MetroACO
from pso import ParticleSwarmOptimizer

class MetroACO_PSO:
    def __init__(self, transfers_file):
        """
        transfers (dataframe): In this case, we obtain the data related to the transfers
        final_statios (list): Final stations allow us to know if there is any other option, 
                            helping to avoid convergence problems
        route_table (dictionary): It is an essential table for consulting the information 
                            that is being obtained in each iteration.
        """
        self.transfers = pd.read_excel(transfers_file).values
            
    def run_ACO_PSO(self, pob, max_epochs, start, final):
        # PSO parameters
        num_particles = 50
        num_iterations = 50
        var_min = 0
        var_max = 1
        variables = 2        
        for epoch in range(max_epochs):
            print(f'\rExecuting the epoch {(epoch + 1):04} of {(max_epochs):04}...', end='')
            if(epoch == 0):
                beta, alpha = np.random.rand(2)                
            
            metro = MetroACO(self.transfers)
            ants = metro.run_ACO(pob, max_epochs, start, final, alpha, beta)                            
            cost = min(ants, key=lambda x: x["Costo"])['Costo']
            if epoch == 0:
                initial_cost = cost
                current_cost = np.inf    
            else:
                current_cost = cost
            
            optimizer = ParticleSwarmOptimizer(num_particles, num_iterations, var_min, var_max, variables, initial_cost, current_cost)
            optimizer.optimize()
            beta, alpha = optimizer.get_best_position() 
        cost = min(ants, key=lambda x: x["Costo"])
        print(f"\n{cost['Costo']}")
        return ants
