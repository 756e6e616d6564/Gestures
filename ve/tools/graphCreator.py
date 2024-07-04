import os
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore

def createGraph():
    folder_path = "data/Benchmark Data/hardData/"
    
    try:
        files = [file for file in os.listdir(folder_path) if file.endswith('.txt')]
        print(files, '1')
    except Exception as e:
        print("Error al listar los archivos:", e)
        return

    for file_name in files:
        try:
            file_path = os.path.join(folder_path, file_name)
            data = np.loadtxt(file_path)
            x = data[:, 1]
            y = data[:, 0]
            plt.title(file_name[:-4])
            plt.plot(x, y)
            plt.savefig(f"data/Benchmark Data/graphImages/{file_name[:-4]}.png")
            plt.clf()
            print(f"Gráfico guardado para {file_name}")
        except Exception as e:
            print(f"Error al procesar {file_name}:", e)

createGraph()
