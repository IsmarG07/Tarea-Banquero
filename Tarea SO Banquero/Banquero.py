import tkinter as tk
from tkinter import ttk, messagebox

# Función para verificar si el estado es seguro
def is_safe_state(available, allocation, max_demand, need):
    num_processes = len(allocation)
    num_resources = len(available)
    
    work = available[:]
    finish = [False] * num_processes
    safe_sequence = []

    while len(safe_sequence) < num_processes:
        allocated_in_this_round = False
        
        for i in range(num_processes):
            if not finish[i]:
                if all(need[i][j] <= work[j] for j in range(num_resources)):
                    for j in range(num_resources):
                        work[j] += allocation[i][j]
                    finish[i] = True
                    safe_sequence.append(i)
                    allocated_in_this_round = True
        if not allocated_in_this_round:
            break
    
    if len(safe_sequence) == num_processes:
        return True, safe_sequence
    else:
        return False, []

# Función para generar las entradas dinámicamente
def generate_entries():
    try:
        num_processes = int(processes_entry.get())
        num_resources = int(resources_entry.get())
        
        if num_processes <= 0 or num_resources <= 0:
            raise ValueError
        
        # Limpiar frames anteriores
        for widget in allocation_frame.winfo_children():
            widget.destroy()
        for widget in max_demand_frame.winfo_children():
            widget.destroy()
        
        allocation_entries.clear()
        max_entries.clear()
        
        # Crear encabezados
        for r in range(num_resources):
            ttk.Label(allocation_frame, text=f"Recurso {r+1}").grid(row=0, column=r+1, padx=5, pady=5)
            ttk.Label(max_demand_frame, text=f"Recurso {r+1}").grid(row=0, column=r+1, padx=5, pady=5)
        
        # Crear entradas para cada proceso
        for i in range(num_processes):
            ttk.Label(allocation_frame, text=f"P{i+1}").grid(row=i+1, column=0, padx=5, pady=5)
            alloc_row = []
            for j in range(num_resources):
                entry = ttk.Entry(allocation_frame, width=5)
                entry.grid(row=i+1, column=j+1, padx=5, pady=5)
                alloc_row.append(entry)
            allocation_entries.append(alloc_row)
            
            ttk.Label(max_demand_frame, text=f"P{i+1}").grid(row=i+1, column=0, padx=5, pady=5)
            max_row = []
            for j in range(num_resources):
                entry = ttk.Entry(max_demand_frame, width=5)
                entry.grid(row=i+1, column=j+1, padx=5, pady=5)
                max_row.append(entry)
            max_entries.append(max_row)
        
        # Habilitar botón de ejecutar
        run_button.config(state=tk.NORMAL)
        
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa números válidos para procesos y recursos.")

# Función para ejecutar el Algoritmo del Banquero
def run_banker():
    try:
        available = [int(x) for x in available_entry.get().split()]
        num_processes = int(processes_entry.get())
        num_resources = int(resources_entry.get())
        
        if len(available) != num_resources:
            raise ValueError("El número de recursos disponibles no coincide con el especificado.")
        
        allocation = []
        max_demand = []
        
        for i in range(num_processes):
            alloc = []
            max_d = []
            for j in range(num_resources):
                a = allocation_entries[i][j].get()
                m = max_entries[i][j].get()
                alloc.append(int(a))
                max_d.append(int(m))
            allocation.append(alloc)
            max_demand.append(max_d)
        
        # Calcula la necesidad de cada proceso
        need = [[max_demand[i][j] - allocation[i][j] for j in range(num_resources)] 
                for i in range(num_processes)]
        
        # Verificar que no haya necesidades negativas
        for i in range(num_processes):
            for j in range(num_resources):
                if need[i][j] < 0:
                    raise ValueError(f"La necesidad del proceso P{i+1} para el recurso {j+1} es negativa.")
        
        safe, sequence = is_safe_state(available, allocation, max_demand, need)
        
        if safe:
            seq_str = ' -> '.join([f"P{p+1}" for p in sequence])
            messagebox.showinfo("Resultado", f"Estado seguro.\nSecuencia segura: {seq_str}")
        else:
            messagebox.showwarning("Resultado", "Estado no seguro. Posible interbloqueo.")
    
    except ValueError as ve:
        messagebox.showerror("Error", f"Entrada inválida: {ve}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Creación de ventana principal
root = tk.Tk()
root.title("Simulador del Algoritmo del Banquero")

# Configurar estilo
style = ttk.Style(root)
style.theme_use('clam')

# Frame para configuración inicial
config_frame = ttk.LabelFrame(root, text="Configuración")
config_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

ttk.Label(config_frame, text="Número de Procesos:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
processes_entry = ttk.Entry(config_frame, width=10)
processes_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(config_frame, text="Número de Recursos:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
resources_entry = ttk.Entry(config_frame, width=10)
resources_entry.grid(row=0, column=3, padx=5, pady=5)

generate_button = ttk.Button(config_frame, text="Generar Entradas", command=generate_entries)
generate_button.grid(row=0, column=4, padx=5, pady=5)

# Frame para recursos disponibles
available_frame = ttk.LabelFrame(root, text="Recursos Disponibles")
available_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

available_entry = ttk.Entry(available_frame, width=50)
available_entry.grid(row=0, column=0, padx=5, pady=5)

# Frames para asignación y demanda máxima
allocation_frame = ttk.LabelFrame(root, text="Asignación")
allocation_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

max_demand_frame = ttk.LabelFrame(root, text="Demanda Máxima")
max_demand_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

# Listas para almacenar las entradas dinámicas
allocation_entries = []
max_entries = []

# Botón para ejecutar el simulador
run_button = ttk.Button(root, text="Ejecutar Algoritmo del Banquero", command=run_banker, state=tk.DISABLED)
run_button.grid(row=4, column=0, padx=10, pady=10)

# Configurar el redimensionamiento
root.columnconfigure(0, weight=1)
for i in range(5):
    root.rowconfigure(i, weight=1)

allocation_frame.columnconfigure(0, weight=1)
max_demand_frame.columnconfigure(0, weight=1)

root.mainloop()
