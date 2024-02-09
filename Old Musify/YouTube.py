import pytube, moviepy, os, json, traceback
from moviepy.editor import AudioFileClip
from pytube import YouTube

#########################################
# AQUÍ VA TODO LO RELACIONADO A YOUTUBE #
#########################################


def Informacion_YouTube(link_descarga):
    video = pytube.YouTube(url=link_descarga)
    canal = (video.author) # Nos devuelve el nombre del canal que ha subido ese video.
    titulo = (video.title) # Nos entrega el título del video.
    duracion = (video.length) # Nos retorna la duración en segundos.
    descripcion = (video.description) # Nos entrega la descripción del video.
    portada = (video.thumbnail_url) # Devuelve la URL de la foto de portada.
    visualizaciones = (video.views) # Entrega las visitas que tiene el video.
    print(canal, "\n", titulo, "\n", duracion, "\n", descripcion, "\n", portada, "\n", visualizaciones)
    return titulo


# Para descargar sólo el sonido de un video de YouTube:
def Descargar_audio_YouTube(link=str, ruta_descarga=str, recortador=bool):
    try:
        with open("Musify.json", "r") as DescargasArchivo:
            ArchivoBase = json.load(DescargasArchivo)
        if ArchivoBase["Detener"] == True:
            return

        ArchivoBase["TotalDescargas"] += 1
        with open("Musify.json", "w") as ArchivosDescargados:
            json.dump(ArchivoBase, ArchivosDescargados)

        yt = pytube.YouTube(link)
        if yt.age_restricted == False:
            calidad = yt.streams.get_audio_only()
            if recortador == True:
                from funciones import Acortador_Nombres
                nombre = f"{Acortador_Nombres(f'{yt.title} - {yt.author}')}.mp3"
            else:
                nombre = f"{yt.title} - {yt.author}.mp3"
            if os.path.exists(nombre):
                with open("Musify.json", "r") as DescargasArchivo:
                    ArchivoBase = json.load(DescargasArchivo)
                ArchivoBase["CantidadDescargadas"] += 1
                with open("Musify.json", "w") as ArchivosDescargados:
                    json.dump(ArchivoBase, ArchivosDescargados)
                pass
            else:
                calidad.download(output_path=ruta_descarga, filename=nombre)
                ArchivoBase["Descargas"].append(f"(YOUTUBE) | {nombre}")
                ArchivoBase["CantidadDescargadas"] += 1
                with open("Musify.json", "w") as ArchivosDescargados:
                    json.dump(ArchivoBase, ArchivosDescargados)
        else:
            yt = pytube.YouTube(link)
            if recortador == True:
                from funciones import Acortador_Nombres
                nombre = f"{Acortador_Nombres(f'{yt.title} - {yt.author}')}.mp3"
            else:
                nombre = f"{yt.title} - {yt.author}.mp3"
            with open("Musify.json", "r") as DescargasArchivo:
                ArchivoBase = json.load(DescargasArchivo)
            ArchivoBase["SinDescargar"].append(f"(YOUTUBE) | {nombre}")
            with open("Musify.json", "w") as ArchivosDescargados:
                json.dump(ArchivoBase, ArchivosDescargados)

    except Exception:
        traceback.print_exc()

        yt = pytube.YouTube(link)
        if recortador == True:
            from funciones import Acortador_Nombres
            nombre = f"{Acortador_Nombres(f'{yt.title} - {yt.author}')}.mp3"
        else:
            nombre = f"{yt.title} - {yt.author}.mp3"
        with open("Musify.json", "r") as DescargasArchivo:
            ArchivoBase = json.load(DescargasArchivo)
        ArchivoBase["SinDescargar"].append(f"(YOUTUBE) | {nombre}")
        with open("Musify.json", "w") as ArchivosDescargados:
            json.dump(ArchivoBase, ArchivosDescargados)
        pass

    with open("Musify.json", "r") as DescargasArchivo:
        ArchivoBase = json.load(DescargasArchivo)
    if ArchivoBase["Detener"] == True:
        return

