# Se encarga de manejar las entradas del usuario muestra la imagen actual
# del juego

import pygame as p
from chess_assistant import Estado_Juego, Movimiento
from Clases import pieza, pawn, bishop, rook, queen, knight

#  Colores para el diseño

# Colores del tablero
white = p.Color("white")
brown = 0x01579b
#0xb88b5c

# Colores para movimientos permitidos
lightgreen = 0x81c784
green = 0x43a047

# Color para comer
yellow = p.Color("yellow")

# Colores para movimientos no permitidos
red = 0xffab91
#f44336
darkred = p.Color("red") 
#0xf44336
#8b0000


p.init()  # Inicialización de pygame

# Variables que definen el tamaño del tablero (display)
alto = 512
ancho = 512
dimension = 8  # Porque un tablero de ajerez es 8x8
SQ_size = alto // dimension
max_FPS = 15  # Variable necesaria para la animacion del juego
imagenes = {}

# Se necesita que las imagenes del juego se carguen una sola vez, porque
# si no, se va laggear el juego
# Entonces, se inicializa un diccionario global que almacene las imagenes
# Este diccionario va a llamarse una sola vez en el main


def load_images():
    piezas = ["wP", "wR", "wN", "wB", "wK", "wQ"]
    piezas += ["bP", "bR", "bN", "bB", "bK", "bQ"]
    for pieza in piezas:
        imagen = p.image.load("imagenes/" + pieza + ".png")
        imagenes[pieza] = p.transform.scale(imagen, (SQ_size, SQ_size))

# El driver principal del código, se encarga de recibir las entradas del
# usuario y de actualizar los graficos

def main():
    screen = p.display.set_mode((ancho, alto))  # Genera el display
    reloj = p.time.Clock() 
    #screen.fill(p.Color("white")) 
    screen.fill(white)
    juego = Estado_Juego() 
    array = []
    array2 = []
    load_images()
    running = True
    cuadro_selec = ()  # Tupla (fila, columna) que Va a iniciar vacía,
    # porque no hay ningún cuadro seleccionado, además, guarda la
    # información del último click del usuario
    historial_clicks = []  # 2 Tuplas (fila, columna) que guardan la
    # información de donde el usuario hizo click. EJ: [(6,4),(4,4),...]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:  # Detecta click del mouse
                ubicacion_mouse = p.mouse.get_pos()  # Posición (x,y) del mouse
                # Variables para obtener la fila y la columna donde está el
                # mouse y cual pieza se eligió
                columna = ubicacion_mouse[0]//SQ_size
                fila = ubicacion_mouse[1]//SQ_size

                # De aca en adelante corre si ya se tienen los dos clicks

                # Caso en que haya seleccionado el mismo cuadro 2 veces
                if cuadro_selec == (fila, columna):
                    cuadro_selec = ()  # Se "deselecciona" el cuadro (Vacío)
                    historial_clicks = []  # Se limpia el historial de clicks
                else:
                    # Caso en el que se seleccione un cuadro diferente,
                    # se guarda en cuadro_selec y se agrega la información del
                    # primer (casilla en la que está la pieza que quiere mover
                    # y segundo click (casilla a la que quiere mover la pieza)
                    cuadro_selec = (fila, columna)
                    if juego.board[fila][columna] != "--" or len(historial_clicks) == 1:
                        historial_clicks.append(cuadro_selec)
                    if len(historial_clicks) == 1:
                        objeto1 = CrearObjeto(historial_clicks[0], juego.board)
                        array = objeto1.cas_avail
                        array2 = objeto1.cas_take
                if len(historial_clicks) == 2:
                    # Aquí ya podemos hacer el movimiento
                    # Se va a ingresar toda la información del movimiento en
                    # una clase específica, para que se pueda acceder y llevar
                    # un mejor control de las jugadas
                    # mov_in = historial_clicks[0]
                    # mov_fin = historial_clicks[1]
                    # Clase que controla las jugadas
                    if Valida(historial_clicks, objeto1.cas_avail, objeto1.cas_take):
                        mov_in = historial_clicks[0]
                        mov_fin = historial_clicks[1]
                        mov = Movimiento(mov_in, mov_fin, juego.board)
                        # Mustra la notación del movimiento
                        print(mov.Notacion_chess())
                        juego.Jugada(mov)
                        # Se resetean las variables que guardan el último click
                        # del usuario y el historial de clicks
                        cuadro_selec = ()
                        historial_clicks = []
                    else:
                        cuadro_selec = ()
                        historial_clicks = []
        Dibujo_Estado_Juego(screen, juego, array, array2, historial_clicks)
        reloj.tick(max_FPS)
        p.display.flip()


