
from MetroACO import MetroACO
from MetroACO_PSO import MetroACO_PSO
import os, time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pob, max_epochs, alpha, beta = 100, 100, 0.8, 0.8

path_metro = os.getcwd() + '/data_base/Metro/trasbordes.xlsx'
# Ruta de prueba.
start, final = 'Indios Verdes', 'Observatorio'
aco     = MetroACO(pd.read_excel(path_metro).values)
aco_pso = MetroACO_PSO(path_metro)

times_ACO      = []
times_ACOPSO   = []
lenghts_ACO    = []
lenghts_ACOPSO = []

for _ in range(10):
    start_time = time.time()
    ants_ACO = aco.run_ACO(pob, max_epochs, start, final, alpha, beta)
    end_time = time.time()
    execution_time = end_time - start_time
    print(execution_time)
    times_ACO.append(execution_time)
    
    best_ant    = min(ants_ACO, key=lambda x: x["Costo"])
    best_lenght = best_ant['Costo']
    lenghts_ACO.append(best_lenght)

    start_time     = time.time()
    ants_ACOPSO    = aco_pso.run_ACO_PSO(pob, max_epochs, start, final)
    end_time       = time.time()
    execution_time = end_time - start_time
    print(execution_time)
    times_ACOPSO.append(execution_time)
    
    best_ant = min(ants_ACOPSO, key=lambda x: x["Costo"])
    best_lenght = best_ant['Costo']
    lenghts_ACOPSO.append(best_lenght)
    
mean_1        = np.mean(times_ACO)
mean_vector_1 = np.full_like(times_ACO, mean_1)
mean_2        = np.mean(times_ACOPSO)
mean_vector_2 = np.full_like(times_ACOPSO, mean_2)

legend_label = ['ACO mean: ' + str(round(mean_1,2)) + ' s', 'ACO/PSO mean: ' + str(round(mean_2,2)) + ' s']
plt.figure()
plt.plot(times_ACO,     linestyle = '-' , marker = 'o', color = 'green')
plt.plot(times_ACOPSO,  linestyle = '-' , marker = 'x', color = 'blue')
plt.plot(mean_vector_1, linestyle = '--', color  = 'green')
plt.plot(mean_vector_2, linestyle = '--', color  = 'blue')

plt.ylim([0,max(times_ACOPSO) + 1])
plt.grid(visible='True')
plt.xlabel('Pruebas')
plt.ylabel('Tiempo (s)')
plt.title('Ruta de ' + start + ' a ' + final + ' usando ' + str(pob) + ' hormigas y ' + str(max_epochs) + ' iteraciones')
plt.legend(legend_label)
