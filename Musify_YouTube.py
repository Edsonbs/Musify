import pytube, re, os, threading
from MusifyTools import MusifyTools
from pytube.exceptions import AgeRestrictedError

class Musify_YouTube:
    def __init__(self, url=str, rutaDescarga=str, elementoDescarga=str):
        self.url = url
        self.rutaDescarga = rutaDescarga
        self.elementoDescarga = str(str(elementoDescarga).upper())
        self.cantidadDescargasTotales = 0

    def esPlaylist(self):
        match1 = re.search(r'\bplaylist\b', self.url)
        match2 = re.search(r'\blist\b', self.url)

        if match1 != None and match1.group() == "playlist":
            return True
        elif match2 != None and match2.group() == "list":
            return True

        return False

    def descargar(self):
        MSG_VIDEO = "VIDEO"
        MSG_AUDIO = "AUDIO"
        RUTA_DESCARGA = self.rutaDescarga
        self.RUTA_USUARIO = MusifyTools().obtenerDirectorioUsuario()

        paraDescargar = []

        if self.esPlaylist() == True:
            VIDEOS = pytube.Playlist(self.url) # Lista de los videos de YT.
            for urlDescarga in VIDEOS:
                paraDescargar.append(urlDescarga)
        elif self.esPlaylist() == False:
            paraDescargar.append(self.url)

        self.cantidadDescargasTotales = len(paraDescargar)

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

                nombre = MusifyTools().soloCaracteresPermitidosEnNombreDeArchivoDelSistema(f"{TITULO} - {AUTOR}.mp4")

                if os.path.exists(self.rutaDescarga+"\\"+nombre): # En caso de que ya se encuentre un archivo con este nombre, no se procesará éste.
                    return

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

                    MusifyTools().convertirArchivo(RUTA_USUARIO_CON_ARCHIVO, RUTA_CON_ARCHIVO)
                    MusifyTools().editarMetadatoMP3(RUTA_CON_ARCHIVO, AUTOR, PORTADA, ANO_PUBLICACION)
                    nombre = nuevoNombre # Para cuando lo añadamos a los descargados.

                MusifyTools().actualizarJson(self.RUTA_USUARIO, nombre, "") # Para que en la GUI aparezca que se ha descargado este elemento.
            except AgeRestrictedError or Exception:
                VIDEO = pytube.YouTube(videoDescargable)
                AUTOR = (VIDEO.author) # Nos devuelve el nombre del canal que ha subido ese video.
                TITULO = (VIDEO.title) # Nos entrega el título del video.
                nombre = str(MusifyTools().soloCaracteresPermitidosEnNombreDeArchivoDelSistema(f"{TITULO} - {AUTOR}.mp4"))
                if self.elementoDescarga == MSG_AUDIO:
                    nombre = nombre.replace("mp4", "mp3")

                MusifyTools().actualizarJson(self.RUTA_USUARIO, "", nombre)

    def obtenerDescargasTotales(self):
        return self.cantidadDescargasTotales

    def iniciarDescarga(self):
        hiloDescarga = threading.Thread(name="Hilo Descarga", target=self.descargar)
        hiloDescarga.start()