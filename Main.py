from GUI import InterfazGrafica
import threading

InterfazGrafica().iniciarVentana()

"""hilo1 = threading.Thread(name="Hilo1", target=InterfazGrafica().iniciarVentana())
hilo2 = threading.Thread(name="Hilo2", target=InterfazGrafica().actualizarVentana())

hilo1.start()
hilo2.start()"""