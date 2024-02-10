import json

def crearJson(ruta=str):
    archivoJson = "MusifyData.json"
    datosJson = {"Descargados": [], "NoDescargados": []}
    with open(archivoJson, "w") as archivo:
        json.dump(datosJson, archivo)

def actualizarJson(ruta=str, descargadoAnadir=str, noDescargadoAnadir=str):
    archivoJson = "MusifyData.json"
    with open(archivoJson, "r") as archivo:
        jsonData = json.load(archivo)
    
    if descargadoAnadir != "":
        jsonData["Descargados"].append(descargadoAnadir)
    if noDescargadoAnadir != "":
        jsonData["NoDescargados"].append(noDescargadoAnadir)
    
    with open(archivoJson, "w") as archivo:
        json.dump(jsonData, archivo)

def leerJson(ruta=str):
    archivoJson = "MusifyData.json"
    with open(archivoJson, "r") as archivo:
        jsonData = json.load(archivo)
        return jsonData

crearJson("")
actualizarJson("", "JODER ME CAGO EN TU PUTA MADRE", "JODER")
print(leerJson(""))