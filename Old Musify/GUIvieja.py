# Imports generales.
import PySimpleGUI as gui
import screeninfo, os, threading, json, time

# Importaciones de mis propias librerías.
from funciones import Detector_Plataforma
from funciones import Detector_Errores
from funciones import Detector_PlayList

from Musify_YouTube import Descargar_audio_playlist_YouTube
from Musify_YouTube import Descargar_audio_YouTube
from funciones import Detector_PlayList
from Musify_YouTube import Descargar_video_playlist_YouTube
from Musify_YouTube import Descargar_video_YouTube

# Propiedades de la interfaz gráfica.
gui.theme("Dark Grey 13") # Tema del color de la interfaz
monitor_x = screeninfo.get_monitors()[0].width # Ancho actual del monitor principal
monitor_y = screeninfo.get_monitors()[0].height # Alto del monitor principal
fuente1, fuente2, fuente3 = "Terminal", "Minecraft", "Courier" # Otra opción como fuente 3 sería "Pixellari".

# Variables del programa.

InputLinkDescarga = "Reemplaza este texto por un link." # Enlace del contenido a descargar
TextoRuta = f"{os.path.expanduser('~')}\\Desktop" # Esta es la carpeta en la que se realizarán las descargas (actualmente contiene valor por defecto)
TipoDescarga = str # Aquí se verá indicado si se descarga audio o video.
CheckFiltradoNombres = bool # Aquí se comprobará si se filtrarán los nombres de los archivos utilizando mi algoritmo.
ColorPlataforma = "#d8435a" # Aquí se ve representado el color con el que se verá el texto que muestra el nombre de la plataforma del link puesto.

# Aquí indicaremos qué elementos se mostrarán en pantalla.
interfaz1 = [[gui.Text("")],
             [gui.Text("Musify", text_color="white", font=f"{fuente1} 25", justification="center", size=(50, 3))],
             [gui.Text("Link de descarga", text_color="white", font=f"{fuente2}")],
             [gui.InputText(f"{InputLinkDescarga}", text_color="#BBB1E7", font=f"{fuente3}", expand_x=True, key="InputLinkDescarga")],
             [gui.Text("", text_color=f"{ColorPlataforma}", font=f"{fuente2}", key="PlataformaDetectada")],
             [gui.Text("")],
             [gui.Text("Ubicación de descarga", text_color="white", font=f"{fuente2}")],
             [gui.InputText(f"{TextoRuta}", text_color="#BBB1E7", font=f"{fuente3}", expand_x=True, key="TextoRuta")],
             [gui.FolderBrowse("Buscar ruta", font=f"{fuente3}", target="TextoRuta"), gui.InputCombo(["VIDEO", "AUDIO"], default_value="AUDIO", font=f"{fuente3}", key="TipoDescarga"), gui.Checkbox("Filtrado de nombres", True, font=f"{fuente3}", key="CheckFiltradoNombres", tooltip="El sistema de filtrado de nombres que empleamos se encarga de eliminar de los nombres de los archivos textos como '[Official Video]', o 'Videoclip Oficial'.")],
             [gui.Button("Descargar", font=f"{fuente3}", expand_x=True, key="BotonDescargar")],
             [gui.Text("Made by Eddyson versión 3.0", text_color="white", font=f"{fuente2}")],
             [gui.Text("", text_color="red", font=f"{fuente2}", key="MostrarError", justification="center", size=(500, 1))],
             [gui.Column([[gui.Text("Descargas:", font=(fuente3, 12), text_color="white", key="ContadorDescargas")]], background_color="#24262C", scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, size_subsample_height=1, sbar_relief="RELIEF_FLAT", key="ColumnaDescargas")],
             [gui.Column([[gui.Text("No descargados:", font=(fuente3, 12), text_color="red", key="ContadorNoDescargados")]], background_color="#24262C", scrollable=True, vertical_scroll_only=True, expand_x=True, size=(None, 100), size_subsample_height=1, sbar_relief="RELIEF_FLAT", key="ColumnaNoDescargados")]]

#[gui.Text(["1", "2"], size=(None, 5), key="NoDescargados")]

