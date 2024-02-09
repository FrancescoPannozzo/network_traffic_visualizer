import math

numero = 123.456
parte_frazionaria, parte_intera = math.modf(numero)
print(parte_frazionaria)  # Questo sarà un numero negativo per i numeri float negativi
print(parte_intera)

numero = 123.456789
parte_frazionaria = numero - int(numero)
parte_frazionaria_arrotondata = round(parte_frazionaria, 3)
print(parte_frazionaria_arrotondata)

LINK_CAP = 1000
PACKET_SIZE = 1518
# Packets Per Seconds
PPS = ((LINK_CAP * 1e6) / 8) / PACKET_SIZE
print(f"PPS = {PPS}")