# Para descargar sólo el sonido de una PlayList de YouTube:
def Descargar_audio_playlist_YouTube(link=str, ruta_descarga=str, recortador=bool):
    contenido = pytube.Playlist(link)
    with open("Musify.json", "r") as DescargasArchivo:
        ArchivoBase = json.load(DescargasArchivo)
    ArchivoBase["TotalDescargas"] += len(contenido)
    with open("Musify.json", "w") as ArchivosDescargados:
        json.dump(ArchivoBase, ArchivosDescargados)

    for enlace in contenido:
        try:
            with open("Musify.json", "r") as DescargasArchivo:
                ArchivoBase = json.load(DescargasArchivo)
            if ArchivoBase["Detener"] == True:
                break

            yt = pytube.YouTube(enlace)
            if yt.age_restricted == False:
                calidad = yt.streams.get_audio_only()
                if recortador == True:
                    from funciones import Acortador_Nombres
                    nombre = f"{Acortador_Nombres(f'{yt.title} - {yt.author}')}.mp3"
                else:
                    nombre = f"{yt.title} - {yt.author}.mp3"
                if os.path.exists(nombre):
                    with open("Musify.json", "r") as DescargasArchivo:
                        ArchivoBase = json.load(DescargasArchivo)
                    ArchivoBase["CantidadDescargadas"] += 1
                    with open("Musify.json", "w") as ArchivosDescargados:
                        json.dump(ArchivoBase, ArchivosDescargados)
                    pass
                else:
                    with open("Musify.json", "r") as DescargasArchivo:
                        ArchivoBase = json.load(DescargasArchivo)
                    calidad.download(output_path=ruta_descarga, filename=nombre)
                    ArchivoBase["Descargas"].append(f"(YOUTUBE) | {nombre}")
                    ArchivoBase["CantidadDescargadas"] += 1
                    with open("Musify.json", "w") as ArchivosDescargados:
                        json.dump(ArchivoBase, ArchivosDescargados)

            else:
                yt = pytube.YouTube(link)
                if recortador == True:
                    from funciones import Acortador_Nombres
                    nombre = f"{Acortador_Nombres(f'{yt.title} - {yt.author}')}.mp3"
                else:
                    nombre = f"{yt.title} - {yt.author}.mp3"
                with open("Musify.json", "r") as DescargasArchivo:
                    ArchivoBase = json.load(DescargasArchivo)
                ArchivoBase["SinDescargar"].append(f"(YOUTUBE) | {nombre}")
                with open("Musify.json", "w") as ArchivosDescargados:
                    json.dump(ArchivoBase, ArchivosDescargados)

        except Exception:
            traceback.print_exc()

            yt = pytube.YouTube(enlace)
            if recortador == True:
                from funciones import Acortador_Nombres
                nombre = f"{Acortador_Nombres(f'{yt.title} - {yt.author}')}.mp3"
            else:
                nombre = f"{yt.title} - {yt.author}.mp3"
            with open("Musify.json", "r") as DescargasArchivo:
                ArchivoBase = json.load(DescargasArchivo)
            ArchivoBase["SinDescargar"].append(f"(YOUTUBE) | {nombre}")
            with open("Musify.json", "w") as ArchivosDescargados:
                json.dump(ArchivoBase, ArchivosDescargados)
            pass

    with open("Musify.json", "r") as DescargasArchivo:
        ArchivoBase = json.load(DescargasArchivo)
    if ArchivoBase["Detener"] == True:
        return



# Para descargar tanto video como audio de un video de YouTube:
def Descargar_video_YouTube(link=str, ruta_descarga=str, recortador=bool):
    try:
        with open("Musify.json", "r") as DescargasArchivo:
            ArchivoBase = json.load(DescargasArchivo)
        if ArchivoBase["Detener"] == True:
            return

        ArchivoBase["TotalDescargas"] += 1
        with open("Musify.json", "w") as ArchivosDescargados:
            json.dump(ArchivoBase, ArchivosDescargados)

        yt = pytube.YouTube(link)
        if yt.age_restricted == False:
            calidad = yt.streams.get_highest_resolution()
            if recortador == True:
                from funciones import Acortador_Nombres
                nombre = f"{Acortador_Nombres(f'{yt.title} - {yt.author}')}.mp4"
            else:
                nombre = f"{yt.title} - {yt.author}.mp4"
            if os.path.exists(nombre):
                with open("Musify.json", "r") as DescargasArchivo:
                    ArchivoBase = json.load(DescargasArchivo)
                ArchivoBase["CantidadDescargadas"] += 1
                with open("Musify.json", "w") as ArchivosDescargados:
                    json.dump(ArchivoBase, ArchivosDescargados)
                pass
            else:
                with open("Musify.json", "r") as DescargasArchivo:
                    ArchivoBase = json.load(DescargasArchivo)
                calidad.download(output_path=ruta_descarga, filename=nombre)
                ArchivoBase["Descargas"].append(f"(YOUTUBE) | {nombre}")
                ArchivoBase["CantidadDescargadas"] += 1
                with open("Musify.json", "w") as ArchivosDescargados:
                    json.dump(ArchivoBase, ArchivosDescargados)

        else:
            yt = pytube.YouTube(link)
            if recortador == True:
                from funciones import Acortador_Nombres
                nombre = f"{Acortador_Nombres(f'{yt.title} - {yt.author}')}.mp3"
            else:
                nombre = f"{yt.title} - {yt.author}.mp3"
            with open("Musify.json", "r") as DescargasArchivo:
                ArchivoBase = json.load(DescargasArchivo)
            ArchivoBase["SinDescargar"].append(f"(YOUTUBE) | {nombre}")
            with open("Musify.json", "w") as ArchivosDescargados:
                json.dump(ArchivoBase, ArchivosDescargados)

    except Exception:
        traceback.print_exc()

        yt = pytube.YouTube(link)
        if recortador == True:
            from funciones import Acortador_Nombres
            nombre = f"{Acortador_Nombres(f'{yt.title} - {yt.author}')}.mp3"
        else:
            nombre = f"{yt.title} - {yt.author}.mp3"
        with open("Musify.json", "r") as DescargasArchivo:
            ArchivoBase = json.load(DescargasArchivo)
        ArchivoBase["SinDescargar"].append(f"(YOUTUBE) | {nombre}")
        with open("Musify.json", "w") as ArchivosDescargados:
            json.dump(ArchivoBase, ArchivosDescargados)
        pass

    with open("Musify.json", "r") as DescargasArchivo:
        ArchivoBase = json.load(DescargasArchivo)
    if ArchivoBase["Detener"] == True:
        return


