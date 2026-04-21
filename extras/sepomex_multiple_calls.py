import requests

# 1. Definir los valores variables (ej. IDs de usuarios)
municipios = [
            "Villaldama",
            "Vallecillo",
            "Parás",
            "Salinas Victoria",
            "Ciénega de Flores",
            "Hidalgo",
            "Abasolo",
            "Higueras",
            "General Zuazua",
            "Agualeguas",
            "General Treviño",
            "Cerralvo",
            "Melchor Ocampo",
            "García",
            "General Escobedo",
            "Santa Catarina",
            "San Pedro Garza García",
            "San Nicolás de los Garza",
            "El Carmen",
            "Apodaca",
            "Pesquería",
            "Marín",
            "Doctor González",
            "Los Ramones",
            "Los Herreras",
            "Los Aldamas",
            "Doctor Coss",
            "General Bravo",
            "China",
            "Guadalupe",
            "Juárez",
            "Santiago",
            "Allende",
            "General Terán",
            "Cadereyta Jiménez",
            "Montemorelos",
            "Rayones",
            "Linares",
            "Iturbide",
            "Galeana",
            "Hualahuises",
            "Doctor Arroyo",
            "Aramberri",
            "General Zaragoza",
            "Mier y Noriega"
        ]
base_url = "https://api.copomex.com/query/get_colonia_por_estado_municipio?token=571fc083-76a8-49d0-81cf-43a3530aad48&estado=Nuevo León&municipio={}"
results = []

# 2. Bucle para hacer cada llamada
for municipio in municipios:
    url = base_url.format(municipio)
    response = requests.get(url)
    if response.status_code == 200:
        results.append(response.json())
        print(f"Llamada exitosa para ID: {municipio}")

# 'results' contiene la información acumulada
print(results)