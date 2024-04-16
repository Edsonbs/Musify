import screeninfo, time, threading
import PySimpleGUI as gui
from Musify_YouTube import Musify_YouTube
from MusifyTools import MusifyTools

class InterfazGrafica:
    def __init__(self):
        # Constantes
        self.VERSION = "4.1.1"
        self.TEMAS_NOMBRES = gui.theme_list() # Todos los temas.
        self.OPCIONES_DESCARGA = ["VIDEO", "AUDIO"]
        self.MONITOR_X = screeninfo.get_monitors()[0].width # Ancho actual del monitor principal
        self.MONITOR_Y = monitor_y = screeninfo.get_monitors()[0].height # Alto del monitor principal
        self.TIPOGRAFIA_1, self.TIPOGRAFIA_2, self.TIPOGRAFIA_3 = "Terminal", "Minecraft", "Courier" # Otra opción como fuente 3 sería "Pixellari".
        self.TAMANO_TITULO, self.TAMANO_TITULO2, self.TAMANO_INPUT, self.TAMANO_TEXTO_SIMPLE, self.TAMANO_TEXTO_MINI = 34, 18, 15, 12, 8
        self.RESOLUCION_X = int(round(self.MONITOR_X/2, 0))
        self.RESOLUCION_Y = int(round(self.MONITOR_Y/1.5, 0))
        self.MUSIFY_TOOLS = MusifyTools()
        self.RUTA_USUARIO = self.MUSIFY_TOOLS.obtenerDirectorioUsuario()

        # Variables
        gui.theme("Dark Grey 13")

        # Parámetros de la clase de descarga.
        self.urlDescarga = "Reemplaza este texto por un link"
        self.rutaDescarga = self.MUSIFY_TOOLS.obtenerDirectorioEscritorio()
        self.tipoDescarga = self.OPCIONES_DESCARGA[0]
        self.filtrarNombres = True

        self.plataformaDetectada = self.MUSIFY_TOOLS.obtenerPlataforma(self.urlDescarga)

        # Con esto tendremos en cuenta si el usuario está pulsando varias veces el botón de descargar con el mismo link.
        self.urlDescargada = []

        # Representación de las descargas actuales realizadas.
        self.actualizadorDespierto = False
        self.descargados = []
        self.descargadosMostrados = []
        self.noDescargados = []
        self.noDescargadosMostrados = []
        self.descargasTotales = 0
        self.cantidadDescargadas = 0
        self.cantidadNoDescargados = 0
        self.elementosInterfaz = [  [gui.Text("")],
                                    [gui.Text("Musify", text_color="white", font=f"{self.TIPOGRAFIA_1} {self.TAMANO_TITULO}", justification="center", size=(self.MONITOR_X, 3))],
                                    [gui.Text("Link de descarga", text_color="white", font=f"{self.TIPOGRAFIA_2} {self.TAMANO_TITULO2}")],
                                    [gui.InputText(f"{self.urlDescarga}", text_color="#BBB1E7", font=f"{self.TIPOGRAFIA_3} {self.TAMANO_INPUT}", expand_x=True, key="urlDescarga")],
                                    [gui.Text("", text_color=f"{self.plataformaDetectada[1]}", font=f"{self.TIPOGRAFIA_2} {self.TAMANO_TEXTO_SIMPLE}", key="plataformaDetectada")],
                                    [gui.Text("")],
                                    [gui.Text("Ubicacion de descarga", text_color="white", font=f"{self.TIPOGRAFIA_2} {self.TAMANO_TITULO2}")],
                                    [gui.InputText(f"{self.rutaDescarga}", text_color="#BBB1E7", font=f"{self.TIPOGRAFIA_3} {self.TAMANO_INPUT}", expand_x=True, key="rutaDescarga")],
                                    [gui.FolderBrowse("Buscar ruta", font=f"{self.TIPOGRAFIA_3} {self.TAMANO_INPUT}", target="rutaDescarga"), gui.InputCombo(self.OPCIONES_DESCARGA, default_value=self.OPCIONES_DESCARGA[0], font=f"{self.TIPOGRAFIA_3} {self.TAMANO_INPUT}", key="tipoDescarga"), gui.Checkbox("Filtrado de nombres", True, font=f"{self.TIPOGRAFIA_3} {self.TAMANO_INPUT}", key="filtrarNombres", tooltip="Esta función se encarga de eliminar de los nombres de los archivos textos como '[Official Video]', o 'Videoclip Oficial'.")],
                                    [gui.Button("Descargar", font=f"{self.TIPOGRAFIA_3} {self.TAMANO_INPUT}", expand_x=True, key="botonDescargar")],
                                    [gui.Text(f"Made by Eddyson {self.VERSION}", text_color="white", font=f"{self.TIPOGRAFIA_2} {self.TAMANO_TEXTO_SIMPLE}")],
                                    [gui.Text("", text_color="red", font=f"{self.TIPOGRAFIA_2} {self.TAMANO_TEXTO_SIMPLE}", key="mostrarError", justification="center", size=(500, 1))],
                                    [gui.Column([[gui.Text("Descargadas:", font=(self.TIPOGRAFIA_3, self.TAMANO_TEXTO_SIMPLE), text_color="white", key="contadorDescargadas")]], background_color="#24262C", scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, size_subsample_height=1, sbar_relief="RELIEF_FLAT", key="columnaDescargadas")],
                                    [gui.Column([[gui.Text("No descargados:", font=(self.TIPOGRAFIA_3, self.TAMANO_TEXTO_SIMPLE), text_color="red", key="contadorNoDescargadas")]], background_color="#24262C", scrollable=True, vertical_scroll_only=True, expand_x=True, size=(None, 100), size_subsample_height=1, sbar_relief="RELIEF_FLAT", key="columnaNoDescargadas")]]
        self.Musify_YouTube = Musify_YouTube(self.urlDescarga, self.rutaDescarga, self.tipoDescarga, self.filtrarNombres, self.MUSIFY_TOOLS)

    def actualizarListaDescargas(self):
        while True:
            time.sleep(1)
            ficheroJson = self.MUSIFY_TOOLS.leerYVaciarJson()
            if ficheroJson != None:
                self.descargados = ficheroJson["Descargados"]
                self.noDescargados = ficheroJson["NoDescargados"]
                self.descargasTotales = self.Musify_YouTube.obtenerDescargasTotales()

                for descargado in self.descargados:
                    if descargado not in self.descargadosMostrados:
                        self.descargadosMostrados.append(descargado)
                        self.cantidadDescargadas += 1
                        contadorDescargas = f"Descargas: {self.cantidadDescargadas}/{self.descargasTotales}"

                        # Ahora actualizaremos la GUI con la nueva descarga realizada.
                        nuevaFila = [[gui.Text(descargado, font=(self.TIPOGRAFIA_3, self.TAMANO_TEXTO_MINI))]]
                        self.ventana.extend_layout(self.ventana["columnaDescargadas"], nuevaFila)
                        self.ventana["contadorDescargadas"].Update(contadorDescargas)
                        self.ventana["columnaDescargadas"].contents_changed()

                for noDescargado in self.noDescargados:
                    if noDescargado not in self.noDescargadosMostrados:
                        self.noDescargadosMostrados.append(noDescargado)
                        self.cantidadNoDescargados += 1
                        contadorNoDescargado = f"No descargados: {self.cantidadNoDescargados}/{self.descargasTotales}"

                        # Ahora actualizaremos la GUI con las no descargadas.
                        nuevaFila = [[gui.Text(noDescargado, font=(self.TIPOGRAFIA_3, self.TAMANO_TEXTO_MINI), text_color="red")]]
                        self.ventana.extend_layout(self.ventana["columnaNoDescargadas"], nuevaFila)
                        self.ventana["contadorNoDescargadas"].Update(contadorNoDescargado)
                        self.ventana["columnaNoDescargadas"].contents_changed()

    def inicializarHiloDescarga(self):
        self.Musify_YouTube = Musify_YouTube(self.urlDescarga, self.rutaDescarga, self.tipoDescarga, self.filtrarNombres, self.MUSIFY_TOOLS)
        self.Musify_YouTube.iniciarDescarga()

    def iniciarVentana(self):
        self.ventana = gui.Window("Musify", layout=self.elementosInterfaz, size=(self.RESOLUCION_X, self.RESOLUCION_Y), resizable=True, icon="Musify_Logo.ico")
        while True:
            evento, contenidoGUI = self.ventana.read()
            if evento == gui.WIN_CLOSED:
                break

            # Aquí va el código

            self.MUSIFY_TOOLS.crearJson()

            self.urlDescarga = contenidoGUI["urlDescarga"]
            self.rutaDescarga = contenidoGUI["rutaDescarga"]
            self.tipoDescarga = contenidoGUI["tipoDescarga"]
            self.filtrarNombres = contenidoGUI["filtrarNombres"]
            self.plataformaDetectada = self.MUSIFY_TOOLS.obtenerPlataforma(self.urlDescarga)

            self.ventana["plataformaDetectada"].Update(self.plataformaDetectada[0])
            self.ventana["mostrarError"].Update(self.MUSIFY_TOOLS.obtenerError(self.urlDescarga, self.rutaDescarga, self.tipoDescarga))

            if self.ventana["mostrarError"].get() == "" and self.urlDescarga not in self.urlDescargada:
                # Iniciamos la descarga usando otro hilo para que la interfaz no se quede colgada mientras se calculan y asignan los hilos necesarios.
                hiloInicializador = threading.Thread(name="hiloInicializador", target=self.inicializarHiloDescarga)
                hiloInicializador.daemon = True
                hiloInicializador.start()
                self.urlDescargada.append(self.urlDescarga)

                if self.actualizadorDespierto == False:
                    # Este hilo actualizará la lista de canciones descargadas continuamente.
                    hiloActualizadorGUI = threading.Thread(name="hiloActualizadorGUI", target=self.actualizarListaDescargas)
                    hiloActualizadorGUI.daemon = True
                    hiloActualizadorGUI.start()
                    self.actualizadorDespierto = True

        self.ventana.close()