# Para descargar tanto video como audio de una PlayList de YouTube:
def Descargar_video_playlist_YouTube(link=str, ruta_descarga=str, recortador=bool):
    contenido = pytube.Playlist(link)
    with open("Musify.json", "r") as DescargasArchivo:
        ArchivoBase = json.load(DescargasArchivo)
    ArchivoBase["TotalDescargas"] += len(contenido)
    with open("Musify.json", "w") as ArchivosDescargados:
        json.dump(ArchivoBase, ArchivosDescargados)

    for enlace in contenido:
        try:
            with open("Musify.json", "r") as DescargasArchivo:
                ArchivoBase = json.load(DescargasArchivo)
            if ArchivoBase["Detener"] == True:
                break

            yt = pytube.YouTube(enlace)
            if yt.age_restricted == False:
                calidad = yt.streams.get_highest_resolution()
                if recortador == True:
                    from funciones import Acortador_Nombres
                    nombre = f"{Acortador_Nombres(f'{yt.title} - {yt.author}')}.mp4"
                else:
                    nombre = f"{yt.title} - {yt.author}.mp4"
                if os.path.exists(nombre):
                    with open("Musify.json", "r") as DescargasArchivo:
                        ArchivoBase = json.load(DescargasArchivo)
                    ArchivoBase["CantidadDescargadas"] += 1
                    with open("Musify.json", "w") as ArchivosDescargados:
                        json.dump(ArchivoBase, ArchivosDescargados)
                    pass
                else:
                    with open("Musify.json", "r") as DescargasArchivo:
                        ArchivoBase = json.load(DescargasArchivo)
                    calidad.download(output_path=ruta_descarga, filename=nombre)
                    ArchivoBase["Descargas"].append(f"(YOUTUBE) | {nombre}")
                    ArchivoBase["CantidadDescargadas"] += 1
                    with open("Musify.json", "w") as ArchivosDescargados:
                        json.dump(ArchivoBase, ArchivosDescargados)

            else:
                yt = pytube.YouTube(link)
                if recortador == True:
                    from funciones import Acortador_Nombres
                    nombre = f"{Acortador_Nombres(f'{yt.title} - {yt.author}')}.mp3"
                else:
                    nombre = f"{yt.title} - {yt.author}.mp3"
                with open("Musify.json", "r") as DescargasArchivo:
                    ArchivoBase = json.load(DescargasArchivo)
                ArchivoBase["SinDescargar"].append(f"(YOUTUBE) | {nombre}")
                with open("Musify.json", "w") as ArchivosDescargados:
                    json.dump(ArchivoBase, ArchivosDescargados)

        except Exception:
            traceback.print_exc()

            yt = pytube.YouTube(enlace)
            if recortador == True:
                from funciones import Acortador_Nombres
                nombre = f"{Acortador_Nombres(f'{yt.title} - {yt.author}')}.mp3"
            else:
                nombre = f"{yt.title} - {yt.author}.mp3"
            with open("Musify.json", "r") as DescargasArchivo:
                ArchivoBase = json.load(DescargasArchivo)
            ArchivoBase["SinDescargar"].append(f"(YOUTUBE) | {nombre}")
            with open("Musify.json", "w") as ArchivosDescargados:
                json.dump(ArchivoBase, ArchivosDescargados)
            pass

    with open("Musify.json", "r") as DescargasArchivo:
        ArchivoBase = json.load(DescargasArchivo)
    if ArchivoBase["Detener"] == True:
        return


# Esta función es la que he encontrado para realizar la descarga de contenido.
def Descargar_musica():
    yt = YouTube(str(input("Enter the URL of the video you want to download: \n>> ")))
    audio = yt.streams.filter(only_audio = True).first()
    print("Enter the destination (leave blank for current directory)")
    destination = str(input("")) or '.'
    out_file = audio.download(output_path = destination)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    print(yt.title + " has been successfully downloaded in .mp3 format.")
