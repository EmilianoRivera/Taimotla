import pandas as pd
import json

# 1. Cargar el archivo de Excel
# Asegúrate de que el nombre del archivo sea correcto
df_excel = pd.read_excel('CatalogoColonias.xlsx') 

lista_final_para_bd = []

# 2. Iterar sobre cada columna (cada columna es un Municipio)
for municipio in df_excel.columns:
    # Tomamos la columna y quitamos los valores vacíos (NaN)
    columna_datos = df_excel[municipio].dropna()
    
    for fila in columna_datos:
        try:
            # Como tus datos vienen como "Colonia": "CP" en el Excel
            # Los tratamos como un pequeño JSON para separar llave y valor
            # Agregamos llaves {} para que json.loads lo reconozca
            dict_fila = json.loads("{" + fila + "}")
            
            for colonia, cp in dict_fila.items():
                # Guardamos la tupla (Colonia, CP, Municipio)
                lista_final_para_bd.append((colonia, cp, municipio))
        except Exception as e:
            print(f"Error procesando la fila '{fila}' en {municipio}: {e}")

print(f"Se procesaron {len(lista_final_para_bd)} colonias en total.")