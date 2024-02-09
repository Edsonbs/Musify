
milista = []

variar = 5
for i in range(100):
    if variar == 0:
        variar = 5
        milista.append("e")
    else:
        milista.append("a")
        variar -= 1

indexador = 0
while indexador < len(milista):
    elemento = milista[indexador]
    if elemento == "a":
        milista.remove(elemento)
    else:
        indexador += 1
    print(f"{milista}, {indexador}")