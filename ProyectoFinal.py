import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def matrizcuadrada(matriz):
    num_columnas = len(matriz)
    for filas in matriz:
        if len(filas) != num_columnas:
            return False
    return True

def diagonal(matriz):
    for i in range(len(matriz)):
        if matriz[i][i] != 0:
            return False 
    return True

def cargarMatriz():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            matriz = leerMatriz(file_path)
            if (matrizcuadrada(matriz) and diagonal(matriz)):
                mostrarResultados(matriz)
            else:
                messagebox.showerror("Error", "La matriz no es cuadrada o su diagonal no es cero.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo: {e}")

def leerMatriz(file_path):
    matriz = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  
                matriz.append(list(map(int, line.split())))
    return matriz

def Matriz_adyacencia(matriz):
    lista_adyacencia = {}
    paises = len(matriz)
    for i in range(paises):
        lista_adyacencia[i] = set(j for j in range(paises) if matriz[i][j] == 1)
    return lista_adyacencia

def ordenarPaisesConflictos(Lista_Adyacencia):
    def merge_sort(Lista_Adyacencia):
        if len(Lista_Adyacencia) <= 1:
            return Lista_Adyacencia
        mitad = len(Lista_Adyacencia) // 2
        mitadIzq = merge_sort(Lista_Adyacencia[:mitad])
        mitadDer = merge_sort(Lista_Adyacencia[mitad:])
        return merge(mitadIzq,mitadDer)

    def merge(Izq, Der):
        ListaOrdenada = []
        i, j = 0, 0

        while i < len(Izq) and j < len(Der):
            if len(Lista_Adyacencia[Izq[i]]) > len(Lista_Adyacencia[Der[j]]):
                ListaOrdenada.append(Izq[i])
                i += 1
            else:
                ListaOrdenada.append(Der[j])
                j += 1
        ListaOrdenada.extend(Izq[i:])
        ListaOrdenada.extend(Der[j:])
        return ListaOrdenada

    keys = list(Lista_Adyacencia.keys())
    sorted_keys = merge_sort(keys)
    return sorted_keys

def AsignarVillas(ordenarPaisesConflictos, lista_adyacencia):
    villas = []

    for paises in ordenarPaisesConflictos:
        asignado = False
        for villa in villas:
            conflicto = False
            for i in range (len(villa)): 
                if villa[i] in lista_adyacencia[paises]:  
                    conflicto = True
                    break
            if not conflicto:
                villa.append(paises)  
                asignado = True
                break
        if not asignado:  
            villas.append([paises])  
    return villas


def MatrizFinal(villas, paises):
    num_villas = len(villas)
    matrizVillas = [[0] * paises for _ in range(num_villas)]
    i=0
    for villa in villas:
        for paises in villa:
            matrizVillas[i][paises] = 1
        i += 1
    return matrizVillas

def mostrarResultados(matriz):
    lista_adyacencia = Matriz_adyacencia(matriz)
    listaOrdenada = ordenarPaisesConflictos(lista_adyacencia)
    villas = AsignarVillas(listaOrdenada, lista_adyacencia)
    matrizVillas = MatrizFinal(villas, len(matriz))

    for widget in result_notebook.winfo_children():
        widget.destroy()

    resultadosView("Matriz de entrada", formatear(matriz))
    resultadosView("Lista adyacencia", formatear(lista_adyacencia))
    resultadosView("Lista ordenada", formatear(listaOrdenada))
    resultadosView("Villas", formatear(villas))
    resultadosView("Matriz final", formatear(matrizVillas))

def resultadosView(title, content):
    frame = ttk.Frame(result_notebook)
    result_notebook.add(frame, text=title)
    
    text = tk.Text(frame, wrap='word')
    text.insert('1.0', content)
    text.config(state='disabled')
    text.pack(expand=1, fill='both')

def formatear(content):
    if isinstance(content, dict):
        return "\n".join(f"{key}: {value}" for key, value in content.items())
    elif isinstance(content, list) and isinstance(content[0], list):
        return "\n".join(" ".join(map(str, row)) for row in content)
    else:
        return "\n".join(map(str, content))

# Configurar la interfaz de tkinter
root = tk.Tk()
root.title("Proyecto Final")

root.geometry("800x600")

main_frame = ttk.Frame(root)
main_frame.pack(expand=1, fill='both')

load_button = tk.Button(main_frame, text="Cargar matriz", command=cargarMatriz)
load_button.pack(pady=20)

result_notebook = ttk.Notebook(main_frame)
result_notebook.pack(expand=1, fill='both')

root.mainloop()