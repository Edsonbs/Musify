class ContenidoDescargado:
    def __init__(self):
        self.descargadas = []
        self.noDescargadas = []

    def anadirDescargado(self, descargado=str):
        self.descargadas.append(descargado)
        print(self.descargadas)

    def anadirNoDescargado(self, noDescagado=str):
        self.noDescargadas.append(noDescagado)

    def obtenerDescargadas(self):
        print(self.descargadas)
        return self.descargadas

    def obtenerNoDescargadas(self):
        return self.noDescargadas