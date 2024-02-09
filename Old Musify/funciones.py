import os
#import threading

######################
# ALGORITMOS PROPIOS #
######################

# Detectaremos sublistas.
def DetectarSublistas(lista=list):
    for palabra in lista:
        if type(palabra) == list:
            indexado = 0
            for valor in palabra:
                lista.insert(lista.index(palabra)+indexado, valor)
                indexado += 2
            lista.remove(palabra)

# Aquí detectaremos a qué plataforma (de las plataformas que planeo que sean compatibles) pertenece un link.
def Detector_Plataforma(link=str):
    enlace = link.split(".")
    enlace = [valor.split("/") for valor in enlace]
    DetectarSublistas(enlace)
    deteccion = 0
    for palabra in enlace:
        if palabra.upper() in ["YOUTUBE", "SPOTIFY", "TWITTER", "INSTAGRAM", "TIKTOK", "TWITCH"]:
            deteccion = 1
        if deteccion == 1:
            return palabra.upper()
    return ""

# Ahora detectaremos si en la URL introducida se nos especifica si se trata de una playlist.
def Detector_PlayList(link=str):
    enlace = link.split("/")
    enlace = [valor.split("?") for valor in enlace]
    DetectarSublistas(enlace)
    enlace = [valor.split("&") for valor in enlace]
    DetectarSublistas(enlace)
    enlace = [valor.split("=") for valor in enlace]
    DetectarSublistas(enlace)
    for elemento in enlace:
        if elemento.upper() == "PLAYLIST":
            return "PLAYLIST"
        elif elemento.upper() == "LIST":
            return "LIST"

# Aquí detectaremos los posibles errores que pueda producir el usuario rellenando los campos.
def Detector_Errores(link=str, ruta=str, tipo_descarga=str):
    error = ""
    if link.split(":")[0].lower() != "https":
        error = "Debes introducir un link."
    elif link.split("/")[2].lower() != "youtu.be" and link.split("/")[2].lower() != "www.youtube.com":
        error = "Debes introducir un link de [YouTube] específicamente."
    elif os.path.isdir(str(ruta)) == False:
        error = "Has seleccionado una carpeta que no existe."
    elif tipo_descarga.upper() not in ["AUDIO", "VIDEO"]:
        error = "Debes elegir descargar solo audio o video con audio."
    else:
        error = ""
    return error

# Este es un algoritmo que sirve para acortar los nombres de las canciones descargadas.
def Acortador_Nombres(nombre=str):
    eliminar_erratas = ["", " ", "|", "\\", "/", ":", "*", '"', "<", ">", "?"]
    eliminar_grupal = ["(OFFICIAL", "[OFFICIAL", "(VIDEOCLIP", "[VIDEOCLIP", "(ANIMATED", "[ANIMATED", "(VERTICAL", "[VERTICAL", "(CLIP", "[CLIP", "(OFICIEL", "[OFICIEL", "(MUSIC", "[MUSIC", "(LYRIC", "[LYRIC", "(HD", "[HD", "(VIDEO", "(VÍDEO", "[VIDEO", "[VÍDEO", "(360º", "[360º", "(AUDIO", "[AUDIO", "(LYRICS", "[LYRICS", "HD", "LYRIC", "LYRICS", "FULL", "WEB", "OFFICIAL", "OFICIAL", "VIDEO", "ENHANCED", "1080P", "720P", "MUSIC", "VIDEO)", "VIDEO]", "OFICIAL)", "OFICIAL]", "MOVIE)", "MOVIE]", "HD)", "HD]", "AUDIO)", "AUDIO]", "VERSION)", "VERSION]", "VISUALIZER)", "VISUALIZER]", "ANIMADO)", "ANIMADO]", "VERTICAL)", "VERTICAL]", "OFICIEL)", "OFICIEL]", "OFFICIAL)", "OFFICIAL]", "CLIP)", "CLIP]", "REMASTERED)", "REMASTERED]", "LYRICS)", "LYRICS]"]
    eliminar_solitario = ["(360º)", "[360º]", "(1080P)", "[1080P]", "(720P)", "[720P]", "(LYRIC)", "[LYRIC]", "(LYRICS)", "[LYRICS]", "(LETRA)", "[LETRA]", "(WEB)", "[WEB]", "(LETRAS)", "[LETRAS]", "(OFFICIAL)", "[OFFICIAL]", "(OFICIAL)", "[OFICIAL]", "(4K)", "[4K]", "(VISUALIZER)", "[VISUALIZER]", "(VISUALIZADOR)", "[VISUALIZADOR]", "(HD)", "[HD]"]
    nombre = nombre.split(" ")
    recordar = []
    for palabra in nombre:
        if palabra.upper() in eliminar_erratas or palabra.upper() in eliminar_solitario:
            recordar.append(palabra)
        elif palabra.upper() in eliminar_grupal:
            recordar.append(palabra)
    if len(recordar) >= 2:
        for palabra in recordar:
            nombre.remove(palabra)

    nombre2 = []
    for palabra in nombre:
        nombre2.append([])
        for letra in palabra:
            if letra in eliminar_erratas:
                pass
            else:
                nombre2[-1].append(letra)

    palabras_nombre2 = []
    for lista in nombre2:
        palabras_nombre2.append("".join(lista))
    nombre = " ".join(palabras_nombre2)
    return nombre
