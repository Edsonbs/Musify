import platform, os, requests, re, json
from moviepy.editor import *
from mutagen.mp3 import MP3
from mutagen.id3 import APIC
from mutagen.easyid3 import EasyID3

class MusifyTools:
    def __init__(self):
        self.directorioHome = os.path.expanduser('~')

    # Devuelve el nombre de la plataforma en la que está corriendo el programa.
    def detectarSistemaOperativo(self):
        return platform.system()

    # Elimina caracteres de un string que no pueden ser aplicados a nombres de archivos de distintos SO.
    def soloCaracteresPermitidosEnNombreDeArchivoDelSistema(self, nombreArchivo=str):
        plataforma = self.detectarSistemaOperativo()
        caracteresNoPermitidosWindows = ["<", ">", ":", '"', "/", "\\", "|", "?", "*"]
        caracteresNoPermitidosUnix = ["/"]
        listaRevisar = list
        nombreResultante = nombreArchivo

        # Vamos a revisar en qué plataforma está corriendo el programa.
        if plataforma.upper() == "WINDOWS":
            listaRevisar = caracteresNoPermitidosWindows
        elif plataforma.upper() in ["LINUX", "DARWIN"]:
            listaRevisar = caracteresNoPermitidosUnix

        # Vamos a eliminar los caracteres del nombre del archivo que no estén permitidos en ese sistema.
        nombreResultante = nombreResultante.replace('"', "''")
        for caracter in listaRevisar:
            nombreResultante = nombreResultante.replace(caracter, "")

        return nombreResultante

    # Este es un algoritmo que elimina fragmentos de los nombres que se le ponen a un video en YouTube de forma general.
    def simplificarNombreArchivo(self, nombreArchivo=str):
        eliminarGrupal = ["(OFFICIAL", "[OFFICIAL", "(VIDEOCLIP", "[VIDEOCLIP", "(ANIMATED", "[ANIMATED", "(VERTICAL", "[VERTICAL", "(CLIP", "[CLIP", "(OFICIEL", "[OFICIEL", "(MUSIC", "[MUSIC", "(LYRIC", "[LYRIC", "(HD", "[HD", "(VIDEO", "(VÍDEO", "[VIDEO", "[VÍDEO", "(360º", "[360º", "(AUDIO", "[AUDIO", "(LYRICS", "[LYRICS", "HD", "LYRIC", "LYRICS", "FULL", "OFFICIAL", "OFICIAL", "VIDEO", "ENHANCED", "1080P", "720P", "MUSIC", "VIDEO)", "VIDEO]", "OFICIAL)", "OFICIAL]", "MOVIE)", "MOVIE]", "HD)", "HD]", "AUDIO)", "AUDIO]", "VERSION)", "VERSION]", "VISUALIZER)", "VISUALIZER]", "ANIMADO)", "ANIMADO]", "VERTICAL)", "VERTICAL]", "OFICIEL)", "OFICIEL]", "OFFICIAL)", "OFFICIAL]", "CLIP)", "CLIP]", "REMASTERED)", "REMASTERED]", "LYRICS)", "LYRICS]"]
        eliminarSolitario = ["(360º)", "[360º]", "(1080P)", "[1080P]", "(720P)", "[720P]", "(LYRIC)", "[LYRIC]", "(LYRICS)", "[LYRICS]", "(LETRA)", "[LETRA]", "(WEB)", "[WEB]", "(LETRAS)", "[LETRAS]", "(OFFICIAL)", "[OFFICIAL]", "(OFICIAL)", "[OFICIAL]", "(4K)", "[4K]", "(VISUALIZER)", "[VISUALIZER]", "(VISUALIZADOR)", "[VISUALIZADOR]", "(HD)", "[HD]"]

        eliminar = []
        nombreResultante = nombreArchivo

        nombreArchivo = nombreArchivo.split(" ")

        for palabra in nombreArchivo:
            if palabra in eliminarGrupal:
                eliminar.append(palabra)
            elif palabra in eliminarSolitario:
                nombreResultante.replace(palabra, "")

        if len(eliminar) > 1:
            for palabra in eliminar:
                nombreResultante.replace(palabra, "")

        return nombreResultante

    # Para convertir un archivo MP4 a MP3.
    def convertirArchivo(self, rutaYNombreArchivoConvertir, rutaYNombreArchivoConvertido):
        archivoConvertir = AudioFileClip(rutaYNombreArchivoConvertir)
        archivoConvertir.write_audiofile(rutaYNombreArchivoConvertido, verbose=False, logger=None)
        archivoConvertir.close()
        os.remove(rutaYNombreArchivoConvertir)

    # Devuelve la ruta al directorio "User".
    def obtenerDirectorioUsuario(self):
        return os.path.expanduser('~')

    def obtenerDirectorioEscritorio(self):
        return f"{os.path.expanduser('~')}\\Desktop"

    def obtenerPlataforma(self, url):
        patronYoutube1 = re.search(r'\byoutube.com\b', url)
        patronYoutube2 = re.search(r'\byoutu.be\b', url)
        patronSpotify = re.search(r'\bspotify.com\b', url)
        patronTwitter1 = re.search(r'\btwitter.com\b', url)
        patronTwitter2 = re.search(r'\bx.com\b', url)
        patronInstagram = re.search(r'\binstagram.com\b', url)
        patronTiktok = re.search(r'\btiktok.com\b', url)
        patronTwitch = re.search(r'\btwitch.tv\b', url)

        if (patronYoutube1 != None and patronYoutube1.group() == "youtube.com") or (patronYoutube2 != None and patronYoutube2.group() == "youtu.be"):
            return "YouTube", "#FA0404"
        elif patronSpotify != None and patronSpotify.group() == "spotify.com":
            return "Spotify", "#1DE33E"
        elif (patronTwitter1 != None and patronTwitter1.group() == "twitter.com") or (patronTwitter2 != None and patronTwitter2.group() == "x.com"):
            return "Twitter", "#1DB6E3"
        elif patronInstagram != None and patronInstagram.group() == "instagram.com":
            return "Instagram", "#CE21DF"
        elif patronTiktok != None and patronTiktok.group() == "tiktok.com":
            return "TikTok", "#F8F8F8"
        elif patronTwitch != None and patronTwitch.group() == "twitch.tv":
            return "Twitch", "#BB68DF"
        else:
            return "Plataforma", "#F09C20"

    def obtenerError(self, url=str, ruta=str, tipoDescarga=str):
        error = ""

        patronURL = re.search(r'\bhttps\b', url)
        patronURL2 = re.search(r'\bhttp\b', url)

        if (patronURL != None and patronURL.group() != "https") or (patronURL2 != None and patronURL2.group() != "http"):
            error = "Debes introducir un link."
        elif self.obtenerPlataforma(url)[0].upper() != "YOUTUBE":
            error = "Debes introducir un link de [YouTube] específicamente."
        elif os.path.isdir(str(ruta)) == False:
            error = "Has seleccionado una carpeta que no existe."
        elif tipoDescarga.upper() not in ["AUDIO", "VIDEO"]:
            error = "Debes elegir descargar audio o video."
        else:
            error = ""
        return error

    # Cambia los metadatos de un archivo MP3.
    def editarMetadatoMP3(self, rutaYNombreArchivo="", autor=None, portada=None, anoPublicacion=None):
        imagen = f"{os.path.expanduser('~')}\\portadaMusify.jpg"

        # Ahora descargaremos la imagen de portada.
        urlPortada = requests.get(portada)
        archivo = open(imagen, "wb")
        archivo.write(urlPortada.content)
        archivo.close()

        audio = MP3(rutaYNombreArchivo)

        # Pondremos una foto de portada.
        with open(imagen, "rb") as archivo:
            audio.tags.add(APIC(
                encoding=3,
                mime='image/jpeg',
                type=3,
                desc=u'Portada de YouTube de este audio.',
                data=archivo.read(),
                ), )
            audio.save(v2_version=3)

        # Pondremos un autor y un año en los metadatos.
        audio = EasyID3(rutaYNombreArchivo)
        EasyID3.RegisterTextKey('year', 'TDRC')
        audio["artist"], audio["author"], audio["year"], audio["encodedby"] = autor, autor, anoPublicacion, "Musify"
        audio.save(v2_version=3)

        # Eliminaremos la foto que he descargado para asignarla como metadatos.
        os.remove(imagen)

    def crearJson(self, ruta=str):
        archivoJson = "MusifyData.json"
        datosJson = {"Descargados": [], "NoDescargados": []}
        with open(archivoJson, "w") as archivo:
            json.dump(datosJson, archivo)

    def actualizarJson(self, ruta=str, descargadoAnadir=str, noDescargadoAnadir=str):
        archivoJson = "MusifyData.json"
        with open(archivoJson, "r") as archivo:
            jsonData = json.load(archivo)

        if descargadoAnadir != "":
            jsonData["Descargados"].append(descargadoAnadir)
        if noDescargadoAnadir != "":
            jsonData["NoDescargados"].append(noDescargadoAnadir)

        with open(archivoJson, "w") as archivo:
            json.dump(jsonData, archivo)

    def leerJson(self, ruta=str):
        archivoJson = "MusifyData.json"
        with open(archivoJson, "r") as archivo:
            jsonData = json.load(archivo)
            return jsonData