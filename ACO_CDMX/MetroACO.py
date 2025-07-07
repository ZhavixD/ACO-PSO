import numpy as np

class MetroACO:
    def __init__(self, transfers_file):
        """
        transfers (dataframe): In this case, we obtain the data related to the transfers
        final_statios (list): Final stations allow us to know if there is any other option, 
                            helping to avoid convergence problems
        route_table (dictionary): It is an essential table for consulting the information 
                            that is being obtained in each iteration.
        """
        self.transfers = transfers_file
        self.final_stations = ['Indios Verdes', 'Politécnico', 'Ciudad Azteca', 'La Paz',
                   'Constitución de 1917', 'Tláhuac', 'Tasqueña', 'Universidad',
                   'Barranca del Muerto', 'Observatorio', 'Cuatro Caminos', 'Buenavista',
                   'El Caminero', 'Tacubaya', 'Tepalcates', 'Tenayuca', 'Pueblo Santa Cruz Atoyac', 
                   'Buenavista', 'Río de los Remedios', 'Preparatoria 1', 'El Rosario', 
                   'Loreto Fabela', 'Campo Marte', 'Aeropuerto T2','Villa de Aragón']
        self.route_table = self.initialize_route_table()

    def initialize_route_table(self):
        return [
            {'Rutas': route, 
             'Feromonas': 0.001, 
             'Distancia': distance, 
             'Visibilidad': 1 / distance}
            for _, route, distance in self.transfers
        ]

    def node_options(self, node):
        options, eta, tau = zip(*[
            (b if node == a else a, route_info['Feromonas'], route_info['Visibilidad'])
            for route_info in self.route_table
            for a, b in [route_info['Rutas'].split(' - ')]
            if node in (a, b)
        ]) if any(node in r['Rutas'] for r in self.route_table) else ([], [], [])
        return list(options), list(eta), list(tau)

    def is_unique_option(self, node):
        return node in self.final_stations

    def choose(self, options, eta, tau, beta, alpha):
        tau, eta = np.array(tau), np.array(eta)
        p = (tau**beta) * (eta**alpha)
        p /= p.sum()  # Normalize probabilities
    
        cumulative = np.cumsum(p)  # Cumulative probabilities
        rng = np.random.uniform(0, 1)  # Random value
    
        # Find the first cumulative probability greater than rng
        decision_idx = np.searchsorted(cumulative, rng)
        return options[decision_idx]

    def search_distance(self, node, new_node):
        route_set = {f"{node} - {new_node}", f"{new_node} - {node}"}
        return next((r['Distancia'] for r in self.route_table if r['Rutas'] in route_set), None)

    def actualization(self, trajectory):
        rho, Q = 0.001, 1
    
        # Evaporation phase: Reduce pheromones
        for route_info in self.route_table:
            route_info['Feromonas'] *= (1 - rho)
    
        # Intensification phase: Update pheromones based on trajectory
        for trajectory_info in trajectory:
            cost = trajectory_info['Costo']
            for route in trajectory_info['Trayectoria'].split(' - '):
                for route_info in self.route_table:
                    if route_info['Rutas'] == route:
                        route_info['Feromonas'] += Q / cost

    def run_ACO(self, pob, max_epochs, start, final, alpha, beta):
        ants = [{'Costo': 0, 'Trayectoria': start} for _ in range(pob)]
        
        for h in range(pob):
            options, eta, tau = self.node_options(start)
            new_node = self.choose(options, eta, tau, beta, alpha)
            path = [start, start, new_node]

            while new_node != final:
                proposed_node = path[-1]
                previous_node = path[-3]

                if proposed_node != previous_node:
                    options, eta, tau = self.node_options(proposed_node)
                    new_node = self.choose(options, eta, tau, beta, alpha)
                    path.append(new_node)
                    preceding_node = path[-2]
                else:
                    if not self.is_unique_option(preceding_node):
                        path.pop(-1)
                        eta.pop(options.index(proposed_node))
                        tau.pop(options.index(proposed_node))
                        options.remove(proposed_node)

                        new_node = self.choose(options, eta, tau, beta, alpha)
                        path.append(new_node)
                        preceding_node = path[-2]
                    else:
                        options, eta, tau = self.node_options(proposed_node)
                        new_node = self.choose(options, eta, tau, beta, alpha)
                        path.append(new_node)
                        preceding_node = path[-2]

            for i in range(2, len(path)):
                ants[h]['Trayectoria'] = ants[h]['Trayectoria'] + ' - ' + path[i]
                dist = self.search_distance(path[i-1], path[i])
                ants[h]['Costo'] = ants[h]['Costo'] + dist

        self.actualization(ants)
        return ants
