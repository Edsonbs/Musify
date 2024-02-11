import pytube, re, os, threading, time
from MusifyTools import MusifyTools
from pytube.exceptions import AgeRestrictedError

class Musify_YouTube:
    def __init__(self, url=str, rutaDescarga=str, elementoDescarga=str, simplificarNombre=bool):
        self.url = url
        self.rutaDescarga = rutaDescarga
        self.elementoDescarga = str(str(elementoDescarga).upper())
        self.simplificarNombre = simplificarNombre
        self.cantidadDescargasTotales = 0
        self.linksDescargados = []
        self.MUSIFY_TOOLS = MusifyTools()
        self.RUTA_USUARIO = self.MUSIFY_TOOLS.obtenerDirectorioUsuario()

        self.nombresCancionesDescargadas1 = []
        self.nombresCancionesDescargadas2 = []
        self.nombresCancionesDescargadas3 = []
        self.nombresCancionesDescargadas4 = []
        self.nombresCancionesDescargadas5 = []

        self.todosDescargados = []

        self.nombresCancionesNoDescargadas1 = []
        self.nombresCancionesNoDescargadas2 = []
        self.nombresCancionesNoDescargadas3 = []
        self.nombresCancionesNoDescargadas4 = []
        self.nombresCancionesNoDescargadas5 = []

        self.todosNoDescargados = []

        self.listaDescargar1 = []
        self.listaDescargar2 = []
        self.listaDescargar3 = []
        self.listaDescargar4 = []
        self.listaDescargar5 = []

    def obtenerDescargasTotales(self):
        return self.cantidadDescargasTotales

    def esPlaylist(self):
        match1 = re.search(r'\bplaylist\b', self.url)
        match2 = re.search(r'\blist\b', self.url)

        if match1 != None and match1.group() == "playlist":
            return True
        elif match2 != None and match2.group() == "list":
            return True

        return False

    def prepararDescarga(self):
        self.paraDescargar = []

        if self.esPlaylist() == True:
            VIDEOS = pytube.Playlist(self.url) # Lista de los videos de YT.
            for urlDescarga in VIDEOS:
                self.paraDescargar.append(urlDescarga)
        elif self.esPlaylist() == False:
            self.paraDescargar.append(self.url)

        if self.url not in self.linksDescargados:
            self.cantidadDescargasTotales += len(self.paraDescargar)
            self.linksDescargados.append(self.url)
        
        # Vamos a dividir la cola de descargas en varias para descargar en modo multithreading.
        if len(self.paraDescargar) > 25:
            cantidadPorCola = int(round(len(self.paraDescargar) / 5))
            self.listaDescargar1 = self.paraDescargar[:cantidadPorCola] # El primer quinto de las canciones.
            self.listaDescargar2 = self.paraDescargar[cantidadPorCola+1:cantidadPorCola*2] # El segundo quinto.
            self.listaDescargar3 = self.paraDescargar[cantidadPorCola*2+1:cantidadPorCola*3] # El tercer quinto.
            self.listaDescargar4 = self.paraDescargar[cantidadPorCola*3+1:cantidadPorCola*4] # El cuarto quinto.
            self.listaDescargar4 = self.paraDescargar[cantidadPorCola*4+1:] # El último quinto
        elif len(self.paraDescargar) > 20:
            cantidadPorCola = int(round(len(self.paraDescargar) / 4))
            self.listaDescargar1 = self.paraDescargar[:cantidadPorCola] # El primer cuarto de las canciones.
            self.listaDescargar2 = self.paraDescargar[cantidadPorCola+1:cantidadPorCola*2] # El segundo cuarto.
            self.listaDescargar3 = self.paraDescargar[cantidadPorCola*2+1:cantidadPorCola*3] # El tercer cuarto.
            self.listaDescargar4 = self.paraDescargar[cantidadPorCola*3+1:] # El cuarto cuarto.
        elif len(self.paraDescargar) > 15:
            cantidadPorCola = int(round(len(self.paraDescargar) / 3))
            self.listaDescargar1 = self.paraDescargar[:cantidadPorCola] # El primer tercio de las canciones.
            self.listaDescargar2 = self.paraDescargar[cantidadPorCola+1:cantidadPorCola*2] # El segundo tercio.
            self.listaDescargar3 = self.paraDescargar[cantidadPorCola*2+1:] # El tercer tercio.
        elif len(self.paraDescargar) > 10:
            cantidadPorCola = int(round(len(self.paraDescargar) / 2))
            self.listaDescargar1 = self.paraDescargar[:cantidadPorCola] # La primera mitad de las canciones.
            self.listaDescargar2 = self.paraDescargar[cantidadPorCola+1:] # La segunda mitad.
        else:
            cantidadPorCola = int(round(len(self.paraDescargar) / 2))
            self.listaDescargar1 = self.paraDescargar # Todas las canciones a modo monohilo.

    def actualizarArchivoJson(self):
        while True:
            time.sleep(0.7)
            recorrerDescargados = [self.nombresCancionesDescargadas1, self.nombresCancionesDescargadas2, self.nombresCancionesDescargadas3, self.nombresCancionesDescargadas4, self.nombresCancionesDescargadas5]

            for listaDescargas in recorrerDescargados:
                if len(listaDescargas) > 0:
                    for nombreCancion in listaDescargas:
                        self.todosDescargados.append(nombreCancion)
                        listaDescargas.remove(nombreCancion)

            recorrerNoDescargados = [self.nombresCancionesNoDescargadas1, self.nombresCancionesNoDescargadas2, self.nombresCancionesNoDescargadas3, self.nombresCancionesNoDescargadas4, self.nombresCancionesNoDescargadas5]

            for listaNoDescargas in recorrerNoDescargados:
                if len(listaNoDescargas) > 0:
                    for nombreCancion in listaNoDescargas:
                        self.todosNoDescargados.append(nombreCancion)
                        listaDescargas.remove(nombreCancion)

            self.MUSIFY_TOOLS.actualizarJsonListado(self.RUTA_USUARIO, self.todosDescargados, self.todosNoDescargados)

            """try:
                time.sleep(0.75)
                # Para la lista de descargadas correctamente.
                for nombreCancion in self.nombresCancionesDescargadas1:
                    if MusifyTools().actualizarJson(self.RUTA_USUARIO, nombreCancion, "") != "ERROR":
                        self.nombresCancionesDescargadas1.remove(nombreCancion)
                
                for nombreCancion in self.nombresCancionesDescargadas2:
                    if MusifyTools().actualizarJson(self.RUTA_USUARIO, nombreCancion, "") != "ERROR":
                        self.nombresCancionesDescargadas1.remove(nombreCancion)
                
                for nombreCancion in self.nombresCancionesDescargadas3:
                    if MusifyTools().actualizarJson(self.RUTA_USUARIO, nombreCancion, "") != "ERROR":
                        self.nombresCancionesDescargadas1.remove(nombreCancion)
                
                for nombreCancion in self.nombresCancionesDescargadas4:
                    if MusifyTools().actualizarJson(self.RUTA_USUARIO, nombreCancion, "") != "ERROR":
                        self.nombresCancionesDescargadas1.remove(nombreCancion)
                
                for nombreCancion in self.nombresCancionesDescargadas5:
                    if MusifyTools().actualizarJson(self.RUTA_USUARIO, nombreCancion, "") != "ERROR":
                        self.nombresCancionesDescargadas1.remove(nombreCancion)

                time.sleep(0.75)
                # Para la lista de no descargadas.
                for nombreCancion in self.nombresCancionesNoDescargadas1:
                    if MusifyTools().actualizarJson(self.RUTA_USUARIO, "", nombreCancion) != "ERROR":
                        self.nombresCancionesDescargadas1.remove(nombreCancion)
                
                for nombreCancion in self.nombresCancionesNoDescargadas2:
                    if MusifyTools().actualizarJson(self.RUTA_USUARIO, "", nombreCancion) != "ERROR":
                        self.nombresCancionesDescargadas1.remove(nombreCancion)
                
                for nombreCancion in self.nombresCancionesNoDescargadas3:
                    if MusifyTools().actualizarJson(self.RUTA_USUARIO, "", nombreCancion) != "ERROR":
                        self.nombresCancionesDescargadas1.remove(nombreCancion)
                
                for nombreCancion in self.nombresCancionesNoDescargadas4:
                    if MusifyTools().actualizarJson(self.RUTA_USUARIO, "", nombreCancion) != "ERROR":
                        self.nombresCancionesDescargadas1.remove(nombreCancion)
                
                for nombreCancion in self.nombresCancionesNoDescargadas5:
                    if MusifyTools().actualizarJson(self.RUTA_USUARIO, "", nombreCancion) != "ERROR":
                        self.nombresCancionesDescargadas1.remove(nombreCancion)
            except Exception:
                pass"""

    def descargar(self, paraDescargar=list, nombreHilo=str):
        MSG_VIDEO = "VIDEO"
        MSG_AUDIO = "AUDIO"
        RUTA_DESCARGA = self.rutaDescarga
        self.RUTA_USUARIO = self.MUSIFY_TOOLS.obtenerDirectorioUsuario()

        for videoDescargable in paraDescargar:
            try:
                VIDEO = pytube.YouTube(videoDescargable)
                AUTOR = (VIDEO.author) # Nos devuelve el nombre del canal que ha subido ese video.
                TITULO = (VIDEO.title) # Nos entrega el título del video.
                DURACION = (VIDEO.length) # Nos retorna la duración en segundos.
                DESCRIPCION = (VIDEO.description) # Nos entrega la descripción del video.
                PORTADA = (VIDEO.thumbnail_url) # Devuelve la URL de la foto de portada.
                VISUALIZACIONES = (VIDEO.views) # Entrega las visitas que tiene el video.
                FECHA_PUBLICACION = (VIDEO.publish_date) # Entrega la fecha de publicación.
                ANO_PUBLICACION = str(FECHA_PUBLICACION)[0:4] # Sólo el año de publicación del video en String.

                nombre = self.MUSIFY_TOOLS.soloCaracteresPermitidosEnNombreDeArchivoDelSistema(f"{TITULO} - {AUTOR}.mp4")
                if self.simplificarNombre == True:
                    nombre = self.MUSIFY_TOOLS.simplificarNombreArchivo(nombre)

                if self.elementoDescarga == MSG_AUDIO:
                    nombre = nombre.replace("mp4", "mp3")
                if os.path.exists(self.rutaDescarga+"\\"+nombre): # En caso de que ya se encuentre un archivo con este nombre, no se procesará éste.
                    return
                if self.elementoDescarga == MSG_AUDIO:
                    nombre = nombre.replace("mp3", "mp4")

                self.linksDescargados.append(videoDescargable)

                if self.elementoDescarga == MSG_VIDEO: # Comprobamos si se desea descargar video.
                    descargable = VIDEO.streams.get_highest_resolution() # Obtenemos la mejor resolución disponible.
                    descargable.download(output_path=RUTA_DESCARGA, filename=nombre) # Descargamos el archivo en cuestión.

                elif self.elementoDescarga == MSG_AUDIO:
                    descargable = VIDEO.streams.get_audio_only() # Obtenemos únicamente el audio.
                    descargable.download(output_path=self.RUTA_USUARIO, filename=nombre)

                    # Ahora convertiremos el archivo de video en audio.
                    nuevoNombre = nombre.replace("mp4", "mp3") # Cambiamos el formato de MP4 a MP3.
                    RUTA_CON_ARCHIVO = RUTA_DESCARGA+"\\"+nuevoNombre # Ubicación en donde estará el archivo que el usuario quiere descargar.
                    RUTA_USUARIO_CON_ARCHIVO = self.RUTA_USUARIO+"\\"+nombre # Ubicación de la carpeta usuario y el archivo que descargamos antes de convertirlo.

                    self.MUSIFY_TOOLS.convertirArchivo(RUTA_USUARIO_CON_ARCHIVO, RUTA_CON_ARCHIVO)
                    self.MUSIFY_TOOLS.editarMetadatoMP3(RUTA_CON_ARCHIVO, AUTOR, PORTADA, ANO_PUBLICACION)
                    nombre = nuevoNombre # Para cuando lo añadamos a los descargados.

                if nombreHilo.upper() == "HILO1":
                    self.nombresCancionesDescargadas1.append(nombre)
                elif nombreHilo.upper() == "HILO2":
                    self.nombresCancionesDescargadas2.append(nombre)
                elif nombreHilo.upper() == "HILO3":
                    self.nombresCancionesDescargadas3.append(nombre)
                elif nombreHilo.upper() == "HILO4":
                    self.nombresCancionesDescargadas4.append(nombre)
                elif nombreHilo.upper() == "HILO5":
                    self.nombresCancionesDescargadas5.append(nombre)
            except AgeRestrictedError or Exception:
                VIDEO = pytube.YouTube(videoDescargable)
                AUTOR = (VIDEO.author) # Nos devuelve el nombre del canal que ha subido ese video.
                TITULO = (VIDEO.title) # Nos entrega el título del video.
                nombre = str(self.MUSIFY_TOOLS.soloCaracteresPermitidosEnNombreDeArchivoDelSistema(f"{TITULO} - {AUTOR}.mp4"))
                if self.simplificarNombre == True:
                    nombre = self.MUSIFY_TOOLS.simplificarNombreArchivo(nombre)
                if self.elementoDescarga == MSG_AUDIO:
                    nombre = nombre.replace("mp4", "mp3")

                if nombreHilo.upper() == "HILO1":
                    self.nombresCancionesNoDescargadas1.append(nombre)
                elif nombreHilo.upper() == "HILO2":
                    self.nombresCancionesNoDescargadas2.append(nombre)
                elif nombreHilo.upper() == "HILO3":
                    self.nombresCancionesNoDescargadas3.append(nombre)
                elif nombreHilo.upper() == "HILO4":
                    self.nombresCancionesNoDescargadas4.append(nombre)
                elif nombreHilo.upper() == "HILO5":
                    self.nombresCancionesNoDescargadas5.append(nombre)

    def iniciarDescarga(self):
        self.prepararDescarga()
        if len(self.listaDescargar5) > 0:
            hiloDescarga5 = threading.Thread(name="HiloDescarga5", target=self.descargar, args=(self.listaDescargar5, "HILO5"))
            hiloDescarga4 = threading.Thread(name="HiloDescarga4", target=self.descargar, args=(self.listaDescargar4, "HILO4"))
            hiloDescarga3 = threading.Thread(name="HiloDescarga3", target=self.descargar, args=(self.listaDescargar3, "HILO3"))
            hiloDescarga2 = threading.Thread(name="HiloDescarga2", target=self.descargar, args=(self.listaDescargar2, "HILO2"))
            hiloDescarga1 = threading.Thread(name="HiloDescarga1", target=self.descargar, args=(self.listaDescargar1, "HILO1"))

            hiloDescarga5.daemon = True
            hiloDescarga4.daemon = True
            hiloDescarga3.daemon = True
            hiloDescarga2.daemon = True
            hiloDescarga1.daemon = True

            hiloDescarga5.start()
            hiloDescarga4.start()
            hiloDescarga3.start()
            hiloDescarga2.start()
            hiloDescarga1.start()
        elif len(self.listaDescargar4) > 0:
            hiloDescarga4 = threading.Thread(name="HiloDescarga4", target=self.descargar, args=(self.listaDescargar4, "HILO4"))
            hiloDescarga3 = threading.Thread(name="HiloDescarga3", target=self.descargar, args=(self.listaDescargar3, "HILO3"))
            hiloDescarga2 = threading.Thread(name="HiloDescarga2", target=self.descargar, args=(self.listaDescargar2, "HILO2"))
            hiloDescarga1 = threading.Thread(name="HiloDescarga1", target=self.descargar, args=(self.listaDescargar1, "HILO1"))

            hiloDescarga4.daemon = True
            hiloDescarga3.daemon = True
            hiloDescarga2.daemon = True
            hiloDescarga1.daemon = True

            hiloDescarga4.start()
            hiloDescarga3.start()
            hiloDescarga2.start()
            hiloDescarga1.start()
        elif len(self.listaDescargar3) > 0:
            hiloDescarga3 = threading.Thread(name="HiloDescarga3", target=self.descargar, args=(self.listaDescargar3, "HILO3"))
            hiloDescarga2 = threading.Thread(name="HiloDescarga2", target=self.descargar, args=(self.listaDescargar2, "HILO2"))
            hiloDescarga1 = threading.Thread(name="HiloDescarga1", target=self.descargar, args=(self.listaDescargar1, "HILO1"))

            hiloDescarga3.daemon = True
            hiloDescarga2.daemon = True
            hiloDescarga1.daemon = True

            hiloDescarga3.start()
            hiloDescarga2.start()
            hiloDescarga1.start()
        elif len(self.listaDescargar2) > 0:
            hiloDescarga2 = threading.Thread(name="HiloDescarga2", target=self.descargar, args=(self.listaDescargar2, "HILO2"))
            hiloDescarga1 = threading.Thread(name="HiloDescarga1", target=self.descargar, args=(self.listaDescargar1, "HILO1"))

            hiloDescarga2.daemon = True
            hiloDescarga1.daemon = True

            hiloDescarga2.start()
            hiloDescarga1.start()
        elif len(self.listaDescargar1) > 0:
            hiloDescarga1 = threading.Thread(name="HiloDescarga1", target=self.descargar, args=(self.listaDescargar1, "HILO1"))

            hiloDescarga1.daemon = True

            hiloDescarga1.start()
        
        hiloActualizador = threading.Thread(name="HiloActualizador", target=self.actualizarArchivoJson)
        hiloActualizador.daemon = True
        hiloActualizador.start()