# Aquí están los valores de las keys utilizadas para cada dato.
"""
InputLinkDescarga: - - -ENLACE DE VIDEO/CANCIÓN A DESCARGAR.
TextoRuta:- - - - - - - RUTA EN LA QUE SE DESEA DESCARGAR LA CANCIÓN.
BotonDescargar:- - - - -BOTÓN QUE INICIA LA DESCARGA DE LAS CANCIONES.
TipoDescarga: - - - - - SELECTOR QUE PERMITE DECIDIR QUÉ.
CheckFiltradoNombres:- -OPCIÓN QUE PERMITE ACTIVAR LA FUNCIÓN DE FILTRADO DE NOMBRES.
MostrarError: - - - - - TEXTO QUE MOSTRARÁ EL ERROR QUE NO PERMITE QUE EL USUARIO CONTINÚE USANDO EL PROGRAMA.
PlataformaDetectada: - -TEXTO QUE MUESTRA LA PLATAFORMA A LA QUE PERTENECE EL LINK INTRODUCIDO.
ColumnaDescargas: - - - APARECERÁ DE FORMA ENLISTADA LAS CANCIONES QUE SE HAN DESCARGADO.
ContadorDescargas: - - -APARECERÁ LA CANTIDAD DE DESCARGAS REALIZADAS.
ColumnaNoDescargados: - APARECERÁN LOS ARCHIVOS QUE NO SE HAYAN PODIDO DESCARGAR EXITOSAMENTE.
ContadorNoDescargados: -ARCHIVOS NO DESCARGADOS.
"""

# Ahora vamos a comprobar qué tanto vamos a encoger o estirar la ventana que se abre inicialmente.
if round(monitor_x/monitor_y) >= 2.00: # Ultrawide.
    resolucion_x = int(monitor_x/3)
    resolucion_y = int(monitor_y/1.5)
else:                                  # Monitor normal.
    resolucion_x = int(monitor_x/1.7)
    resolucion_y = int(monitor_y/1.7)