# Función responsable de mostrar la interfaz
def Dibujo_Estado_Juego(screen, juego, cas_avail, cas_take, historial_clicks):
    Dibuja_Tablero(screen)  # Dibuja los cuadritos del tablero
    if len(historial_clicks) == 1:
        Posibles(screen, cas_avail, cas_take)
        Movimientos_Invalidos(screen, cas_avail, cas_take)
    Dibuja_Piezas(screen, juego.board)


# Dibuja los cuadrados del tablero en el orden de aparición en la interfaz
def Dibuja_Tablero(screen):
    colores = [white, brown]
    for f in range(dimension):  # f: fila
        for c in range(dimension):  # c: columna
            color = colores[((f+c) % 2)]
            left = c * SQ_size
            top = f * SQ_size
            p.draw.rect(screen, color, p.Rect(left, top, SQ_size, SQ_size))

def Movimientos_Invalidos(screen, cas_avail, cas_take):
    colores = [red, darkred]
    for f in range(dimension):  # f: fila
        for c in range(dimension):  # c: columna
            color = colores[((f+c) % 2)]
            left = c * SQ_size
            top = f * SQ_size
            if not ((f, c) in cas_avail or (f, c) in cas_take):
                p.draw.rect(screen, color, p.Rect(left, top, SQ_size, SQ_size))

# Muestra las piezas en el tablero usando el Estado_Juego actual (clase board)
def Dibuja_Piezas(screen, board):
    for f in range(dimension):  # f:fila
        for c in range(dimension):  # c:columna
            pieza = board[f][c]
            rectangulo = p.Rect(c * SQ_size, f * SQ_size, SQ_size, SQ_size)
            if pieza != "--":  # o es un espacio vacío
                screen.blit(imagenes[pieza], rectangulo)


# Verifica que la combinación entre la primera posición escogida y la segunda sea válida
def Valida(historial_clicks, cas_avail, cas_take):
    if historial_clicks[1] in cas_avail or historial_clicks[1] in cas_take:
        return True


# Esta función va a mostrar de color verde claro los posibles movimientos que pueden realizar las piezas
def Posibles(screen, cas_avail, cas_take):
    colores = [lightgreen, green]
    for f in range(dimension):  # f: fila
        for c in range(dimension):  # c: columna
            color = colores[((f+c) % 2)]
            left = c * SQ_size
            top = f * SQ_size
            if (f, c) in cas_avail or (f, c) in cas_take:
                p.draw.rect(screen, color, p.Rect(left, top, SQ_size, SQ_size))
    """color = green
    for i in range(len(cas_avail)):
        left = cas_avail[i][1]*SQ_size  # Con left y top define las posición de la casilla a la que se puede mover inicialmente
        top = cas_avail[i][0]*SQ_size
        p.draw.rect(screen, color, p.Rect(left, top, SQ_size, SQ_size))"""
    color = yellow
    for i in range(len(cas_take)):
        left = cas_take[i][1]*SQ_size  # Con left y top define las posición de la casilla a la que se puede mover inicialmente
        top = cas_take[i][0]*SQ_size
        p.draw.rect(screen, color, p.Rect(left, top, SQ_size, SQ_size))


# Verifica cual pieza es la casilla escogida y crea un objeto
def CrearObjeto(Primer_click, board):
    color = board[Primer_click[0]][Primer_click[1]][0]
    fila = Primer_click[0]
    col = Primer_click[1]
    if board[Primer_click[0]][Primer_click[1]][1] == "P":
        objeto = pawn("P", color, fila, col, [], [], board)
    elif board[Primer_click[0]][Primer_click[1]][1] == "B":
        objeto = bishop("B", color, fila, col, [], [], board)
    elif board[Primer_click[0]][Primer_click[1]][1] == "R":
        objeto = rook("R", color, fila, col, [], [], board)
    elif board[Primer_click[0]][Primer_click[1]][1] == "Q":
        objeto = queen("Q", color, fila, col, [], [], board)
    elif board[Primer_click[0]][Primer_click[1]][1] == "N":
        objeto = knight("N", color, fila, col, [], [], board)
    return objeto

# Para que se ejecute solo cuando corro este archivo.py
if __name__ == "__main__":
    main()