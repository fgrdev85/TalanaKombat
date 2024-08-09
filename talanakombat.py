import re
import json
from collections import deque

# Definición de las secuencias de movimientos
movimientosT = {
    'TonynTaladoken': ['DSD', 'P'],
    'TonynRemuyuken': ['SD', 'K'],
}
movimientosA = {
    'ArnaldolRemuyuken': ['SA', 'K'],
    'ArnaldolTaladoken': ['ASA', 'P'],
}
descuentoTonyn = {
    'TonynTaladoken': 3,
    'TonynRemuyuken': 2,
    'K': 1,
    'P': 1,
    'BLK': 0,
}
descuentoArnaldol = {
    'ArnaldolTaladoken': 2,
    'ArnaldolRemuyuken': 3,
    'K': 1,
    'P': 1,
    'BLK': 0,
}
traduccion = {
    'D': 'avanza',
    'W': 'salta',
    'A': 'retrocede',
    'S': 'se agacha',
    'K': 'da una patada',
    'P': 'da un puñetazo',
    'BLK': '',
}

# Buffer de entrada (limite de movimientos recientes a considerar)
buffer = deque(maxlen=2)

# Función que encuentra un movimiento dada una combinación
def detectar_secuencia(buffer, movimientos):
    for nombre_movimiento, secuencia in movimientos.items():
        if list(buffer) == secuencia:
            return nombre_movimiento
    return None

#Detecta secuencias y define el movimiento
def recibir_entrada(input, jugador):
    buffer.append(input)
    if jugador == 1:
        movimiento_detectado = detectar_secuencia(buffer, movimientosT)
    else:
        movimiento_detectado = detectar_secuencia(buffer, movimientosA)
    if movimiento_detectado:
        return movimiento_detectado
    else:
        return 0

entradasjugador = {
    'TonynTaladoken': 'conecta un Taladoken',
    'TonynRemuyuken': 'conecta un Remuyuken',
    'ArnaldolRemuyuken': 'conecta un Remuyuken',
    'ArnaldolTaladoken': 'conecta un Taladoken',
}

#Función que relata las jugadas
def relata_jugadas(entradas_jugador, flag):
    golpe = ''
    if flag:
        print(entradasjugador[entradas_jugador[0]], end=' ')
        golpe = entradas_jugador[0]
    else:
        for i in entradas_jugador:
            print( traduccion.get(i, 'se mueve'), end=' ')
        golpe = entradas_jugador[-1]
    return golpe

#Permite discriminar entre un movimiento y golpes simples
def procesa_entrada(entradas_jugador, jugador):
    buffer.append(entradas_jugador[0])
    for i in range(1,len(entradas_jugador)):
        flag = 0
        movimiento = recibir_entrada(entradas_jugador[i], jugador)
        if movimiento:
            flag = 1
            entradas_jugador[i-1] = movimiento
            entradas_jugador = entradas_jugador[:-1]

    return relata_jugadas(entradas_jugador, flag)


def leer_json(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        datos = json.load(archivo)
    return datos

# Función para reconocer las secuencias en una lista de strings
def reconocer_secuencias(lista, expresion):
    resultados = []
    for string in lista:
        matches = re.findall(expresion, string)
        resultados.append(matches)
    return resultados

#Preprocesamiento de listas
def procesar_listas(lista):
    for i in range(len(lista)):
        if len(lista[i]) == 1:
            lista[i] = ['BLK']
        else:
            lista[i] = lista[i][:-1]
    return lista


def concatenar_listas(a, b):
    for i in range(len(a)):
        a[i].append(b[i][0])
    return a

# Cuenta los caracteres apra definir el jugador que comienza
def cuenta_caracteres(l):
    contador = 0
    for i in range(len(l)):
        contador = contador + len(l[i])
    return contador

# Cuenta los caracteres apra definir el jugador que comienza
def inicia_juego(a,b,c,d):
    inicia = 1
    l1 = cuenta_caracteres(a)
    l2 = cuenta_caracteres(b)
    l3 = cuenta_caracteres(c)
    l4 = cuenta_caracteres(d)
    if l1+l2 == l3+l4:
        if l1 == l3:
            if l2 > l4:
                inicia = 2
        elif l1 > l3:
            inicia = 2
    elif l1 + l2 > l3 + l4:
        inicia = 2
    return inicia

#Valida que sean maximo 5 movimientos
def validar_movs(l):
    for i in range(len(l)):
        l[i] = l[i][:5]

#Valida que sea 1 solo golpe
def validar_golpes(l):
    for i in range(len(l)):
        l[i] = l[i][:1]


# Expresión regular para las secuencias especificadas
expresion_regular = r'(DSD|ASA|SA|SD|W|S|A|D|P|K|)'


# Ruta del archivo JSON
ruta_archivo = 'datos.json'

# Leer el archivo JSON
contenido_json = leer_json(ruta_archivo)

#Extrae los movimientos y los golpes de ambos jugadores
lista1 = contenido_json['player1']['movimientos']
lista2 = contenido_json['player1']['golpes']
lista3 = contenido_json['player2']['movimientos']
lista4 = contenido_json['player2']['golpes']

#Valida que sean maximo 5 movimientos
#Valida que sea 1 solo golpe
validar_movs(lista1)
validar_golpes(lista2)
validar_movs(lista3)
validar_golpes(lista4)

# Evaluar cada lista
# m1 significa movimientos del player1
m1 = reconocer_secuencias(lista1, expresion_regular)
# g1 significa golpes del player1
g1 = reconocer_secuencias(lista2, expresion_regular)
# m1 significa movimientos del player2
m2 = reconocer_secuencias(lista3, expresion_regular)
# m1 significa golpes del player2
g2 = reconocer_secuencias(lista4, expresion_regular)

#Procesamiento previo de las listas
m1 = procesar_listas(m1)
g1 = procesar_listas(g1)
m2 = procesar_listas(m2)
g2 = procesar_listas(g2)
l1 = concatenar_listas(m1, g1)
l2 = concatenar_listas(m2, g2)

# Define el jugador que empieza
inicia = inicia_juego(lista1,lista2,lista3,lista4)
puntosplayer1 = 6
puntosplayer2 = 6
largo_menor = len(l1) if len(l1) < len(l2) else len(l2)

#Flujo principal escribe el relato y cambia el orden dependiendo del jugador que empieza
for i in range(largo_menor):
    if inicia == 1:
        print(' Tonyn ', end='')
        descuento = procesa_entrada(l1[i],1)
        puntosplayer2 -= descuentoTonyn.get(descuento,0)
        print('')
        if puntosplayer2 <= 0:
            break
        print(' Arnaldol ', end='')
        descuento = procesa_entrada(l2[i],2)
        puntosplayer1 -= descuentoArnaldol.get(descuento, 0)
        print('')
        if puntosplayer1 <= 0:
            break
    else:
        print(' Arnaldol ', end='')
        descuento = procesa_entrada(l2[i],2)
        puntosplayer1 -= descuentoArnaldol.get(descuento,0)
        print('')
        if puntosplayer1 <= 0:
            break
        print(' Tonyn ', end='')
        descuento = procesa_entrada(l1[i],1)
        puntosplayer2 -= descuentoTonyn.get(descuento,0)
        print('')
        if puntosplayer2 <= 0:
            break

#Salida final define el jugador ganador
if puntosplayer1 > puntosplayer2:
    print('Tonyn Gana la pelea y aun le queda', puntosplayer1, 'de energía')
else:
    print('Arnaldor Gana la pelea y aun le queda', puntosplayer2, 'de energía')