# Aquí configuraremos las propiedades generales de la ventana.
def Ventana():
    ventana = gui.Window("Musify", layout=interfaz1, size=(resolucion_x, resolucion_y), resizable=True, icon="MusifyLogo.ico")

    EjecutarHilo3 = 0 # Esto comprobará si se ha ejecutado una vez el hilo 3.
    # Aquí la ventana se ejecutará de forma contínua.
    while True:
        evento, valor = ventana.read() # Esto es el resultado de las interacciones del usuario con la interfaz
        if evento != gui.WIN_CLOSED:
            # A partir de aquí podemos indicar las órdenes que se ejecutarán entre interacción e interacción.
            #print(evento, valor)

            # Asignaremos a las variables anteriormente creadas sus valores correspondientes.
            InputLinkDescarga = valor["InputLinkDescarga"] # Enlace del contenido a descargar
            TextoRuta = valor["TextoRuta"] # Esta es la carpeta en la que se realizarán las descargas (actualmente contiene valor por defecto)
            TipoDescarga = valor["TipoDescarga"] # Aquí se verá indicado si se descarga audio o video.
            CheckFiltradoNombres = valor["CheckFiltradoNombres"] # Aquí se comprobará si se filtrarán los nombres de los archivos utilizando mi algoritmo.
            Error = False

            # Ahora detectaremos a qué plataforma pertenece el enlace introducido y su color en hexadecimal para su representación.
            plataforma = Detector_Plataforma(InputLinkDescarga)
            ventana["PlataformaDetectada"].Update(plataforma)

            # Ahora comprobaremos los posibles errores que puedan cometerse en la interfaz gráfica, antes de comenzar con las descargas.
            ventana["MostrarError"].Update(Detector_Errores(InputLinkDescarga, TextoRuta, TipoDescarga))

            # Ahora ejecutaremos la descarga del contenido deseado.
            # Aquí haremos la descarga desde YouTube distinguiendo entre un contenido solitario o una playlist.

            # Para descargar audio desde YouTube:
            if ventana["MostrarError"].get() == "" and TipoDescarga == "AUDIO" and ventana["PlataformaDetectada"].get().upper() == "YOUTUBE":
                def Realizar_descarga():
                    if Detector_PlayList(InputLinkDescarga) in ["PLAYLIST", "LIST"]: # Primero detectaremos si el link hace referencia a una playlist.
                        Descargar_audio_playlist_YouTube(InputLinkDescarga, TextoRuta, CheckFiltradoNombres)
                        pass
                    else:
                        Descargar_audio_YouTube(InputLinkDescarga, TextoRuta, CheckFiltradoNombres)

            # Para descargar video desde YouTube 
            if ventana["MostrarError"].get() == "" and TipoDescarga == "VIDEO" and ventana["PlataformaDetectada"].get().upper() == "YOUTUBE":
                def Realizar_descarga():
                    if Detector_PlayList(InputLinkDescarga) in ["PLAYLIST", "LIST"]: # Primero detectaremos si el link hace referencia a una playlist.
                        Descargar_video_playlist_YouTube(InputLinkDescarga, TextoRuta, CheckFiltradoNombres)
                        pass
                    else:
                        Descargar_video_YouTube(InputLinkDescarga, TextoRuta, CheckFiltradoNombres)

            MusifyJson = open("Musify.json", "w")
            ContenidoJson = {"Descargas":[], "TotalDescargas":0, "CantidadDescargadas":0, "SinDescargar":[], "Detener":False}
            json.dump(ContenidoJson, MusifyJson)
            MusifyJson.close()

            if ventana["MostrarError"].get() == "" and ventana["PlataformaDetectada"].get().upper() == "YOUTUBE":
                hilo2 = threading.Thread(name="Hilo2", target=Realizar_descarga)
                hilo2.start()



                # Esta función que estará aquí debajo será que que será empleada para mostrar los elementos descargados.
                def Mostrar_Columna_Descargas():
                    #from GUI import hilo2
                    ya_mostrados = []
                    ya_mostrados2 = []
                    while True:
                        time.sleep(0.7)
                        with open("Musify.json", "r") as JsonMusify:
                            contenido = json.load(JsonMusify)

                        # Estas son las variables de nuestro archivo "Musify.json"
                        descargas_mostrar = contenido["Descargas"]
                        descargas_totales = contenido["TotalDescargas"]
                        descargas_finalizadas = contenido["CantidadDescargadas"]
                        detener_proceso = contenido["Detener"]
                        no_descargado = contenido["SinDescargar"]

                        for elemento in descargas_mostrar:
                            if detener_proceso == True:
                                break
                            elif elemento in ya_mostrados:
                                pass
                            else:
                                ya_mostrados.append(elemento)
                                contador_descargas = f"Descargas: {descargas_finalizadas}/{descargas_totales}"
                                #fila = [[gui.pin(gui.Col([[gui.Text(f"{elemento}")]]))]]
                                fila = [[gui.Text(elemento, font=(fuente3, 8))]]
                                ventana.extend_layout(ventana["ColumnaDescargas"], fila)

                                ventana["ContadorDescargas"].Update(contador_descargas)
                                #ventana.refresh()
                                ventana["ColumnaDescargas"].contents_changed()

                        for elemento2 in no_descargado:
                            if detener_proceso == True:
                                break
                            elif elemento2 in ya_mostrados2:
                                pass
                            else:
                                ya_mostrados2.append(elemento2)
                                contador_no_descargados = f"No descargados: {len(no_descargado)}/{descargas_totales}"
                                #fila = [[gui.pin(gui.Col([[gui.Text(f"{elemento}")]]))]]
                                fila = [[gui.Text(elemento2, font=(fuente3, 8), text_color="red")]]
                                ventana.extend_layout(ventana["ColumnaNoDescargados"], fila)
                                
                                ventana["ContadorNoDescargados"].Update(contador_no_descargados)
                                #ventana.refresh()
                                ventana["ColumnaNoDescargados"].contents_changed()
                        if detener_proceso == True:
                            break

                if EjecutarHilo3 == 0:
                    hilo3 = threading.Thread(name="Hilo3", target=Mostrar_Columna_Descargas)
                    hilo3.start()
                    EjecutarHilo3 += 1
        elif evento == gui.WIN_CLOSED: # En caso de que cerremos la ventana...
            MusifyJson = open("Musify.json", "w")
            ContenidoJson = {"Descargas":[], "TotalDescargas":0, "CantidadDescargadas":0, "SinDescargar":[], "Detener":True}
            json.dump(ContenidoJson, MusifyJson)
            MusifyJson.close()
            break
    ventana.close() # Definimos que cerramos la ventana en caso de cerrar el bucle.

hilo1 = threading.Thread(name="Hilo1", target=Ventana) # Este es el hilo encargado de ejecutar toda la ventana como ocurría anteriormente.
hilo1.start()
hilo1.join()