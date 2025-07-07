import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
import datetime, os
from MetroACO_PSO import MetroACO_PSO

path = os.getcwd()
est = []

class App_ACO:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1200x1000')
        self.root.title('Ant Colony Optimization (ACO)')
        self.root.config(bg='#FFFFFF')
        self.setup_ui()

    def obtain(self):
        return self.options.get()
    
    def aprox_time(self):
        return self.arrive_time if hasattr(self, 'arrive_time') else None

    def setup_ui(self):
        self.route = []
        self.close = ttk.Button(self.root, text='Close and Quit', command=self.quit)
        self.close.pack()

        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT)
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT)
        
        self.left_canvas = tk.Canvas(self.left_frame, width=400, height=600, bg="white")
        self.left_canvas.pack()
        self.lbl_metro = tk.Label(self.left_frame, text='Choose: ').place(x = 125, y = 25)
        self.metro_button = tk.Button(self.left_frame, text = 'Metro', width=15)
        self.metro_button.place(x = 40, y = 65)
        self.metro_button.config(command = self.load_metro)
        self.metrobus_button = tk.Button(self.left_frame, text = 'Metrobús', width=15)
        self.metrobus_button.place(x = 175, y = 65)
        self.metrobus_button.config(command = self.load_metrobus)
        self.lbl_obstacles = ttk.Label(self.left_frame, text = 'Obstacle:').place(x = 20, y = 120)
        self.obstacles = ttk.Combobox(self.left_frame, width = 15, values = est)
        self.obstacles.place(x = 100, y = 120)

        self.lbl_start = tk.Label(self.left_frame, text='Your location:').place(x = 40, y = 160)
        self.start = ttk.Combobox(self.left_frame, width = 25, values = est)
        self.start.place(x = 40, y = 190)
        self.lbl_final = ttk.Label(self.left_frame, text='Your destiny:').place(x = 40, y = 230)
        self.final = ttk.Combobox(self.left_frame, width = 25, values = est)
        self.final.place(x = 40, y = 260)
        self.lbl_ants = ttk.Label(self.left_frame, text='Ants:').place(x = 40, y = 300)
        self.ants = tk.Entry(self.left_frame, width=10)
        self.ants.place(x = 40, y = 330)
        self.lbl_epochs = ttk.Label(self.left_frame, text='Iterations:').place(x = 150, y = 300)
        self.epochs = tk.Entry(self.left_frame, width=10)
        self.epochs.place(x = 150, y = 330)

        self.bm = ttk.Button(self.left_frame, text='Start', width=20, command=self.start_aco)
        self.bm.place(x = 70, y = 370)
        self.lbl_actual_time = ttk.Label(self.left_frame, text = 'Departure time:')
        self.lbl_actual_time.place(x = 20, y = 420)
        self.lbl_arrive_time = ttk.Label(self.left_frame, text = "Arrival time:")
        self.lbl_arrive_time.place(x = 20, y = 460)
        self.lbl_time = ttk.Label(self.left_frame, text = 'Travel time:')
        self.lbl_time.place(x = 20, y = 500)
        self.directions = ttk.Button(self.left_frame, text = 'Directions', width = 20, command = self.show_route)
        self.directions.place(x = 70, y = 540)

        self.right_label = tk.Label(self.right_frame, text="Obtained routes")
        self.right_label.pack()
        self.right_canvas = tk.Canvas(self.right_frame, width=900, height=900, bg="white")
        self.right_canvas.pack()
        self.clear_button = tk.Button(self.right_frame, text='Clear', width=15, command=self.clear_canvas)
        self.clear_button.pack(side=tk.BOTTOM)  
        
    def clear_canvas(self):
        self.right_canvas.delete("all")        

    def load_metro(self):
        self.points = pd.read_excel(path + '/data_base/Metro/puntos.xlsx').values
        esta = pd.read_excel(path + '/data_base/Metro/est_metro.xlsx').values
        aux = []
        for i in range(len(esta)):
            aux.append(esta[i][0])
        
        self.stations = aux
        self.obstacles['values'] = self.stations
        self.start['values'] = self.stations
        self.final['values'] = self.stations
        self.update_map()

    def load_metrobus(self):
        self.points = pd.read_excel(path + '/data_base/Metrobus/puntos.xlsx').values
        esta = pd.read_excel(path + '/data_base/Metrobus/est_metrobus.xlsx').values
        
        aux = []
        for i in range(len(esta)):
            aux.append(esta[i][0])
        
        self.stations = aux        
        self.obstacles['values'] = self.stations
        self.start['values'] = self.stations
        self.final['values'] = self.stations
        self.update_map()
      
    def update_map(self):
        points_x = self.points[:,3]
        points_y = self.points[:,4]
        names = self.points[:,0]
        for x, y, name in zip(points_x, points_y, names):
            self.right_canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill = "black")
            self.right_canvas.create_text(x + 5, y - 5, text = name, anchor = 'nw', font=('Arial', 3))  
            
    def start_aco(self):
        self.e_start = str(self.start.get())
        self.e_final = str(self.final.get())
        self.obstaculo = str(self.obstacles.get())

        if(len(self.stations) < 200):
            self.aco = MetroACO_PSO(path + '/data_base/Metro/trasbordes.xlsx')
        elif(len(self.stations) > 200):
            self.aco = MetroACO_PSO(path + '/data_base/Metrobus/trasbordes.xlsx')
            
        pob = int(self.ants.get())
        max_epochs = int(self.epochs.get())
        self.ants_results = self.aco.run_ACO_PSO(pob, max_epochs, self.e_start, self.e_final)

        data = "Costo"
        self.valid_ants = []
        for hormiga in self.ants_results:
            route = hormiga['Trayectoria'].split(' - ')
            if self.obstaculo not in route:
                self.valid_ants.append(hormiga)
        
        aco_met = min(self.valid_ants, key=lambda x: x[data])
        self.route = aco_met['Trayectoria'].split(' - ')
        cost = aco_met[data]

        v_prom = 6.94444
        t_prom = cost/v_prom
        t_prom = t_prom/60
        t_prom = round(t_prom, 3)        
        
        actual_time = datetime.datetime.now()
        actual_time_str = actual_time.strftime("%H:%M:%S")
        minutes_to_add = datetime.timedelta(minutes=t_prom)
        self.lbl_actual_time.config(text=f"Departure time: {actual_time_str}")
        
        self.arrive_time = actual_time + minutes_to_add   
        arrive_time_str = self.arrive_time.strftime("%H:%M:%S")        
        self.lbl_arrive_time.config(text=f"Arrival time: {arrive_time_str}")
        
        travel_time = self.arrive_time - actual_time
        travel_time_seconds = travel_time.total_seconds()        
        hours = int(travel_time_seconds // 3600)
        minutes = int((travel_time_seconds % 3600) // 60)
        seconds = int(travel_time_seconds % 60)        
        travel_time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.lbl_time.config(text=f"Travel time: {travel_time_str}")
        self.root.update_idletasks()

        for h in range(len(self.valid_ants)):
            ant_route = self.valid_ants[h]['Trayectoria'].split(' - ')
            self.draw_route(ant_route, "blue", 2)            
        self.draw_route(self.route, "red", 5)
        
    def draw_route(self, route, color, tam):
        for i in range(len(route) - 1):
            estacion_actual = route[i]
            estacion_siguiente = route[i + 1]        
            indice_actual = np.where(self.points[:, 0] == estacion_actual)[0]
            indice_siguiente = np.where(self.points[:, 0] == estacion_siguiente)[0]
        
            x0, y0 = self.points[indice_actual[0], 3], self.points[indice_actual[0], 4]
            x1, y1 = self.points[indice_siguiente[0], 3], self.points[indice_siguiente[0], 4]
            self.right_canvas.create_line(x0, y0, x1, y1, fill = color, width = tam)
                   
    def show_route(self):
        self.new_root = tk.Toplevel(self.root)
        self.new_root.title('directions de la route')
        self.new_root.geometry('400x300')  
        self.frame_directions = tk.Frame(self.new_root)
        self.frame_directions.pack(fill=tk.BOTH, expand=True)  
        
        self.lista = tk.Listbox(self.frame_directions)
        self.scrollbar = tk.Scrollbar(self.frame_directions, orient=tk.VERTICAL, command=self.lista.yview)
        self.lista.config(yscrollcommand=self.scrollbar.set)
        
        for r in self.route:
            self.lista.insert(tk.END, r)
        
        self.lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) 
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  
            
    def quit(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()
