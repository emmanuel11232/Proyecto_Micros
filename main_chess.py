import copy
import pygame as p
from chess_assistant import Estado_Juego, Movimiento, Estado_promotion_b
from chess_assistant import Estado_promotion_w, cambiar_board
from Clases import pawn, bishop, rook, queen, knight, king
import random


# Colores del tablero
white = p.Color("white")
blue = 0x01579b
# Colores para movimientos permitidos
lightgreen = 0x81c784
green = 0x43a047
# Color para comer
yellow = p.Color("yellow")
# Colores para movimientos no permitidos
red = 0xffab91
darkred = p.Color("red")

# Color de texto
black = p.Color("black")

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
    random.seed()
    running = True
    TurnoPC = False
    cas_disp = []  # Se usa para pintar verde
    cas_tomar = []  # Se usa para pintar amarillo
    primerMovimiento = [1, 1, 1, 1, 1, 1]  # Matriz que define si ya se
    # movieron por primera vez las piezas relacionadas con el enroque.
    historial_mov = [(0, 0), (0, 0)]  # Guarda el último movimiento válido.
    jaque = "-"  # "-": no jaque, 1 en jaque blanco, 2 en jaque`` negro
    jaquemate = False
    cuadro_selec = ()  # Tupla (fila, columna) que Va a iniciar vacía,
    # porque no hay ningún cuadro seleccionado, además, guarda la
    # información del último click del usuario
    historial_clicks = []  # 2 Tuplas (fila, columna) que guardan la
    # información de donde el usuario hizo click. EJ: [(6,4),(4,4)]
    juego = Estado_Juego()
    casilla_reyenjaque = []
    # Variables globales para indicarle al usuario los errores de movimientos
    font_error = p.font.Font('freesansbold.ttf', 25)
    error = " "

    # Tiene que ver con pygame
    screen = p.display.set_mode((ancho, alto))  # Genera el display
    reloj = p.time.Clock()
    screen.fill(white)
    load_images()


    # "inicia" define el color inicial, se define el tablero y primerMovimiento
    inicia, juego.board, primerMovimiento = AsignarTablero(juego.board, primerMovimiento)
    equipo, vsPC = EscogerModo()  # Equipo define con quien juega el usuario
    # y vsPC el modo de juego.
    color = equipo  # Color controla cual equipo puede mover en el turno.
    # Si el color que inicia no es el del color válido para este turno entra.
    if inicia != color:
        # Si se juega contra PC, entonces juega primero la PC.
        if vsPC:
            TurnoPC = True
        # Cambia el color del turno al opuesto.
        if color == "w":
            color = "b"
        else:
            color = "w"
    if color == "b": coloratacante = "w"
    else: coloratacante = "b"
    jaque = check(juego.board, coloratacante, historial_mov, primerMovimiento)
    if jaque != "-":
        jaquemate = checkmate(juego.board, historial_mov, primerMovimiento, coloratacante)
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Detecta click del mouse
            elif (e.type == p.MOUSEBUTTONDOWN or (vsPC and TurnoPC)) and not jaquemate:
                if not TurnoPC:
                    # Se limpia el mensaje de error en un movimiento
                    # de la interfaz
                    error = " "
                    mensaje = font_error.render(error, True, p.Color("red"))
                    screen.blit(mensaje, (0, 240))
                    
                    ubicacion_mouse = p.mouse.get_pos()  # Posición (x,y) del mouse
                    # Variables para obtener la fila y la columna donde está el
                    # mouse y cual pieza se eligió
                    columna = ubicacion_mouse[0]//SQ_size
                    fila = ubicacion_mouse[1]//SQ_size

                    # Arregla el bug, cuando se escoge justo el límite de
                    # la pantalla y se sale del rango la elección.
                    if columna == 8:
                        columna = 7
                    if fila == 8:
                        fila = 7

                    # Caso en que haya seleccionado el mismo cuadro 2 veces
                    if cuadro_selec == (fila, columna):
                        cuadro_selec = ()  # Se "deselecciona" el cuadro.
                        historial_clicks = []  # Se limpia el historial0.

                    # Caso en el que se seleccione un cuadro diferente, o no
                    # se haya seleccionado ninguno aún.
                    else:
                        cuadro_selec = (fila, columna)

                        # Si se escoge una casilla no vacía o ya se tenía un
                        # click, se procede a guardar el cuadro en el
                        # historial de clicks
                        if juego.board[fila][columna] != "--" or len(historial_clicks) == 1:
                            historial_clicks.append(cuadro_selec)

                    # Si sólo se tiene seleccionada la pieza con el 1er click
                    # Se crea un objeto con los atributos de la pieza escogida
                    # Guarda cas_disp y cas_tomar que son necesarias para
                    # pintar el tablero.
                        if len(historial_clicks) == 1:
                            casilla_reyenjaque, objeto1 = CrearObjeto(
                                historial_clicks[0], juego.board, historial_mov, primerMovimiento)
                            cas_disp = objeto1.cas_avail
                            cas_tomar = objeto1.cas_take
                else:  # Si es el turno de la PC
                    escoge = True
                    # Procede a escoger una casilla random de todo el tablero
                    while escoge:
                        pcfila = random.randint(0, 7)
                        pccol = random.randint(0, 7)
                        # Procede, si la casilla no está vacía y es del equipo,
                        # del PC a crear un objeto de esa casilla y con esto
                        # escoger de sus casillas disponibles(si tiene) o de
                        # casillas por comer(si tiene) un movimiento, en
                        # caso de no tener ninguna, escoge otra casilla
                        if (juego.board[pcfila][pccol] != "--" and juego.board[pcfila][pccol][0] != equipo):
                            historial_clicks.append((pcfila, pccol))
                            casilla_reyenjaque, objeto1 = CrearObjeto(
                                (pcfila, pccol), juego.board, historial_mov, primerMovimiento)
                            cas_disp = objeto1.cas_avail
                            cas_tomar = objeto1.cas_take
                            rand = random.randint(0, 1)
                            if (rand == 0 or cas_tomar == []) and cas_disp != []:
                                historial_clicks.append(
                                    random.choice(cas_disp))
                                escoge = False
                            elif rand == 1 and cas_tomar != []:
                                historial_clicks.append(
                                    random.choice(cas_tomar))
                                escoge = False
                            else:
                                historial_clicks = []
                # Si ya escogió hacia donde se quiere mover, se
                # entra a este condicional.
                if len(historial_clicks) == 2:
                    # El if corrobora que la combinación de las dos elecciones
                    # es válida, es decir, que es un movimiento legal.
                    if Valida(historial_clicks, historial_mov, juego.board, objeto1, color, primerMovimiento):
                        # Se utiliza la clase "Movimiento", que permite
                        # llevar un mejor orden, permite ver la notación.
                        mov_in = historial_clicks[0]
                        mov_fin = historial_clicks[1]
                        mov = Movimiento(mov_in, mov_fin, juego.board)
                        print(mov.Notacion_chess())

                        # Almacena el movimiento que se acaba de hacer
                        # y se va a mantener ahí, hasta que se haga otro válido
                        historial_mov = (
                            historial_clicks[0], historial_clicks[1])

                        # Actualiza atributos del objeto, en caso de que se
                        # vaya a dar una promoción
                        if isinstance(objeto1, pawn):
                            objeto1.fila = mov_fin[0]
                            objeto1.col = mov_fin[1]
                            mov.pieza_movida = promotion(
                                objeto1, mov.pieza_movida)

                        # Se actualiza el tablero con la jugada
                        juego.Jugada(mov, objeto1)

                        # Modifica el arreglo de booleanas en caso de que
                        # se haya dado el primer movimiento en una de las
                        # piezas que afectan el enroque.
                        # REY BLANCO
                        primerMovimiento = primerMov(juego.board, primerMovimiento)

                        # Revisa si bajo las condiciones actuales, existe un
                        # jaque para el próximo equipo.
                        jaque = check(juego.board, color, historial_mov, primerMovimiento)

                        # Si hay check, entonces define cuál es la lista de
                        # movimientos válidos para el próximo equipo.
                        if jaque != "-":
                            jaquemate = checkmate(juego.board, historial_mov, primerMovimiento, color)
                        # Si se juega vsPC, se pasa el turno al oponente.
                        if vsPC:
                            TurnoPC = not TurnoPC

                        # Se cambia el color para que juegue el oponente ahora.
                        if color == "w":
                            color = "b"
                        else:
                            color = "w"

                    # Si el movimiento no fue válido:
                    else:
                        if historial_clicks[1] in casilla_reyenjaque:
                            error = "Inválido por rey en jaque"
                            print("Inválido por rey en jaque")
                        elif color != objeto1.color:
                            error = "No corresponde al turno"
                            print("No corresponde al turno")
                        else:
                            error = "Movimiento inválido para la pieza"
                            print("El movimiento no corresponde con la pieza")
                    # Se resetean las variables que guardan el último click
                    # del usuario y el historial de clicks.
                    cuadro_selec = ()
                    historial_clicks = []
            # Función de saltar turno
            elif (e.type == p.KEYDOWN) and not jaquemate:
                # Invierte el color al que le toca jugar y en caso de estar
                # jugando contra la PC, le da el turno a la PC de nuevo.
                if e.key == p.K_s:
                    if color == "w":
                        color = "b"
                    else:
                        color = "w"
                    if not TurnoPC and vsPC:
                        TurnoPC = True

        # Se encarga de pintar en pantalla el tablero, así
        # como los colores correspondientes en las otras casillas
        Dibujo_Estado_Juego(screen, juego, cas_disp,
                            cas_tomar, historial_clicks)
        # Se imprimen en pantalla los mensajes de movimientos inválidos
        mensaje = font_error.render(error, True, p.Color("red"))
        mensaje1 = font_error.render(error, True, black)
        left = 150 - 2*len(error)
        screen.blit(mensaje1, (left-1, 239))
        screen.blit(mensaje1, (left+1, 241))
        screen.blit(mensaje, (left, 240))

        # Si se llega al jaque mate, lo muestra en pantalla hasta que
        # se salga de la ventana.
        if jaquemate:
            vsPC = False
            p.font.init()
            font = p.font.Font('freesansbold.ttf', 35)
            font2 = p.font.Font('freesansbold.ttf', 20)
            texto_fondo1 = font.render('Jaque Mate', True, p.Color("red"))
            texto_fondo2 = font.render('Jaque Mate', True, p.Color("green"))
            texto = font.render('Jaque Mate', True, black)
            if jaque == 1:
                texto2_fondo = font2.render('Gana negro', True, p.Color("red"))
                texto2_fondo1 = font2.render('Gana negro', True, p.Color("green"))
                texto2 = font2.render('Gana negro', True, black)
                screen.blit(texto2_fondo, (181, 241))
                screen.blit(texto2_fondo1, (179, 239))
                screen.blit(texto2, (180, 240))
            else:
                texto2_fondo = font2.render('Gana blanco', True, p.Color("red"))
                texto2_fondo1 = font2.render('Gana blanco', True, p.Color("green"))
                texto2 = font2.render('Gana blanco', True, black)
                screen.blit(texto2_fondo, (181, 241))
                screen.blit(texto2_fondo1, (179, 239))
                screen.blit(texto2, (180, 240))
            screen.blit(texto_fondo1, (151, 201))
            screen.blit(texto_fondo2, (149, 199))
            screen.blit(texto, (150, 200))
        reloj.tick(max_FPS)
        p.display.flip()


# Revisa si el movimiento que se acaba de realizar afecta a la
# matriz de primerMovimiento.
def primerMov(board, primerMovimiento):
    if board[7][4] == "--" and primerMovimiento[0]:
        primerMovimiento[0] = 0
    # REY NEGRO
    if board[0][4] == "--" and primerMovimiento[1]:
        primerMovimiento[1] = 0
    # TORRE BLANCA DERECHA
    if board[7][7] == "--" and primerMovimiento[2]:
        primerMovimiento[2] = 0
    # TORRE BLANCA IZQUIERDA
    if board[7][0] == "--" and primerMovimiento[3]:
        primerMovimiento[3] = 0
    # TORRE NEGRA DERECHA
    if board[0][7] == "--" and primerMovimiento[4]:
        primerMovimiento[4] = 0
    # TORRE NEGRA IZQUIERDA
    if board[0][0] == "--" and primerMovimiento[5]:
        primerMovimiento[5] = 0
    return primerMovimiento


def EscogerModo():
    equipo = "w"
    altotemp = 256
    anchotemp = 512
    dimension_temp = 2
    SQ_size_temp = anchotemp // dimension_temp
    screen1 = p.display.set_mode((anchotemp, altotemp))  # Genera el display
    reloj1 = p.time.Clock()
    screen1.fill(white)

    # Carga las imágenes desde la carpeta y las escala
    img1 = p.image.load("imagenes/" + "PC" + ".png")
    img2 = p.image.load("imagenes/" + "Asistente" + ".png")
    img1 = p.transform.scale(img1, (SQ_size_temp, SQ_size_temp))
    img2 = p.transform.scale(img2, (SQ_size_temp*0.9, SQ_size_temp*0.55))

    # Se genera un rectangulo para poner la imagen encima
    rectangulo1 = p.Rect(15, 65, SQ_size_temp, SQ_size_temp)

    # Se generan dos rectangulos para pintar el fondo
    rectangulo2 = p.Rect(0, 0, SQ_size_temp, SQ_size_temp)
    rectangulo3 = p.Rect(SQ_size_temp, 0, SQ_size_temp, SQ_size_temp)
    p.draw.rect(screen1, "white", rectangulo2)
    p.draw.rect(screen1, "blue", rectangulo3)

    # Pinta las imágenes
    screen1.blit(img1, rectangulo3)
    screen1.blit(img2, rectangulo1)

    # Se le hace flip a la pantalla
    reloj1.tick(max_FPS)
    p.display.flip()
    corriendo = True

    # Se obtiene cuál fue la selección del usuario y se retorna
    while corriendo:
        ubicacion_mouse1 = p.mouse.get_pos()
        colum = int(ubicacion_mouse1[0]//SQ_size_temp)
        for e in p.event.get():
            if e.type == p.QUIT:
                corriendo = False
            elif e.type == p.MOUSEBUTTONDOWN:
                colum = int(ubicacion_mouse1[0]//SQ_size_temp)
                corriendo = False
    if colum:
        equipo = escogerequipo()
    screen1 = p.display.set_mode((ancho, alto))
    bool(colum)
    return equipo, colum


# Función encargada de realizar la coronación del pawn.
# Recibe a los atributos de la pieza actual para comprobar
# que cumple con las condiciones para realizar el promotion
def promotion(objeto2, mov):

    # Comprueba que la pieza se encuentre en las dos únicas filas posibles
    # para realizar la coronación, es decir, la última fila posible para
    # cada uno de los pawn de ambos lados del tablero.
    # La función, en caso de cumplirse las condiciones, retorna la pieza
    # seleccionada por el usuario y en caso de no cumplirse, se retorna
    # la pieza original y no se refleja ningún cambio.
    if objeto2.fila == 0 or objeto2.fila == 7:
        # Se comprueba que la pieza sea un pawn
        if objeto2.tipo == "P":
            # Variables definen el tamaño de la interfaz de selección temporal
            altotemp = 256
            anchotemp = 256

            screen1 = p.display.set_mode(
                (anchotemp, altotemp+64))  # Genera el display con las dimensiones dadas
            reloj1 = p.time.Clock()
            screen1.fill(white)

            p.font.init()
            font = p.font.Font('freesansbold.ttf', 16)
            texto = font.render(
                'Seleccione la pieza deseada', True, black, white)
            screen1.blit(texto, (16, 288))

            # Determina el color de la pieza que está realizando la coronación,
            # para generar una interfaz de selección acorde al color.
            # Genera un "tablero" temporal de selección.
            if objeto2.color == "w":
                seleccion = Estado_promotion_w()
            else:
                seleccion = Estado_promotion_b()

            # Se inicializa el ciclo de estado que espera a la selección de la nueva pieza
            promoted = True
            dimension_temp = 2  # Es 2 ya que se va a generar una tablero de 2x2
            SQ_size_temp = anchotemp // dimension_temp  # Se define la escala

            # Carga las imágenes desde la carpeta y las escala
            imagenesG = {}
            piezas = ["wR", "wN", "wB", "wQ"]
            piezas += ["bR", "bN", "bB", "bQ"]
            for pieza in piezas:
                imagen = p.image.load("imagenes/" + pieza + ".png")
                imagenesG[pieza] = p.transform.scale(
                    imagen, (SQ_size_temp, SQ_size_temp))

            while promoted:

                # Detecta click del mouse
                ubicacion_mouse1 = p.mouse.get_pos()

                # Variables para obtener la fila y la columna donde está el
                # mouse y cual pieza se eligió
                colum = int(ubicacion_mouse1[0]//SQ_size_temp)
                fil = int(ubicacion_mouse1[1]//SQ_size_temp)

                for e in p.event.get():

                    # Espera a que el usuario dé click dentro del rango de selección
                    if e.type == p.MOUSEBUTTONDOWN and ubicacion_mouse1[1] <= 256:
                        # Regresa a la pantalla a las dimensiones originales y retorna
                        # la pieza del tablero temporal de selección
                        # que coincida con la fila y columna seleccionada por el usuario
                        screen1 = p.display.set_mode((ancho, alto))
                        return seleccion.board[fil][colum]

                colores = [white, blue]
                for f in range(dimension_temp):  # f: fila
                    for c in range(dimension_temp):  # c: columna
                        if colum == c and fil == f:
                            color = green
                        else:
                            color = colores[((f+c) % 2)]
                        left = c * SQ_size_temp
                        top = f * SQ_size_temp
                        p.draw.rect(screen1, color, p.Rect(
                            left, top, SQ_size_temp, SQ_size_temp))
                for f in range(dimension_temp):  # f:fila
                    for c in range(dimension_temp):  # c:columna
                        pieza1 = seleccion.board[f][c]
                        rectangulo1 = p.Rect(
                            c * SQ_size_temp, f * SQ_size_temp, SQ_size_temp, SQ_size_temp)
                        screen1.blit(imagenesG[pieza1], rectangulo1)
                reloj1.tick(max_FPS)
                p.display.flip()
        else:
            return mov
    else:
        return mov


# Función responsable de mostrar la interfaz
def Dibujo_Estado_Juego(screen, juego, cas_avail, cas_take, historial_clicks):
    # Dibuja los cuadros del tablero.
    Dibuja_Tablero(screen)

    # Si ya se seleccionó una casilla, se pintan los movimientos
    # válidos en verde o amarillo (si es posible comer) y los
    # inválidos en rojo.
    if len(historial_clicks) == 1:
        Posibles(screen, cas_avail, cas_take)
        Movimientos_Invalidos(screen, cas_avail, cas_take)

    # Dibuja las piezas encima del tablero pintado anteriormente.
    Dibuja_Piezas(screen, juego.board)


# Dibuja los cuadrados del tablero en el orden de aparición en la interfaz
def Dibuja_Tablero(screen):
    colores = [white, blue]
    for f in range(dimension):  # f: fila
        for c in range(dimension):  # c: columna
            color = colores[((f+c) % 2)]
            left = c * SQ_size
            top = f * SQ_size
            p.draw.rect(screen, color, p.Rect(left, top, SQ_size, SQ_size))


# Toma las casillas disponibles para moverse y comer, y pinta de rojo
# todas las que no son estas.
def Movimientos_Invalidos(screen, cas_avail, cas_take):
    colores = [red, darkred]
    for f in range(dimension):  # f: fila
        for c in range(dimension):  # c: columna
            color = colores[((f+c) % 2)]
            left = c * SQ_size
            top = f * SQ_size
            if not ((f, c) in cas_avail or (f, c) in cas_take):
                p.draw.rect(screen, color, p.Rect(left, top, SQ_size, SQ_size))


# Muestra las piezas en el tablero usando el Estado_Juego actual (class board)
def Dibuja_Piezas(screen, board):
    for f in range(dimension):  # f:fila
        for c in range(dimension):  # c:columna
            pieza = board[f][c]
            rectangulo = p.Rect(c * SQ_size, f * SQ_size, SQ_size, SQ_size)
            if pieza != "--":  # No es un espacio vacío.
                screen.blit(imagenes[pieza], rectangulo)


# Esta función va a mostrar de color verde claro los posibles
# movimientos que pueden realizar las piezas
def Posibles(screen, cas_avail, cas_take):
    colores = [lightgreen, green]
    for f in range(dimension):  # f: fila
        for c in range(dimension):  # c: columna
            color = colores[((f+c) % 2)]
            left = c * SQ_size
            top = f * SQ_size
            if (f, c) in cas_avail or (f, c) in cas_take:
                p.draw.rect(screen, color, p.Rect(left, top, SQ_size, SQ_size))
    color = yellow
    for i in range(len(cas_take)):
        left = cas_take[i][1]*SQ_size  # Define la fila
        top = cas_take[i][0]*SQ_size  # Define la columna
        p.draw.rect(screen, color, p.Rect(left, top, SQ_size, SQ_size))


# Verifica que la combinación entre la primera posición escogida
# y la segunda sea válida, también se encarga de llevar los turnos puesto que
# sólo permite que sean intercalados y con blanco de primero.
def Valida(historial_clicks, historial_mov, board, objeto, color, primerMovimiento):
    juego_temporal = Estado_Juego()
    # Si la casilla escogida es una disponible, o una donde se puede comer y
    # además es el turno de las piezas de ese color, se permite el movimiento
    if (historial_clicks[1] in objeto.cas_avail or (historial_clicks[1] in objeto.cas_take)) and (color == objeto.color):
        # Verifica si es peón para corroborar una posible comida al paso
        if isinstance(objeto, pawn):
            if historial_clicks[1] == objeto.cuadro_alpaso:
                board[historial_mov[1][0]][historial_mov[1][1]] = "--"
        juego_temporal.board = copy.deepcopy(board)
        mov = Movimiento((objeto.fila, objeto.col),
                         (historial_clicks[1][0], historial_clicks[1][1]), juego_temporal.board)
        juego_temporal.Jugada(mov, objeto)
        # Define a cual rey se le va a consultar el jaque
        if historial_mov != ():
            color = board[historial_mov[1][0]][historial_mov[1][1]][0]
        else:
            color = "w"
        if check(juego_temporal.board, color, historial_mov, primerMovimiento) == 1 and color == "w":
            return False
        elif check(juego_temporal.board, color, historial_mov, primerMovimiento) == 2 and color == "b":
            return False
        return True


# Verifica cual pieza es la casilla escogida y crea un objeto
def CrearObjeto(Primer_click, board, historial_mov, primerMovimiento):
    juego_temporal = Estado_Juego()  # Para revisar check en posibles movs.
    color = board[Primer_click[0]][Primer_click[1]][0]
    casilla_reyenjaque = []
    if color == "w":
        coloratacante = "b"
    else:
        coloratacante = "w"
    fila = Primer_click[0]
    col = Primer_click[1]
    # Cada uno de los condicionales revisa que tipo de pieza escogió el usuario
    # y crea un objeto con los atributos que pide dicha clase
    if board[Primer_click[0]][Primer_click[1]][1] == "P":
        objeto = pawn("P", color, fila, col, [], [], board, historial_mov)
    elif board[Primer_click[0]][Primer_click[1]][1] == "B":
        objeto = bishop("B", color, fila, col, [], [], board)
    elif board[Primer_click[0]][Primer_click[1]][1] == "R":
        objeto = rook("R", color, fila, col, [], [], board)
    elif board[Primer_click[0]][Primer_click[1]][1] == "Q":
        objeto = queen("Q", color, fila, col, [], [], board)
    elif board[Primer_click[0]][Primer_click[1]][1] == "N":
        objeto = knight("N", color, fila, col, [], [], board)
    elif board[Primer_click[0]][Primer_click[1]][1] == "K":
        objeto = king("K", color, fila, col, [], [], board, primerMovimiento)
    # Se asegura de que las posiciones disponibles no caerían en un jaque dado
    # por el otro rey, esto se revisa aquí y no en la clase porque
    # habría una recursividad infinita.
        for a in range(8):
            for b in range(8):
                if color != board[a][b][0] and board[a][b][1] == "K":
                    for filareyenemigo in [-1, 0, 1]:
                        for colreyenemigo in [-1, 0, 1]:
                            casilla = (a + filareyenemigo, b + colreyenemigo)
                            if casilla in objeto.cas_take:
                                objeto.cas_take.remove(casilla)
                            if casilla in objeto.cas_avail:
                                objeto.cas_avail.remove(casilla)
    quitar1 = []  # Esta lista representa las movidas que ponen en check al rey
    for disponible in objeto.cas_avail:
        juego_temporal.board = copy.deepcopy(board)
        mov = Movimiento(
            (objeto.fila, objeto.col), disponible, juego_temporal.board)
        juego_temporal.Jugada(mov, objeto)
        if (check(juego_temporal.board, coloratacante, historial_mov,
                  primerMovimiento) != "-"):
            quitar1.append(disponible)
    for h in quitar1:
        objeto.cas_avail.remove(h)

    quitar2 = []  # Esta lista representa las comidas que ponen en check al rey
    for disponible in objeto.cas_take:
        juego_temporal.board = copy.deepcopy(board)
        mov = Movimiento(
            (objeto.fila, objeto.col), disponible, juego_temporal.board)
        juego_temporal.Jugada(mov, objeto)
        if (check(juego_temporal.board, coloratacante, historial_mov,
                  primerMovimiento) != "-"):
            quitar2.append(disponible)
    for h in quitar2:
        objeto.cas_take.remove(h)
    casilla_reyenjaque += quitar1 + quitar2
    return casilla_reyenjaque, objeto


# Esta función simplemente revisa si alguna pieza está atacando al rey
def check(board, color, historial_mov, primerMovimiento):
    total_take = []
    a = 0
    b = 0
    # Va casilla por casilla del tablero.
    for a in range(8):
        for b in range(8):
            # En caso de que la pieza sea del color que puede atacar al rey,
            # se procede a crear un objeto con dicha pieza y verificar si
            # dentro de las casillas en las que puede comer, está la del rey
            if color == board[a][b][0]:
                if board[a][b][1] == "P":
                    objeto = pawn("P", board[a][b][0],
                                  a, b, [], [], board, historial_mov)
                elif board[a][b][1] == "B":
                    objeto = bishop("B", board[a][b][0], a, b, [], [], board)
                elif board[a][b][1] == "R":
                    objeto = rook("R", board[a][b][0], a, b, [], [], board)
                elif board[a][b][1] == "Q":
                    objeto = queen("Q", board[a][b][0], a, b, [], [], board)
                elif board[a][b][1] == "N":
                    objeto = knight("N", board[a][b][0], a, b, [], [], board)
                elif board[a][b][1] == "K":
                    objeto = king("K", color, a, b, [], [], board, primerMovimiento)
                if board[a][b] != "--":
                    if objeto.cas_take != []:
                        for t in objeto.cas_take:
                            if t not in total_take:
                                total_take.append(t)
            # Se guardan las coordenadas del rey, para verificar si
            # en efecto está en jaque.
            elif board[a][b][1] == "K":
                fila_rey = a
                col_rey = b
    # Si alguna pieza lo ataca, se marca como Jaque.
    if (fila_rey, col_rey) in total_take:
        if color == "w":
            return 2
        elif color == "b":
            return 1
    else:
        return "-"


# Revisa el checkmate
def checkmate(board, historial_mov, primerMovimiento, color):
    # Si el rey está siendo atacado y no se puede salvar sólo, jaque mate.
    ValidosenCheck = MovValidosCheck(board, historial_mov, primerMovimiento, color)
    if (check(board, color, historial_mov, primerMovimiento) != "-") and ValidosenCheck == []:
        return True
    else:
        return False


# Esta función se llama desde la función de checkmate y crea un arreglo con
# todos los posibles movimientos que se pueden realizar una vez
# que se está en jaque.
def MovValidosCheck(board, historial_mov, primerMovimiento, color):
    juego_temporal = Estado_Juego()
    ValidosenCheck = []
    a = 0
    b = 0
    for a in range(8):
        for b in range(8):
            if color != board[a][b][0]:
                if board[a][b][1] == "P":
                    objeto = pawn("P", board[a][b][0],
                                  a, b, [], [], board, historial_mov)
                elif board[a][b][1] == "B":
                    objeto = bishop("B", board[a][b][0], a, b, [], [], board)
                elif board[a][b][1] == "R":
                    objeto = rook("R", board[a][b][0], a, b, [], [], board)
                elif board[a][b][1] == "Q":
                    objeto = queen("Q", board[a][b][0], a, b, [], [], board)
                elif board[a][b][1] == "N":
                    objeto = knight("N", board[a][b][0], a, b, [], [], board)
                elif board[a][b][1] == "K":
                    objeto = king("K", board[a][b][0], a, b, [
                    ], [], board, primerMovimiento)
                if board[a][b] != "--":
                    for disponible in objeto.cas_avail:
                        juego_temporal.board = copy.deepcopy(board)
                        mov = Movimiento(
                            (objeto.fila, objeto.col), disponible, juego_temporal.board)
                        juego_temporal.Jugada(mov, objeto)
                        if not (check(juego_temporal.board, color, historial_mov, primerMovimiento) != "-"):
                            jugada = ((objeto.fila, objeto.col), (disponible))
                            ValidosenCheck.append(jugada)
                    for disponible in objeto.cas_take:
                        juego_temporal.board = copy.deepcopy(board)
                        mov = Movimiento(
                            (objeto.fila, objeto.col), disponible, juego_temporal.board)
                        juego_temporal.Jugada(mov, objeto)
                        if not (check(juego_temporal.board, color, historial_mov, primerMovimiento) != "-"):
                            jugada = ((objeto.fila, objeto.col), (disponible))
                            ValidosenCheck.append(jugada)
    return ValidosenCheck


def AsignarTablero(board, primerMovimiento1):
    inicia = "w"
    altotemp = 256
    anchotemp = 512
    dimension_temp = 2
    SQ_size_temp = anchotemp // dimension_temp
    screen1 = p.display.set_mode((anchotemp, altotemp))  # Genera el display
    reloj1 = p.time.Clock()
    screen1.fill(white)

    # Carga las imágenes desde la carpeta y las escala
    img1 = p.image.load("imagenes/" + "Asignar" + ".png")
    img2 = p.image.load("imagenes/" + "Basic" + ".png")
    img1 = p.transform.scale(img1, (SQ_size_temp//2, SQ_size_temp//2))
    img2 = p.transform.scale(img2, (SQ_size_temp//2, SQ_size_temp//2))

    # Se genera un rectangulo para poner la imagen encima
    rectangulo1 = p.Rect(64, 64, SQ_size_temp, SQ_size_temp)
    rectangulo2 = p.Rect(320, 64, SQ_size_temp, SQ_size_temp)

    # Se generan dos rectangulos para pintar el fondo
    rectangulo3 = p.Rect(0, 0, SQ_size_temp, SQ_size_temp)
    rectangulo4 = p.Rect(SQ_size_temp, 0, SQ_size_temp, SQ_size_temp)
    p.draw.rect(screen1, "white", rectangulo3)
    p.draw.rect(screen1, "blue", rectangulo4)

    # Pinta las imágenes
    screen1.blit(img1, rectangulo2)
    screen1.blit(img2, rectangulo1)

    # Se le hace flip a la pantalla
    reloj1.tick(max_FPS)
    p.display.flip()
    corriendo = True

    # Se obtiene cuál fue la selección del usuario y se retorna
    while corriendo:
        ubicacion_mouse1 = p.mouse.get_pos()
        colum = int(ubicacion_mouse1[0]//SQ_size_temp)
        for e in p.event.get():
            if e.type == p.QUIT:
                corriendo = False
            elif e.type == p.MOUSEBUTTONDOWN:
                colum = int(ubicacion_mouse1[0]//SQ_size_temp)
                corriendo = False
    screen1 = p.display.set_mode((ancho, alto))
    if colum == 1:
        inicia = quieninicia()
        board, primerMovimiento1 = cambiarBoard(board, primerMovimiento1)
    return inicia, board, primerMovimiento1


# Permite definir el tablero inicial, en caso de que no sea el inicial.
def cambiarBoard(board, primerMovimiento_temp):
    load_images()
    altotemp = 640
    anchotemp = 512
    dimension_temp = 10  # Se define una matriz de 10x10, para
    # adjuntar el área de selección de piezas
    SQ_size_temp = altotemp // dimension_temp
    screen1 = p.display.set_mode((anchotemp, altotemp))  # Genera el display
    reloj1 = p.time.Clock()
    screen1.fill(white)
    cuadro_selec_temp = ()
    historial_clicks_temp = []
    z = False
    promotion_w_disponible = True
    promotion_b_disponible = True
    tp = "--"
    asignando = True

    # Se inicializan las variables que
    # que controlan la cantidad máxima de cada tipo de pieza que
    #  se puede colocar.
    num_pawns_w = 0
    num_pawns_b = 0
    num_bishops_w = 0
    num_bishops_b = 0
    num_rook_w = 0
    num_rook_b = 0
    num_knights_w = 0
    num_knights_b = 0
    num_queen_w = 0
    num_queen_b = 0
    num_king_w = 0
    num_king_b = 0

    # Se inicializa la variable que controla la cantidad de promociones que
    # se han realizado
    num_promotion_w = 0
    num_promotion_b = 0

    # Se genera un elemento de clase cambiar_board
    tablero_temporal = cambiar_board()

    # Se entra al ciclo infinito
    while asignando:
        for e in p.event.get():
            if e.type == p.QUIT:
                # El usuario solamente puede continuar si ya fueron colocados
                # ambos reyes en el tablero. El juego no puede iniciar
                # sin la presencia de ambos
                # if num_king_b == 1 and num_king_w == 1:
                asignando = False
                return board, primerMovimiento_temp
            elif e.type == p.KEYDOWN:
                if e.key == p.K_SPACE:
                    if num_king_b == 1 and num_king_w == 1:
                        asignando = False
                        return board, primerMovimiento_temp
            elif e.type == p.MOUSEBUTTONDOWN:
                ubicacion_mouse = p.mouse.get_pos()  # Posición (x,y) del mouse

                # Variables para obtener la fila y la columna donde está el
                # mouse y cual pieza se eligió
                columna = ubicacion_mouse[0]//SQ_size_temp
                fila = ubicacion_mouse[1]//SQ_size_temp

                # Caso en que haya seleccionado la misma pieza 2 veces
                if cuadro_selec_temp == (fila, columna):
                    if fila < 8:
                        tablero_temporal.board[fila][columna] = "--"  # Se elimina del tablero dicha pieza
                        # Se reinicia las variables de promocion
                        num_promotion_w = 0
                        num_promotion_b = 0
                        promotion_w_disponible = True
                        promotion_b_disponible = True
                        cuadro_selec_temp = ()  # Se "deselecciona" el cuadro (Vacío)
                        historial_clicks_temp = []  # Se limpia el historial de clicks

                # Caso en el que se seleccione un cuadro diferente, o no
                # se haya seleccionado ninguno aún.
                else:
                    cuadro_selec_temp = (fila, columna)

                    # Si se escoge una casilla no vacía o ya se tenía un
                    # click, se procede a guardar el cuadro en el
                    # historial de clicks
                    if tablero_temporal.board[fila][columna] != "--" or len(historial_clicks_temp) == 1:
                        historial_clicks_temp.append(cuadro_selec_temp)

                    # Si sólo se tiene seleccionada la pieza con el 1er click
                    # Se define que el origen será la pieza en la fila y columna
                    # seleccionadas
                    if len(historial_clicks_temp) == 1:
                        origen = tablero_temporal.board[historial_clicks_temp[0][0]][historial_clicks_temp[0][1]]

                    if len(historial_clicks_temp) == 2:

                        mov_in = historial_clicks_temp[0]
                        mov_fin = historial_clicks_temp[1]

                        # Se define que en condiciones normales,
                        # el destino será igual al origen
                        destino = origen

                        # Evita una sobreescritura en el caso en que el primer click del usuario
                        # se dio en el área del seleccionador y su segundo click intenta
                        # sobreescribir alguna de las piezas del seleccionador
                        if mov_in[0] > 7:
                            if mov_fin[0] > 7:
                                destino = tablero_temporal.board[mov_fin[0]][mov_fin[1]]
                                z = True

                        if mov_in[0] < 8:
                            # Evita una sobreescritura en el caso en que el primer click del usuario
                            # se dio en el área del tablero y su segundo click intenta
                            # sobreescribir alguna de las piezas del seleccionador
                            if mov_fin[0] == 8 or mov_fin[0] == 9:
                                destino = tablero_temporal.board[mov_fin[0]][mov_fin[1]]
                                z = True

                            # Si el usario da su segundo click en algún cuadro del tablero(esté vacío o no),
                            # se sobrepone y limpia el cuadro en el que estaba anteriormente
                            if (mov_fin[0] < 8):
                                origen = "--"

                        # Define las variables según el tipo, color de la pieza y posición
                        # que se está tratando de colocar desde el seleccionador.

                        if mov_fin[0] == 7 and mov_fin[1] == 4 and tablero_temporal.board[mov_in[0]][mov_in[1]] == "wK":
                            a = 7
                            b = 4
                            k = 0
                            tp = "wK"
                            # REY BLANCO

                        if mov_fin[0] == 0 and mov_fin[1] == 4 and tablero_temporal.board[mov_in[0]][mov_in[1]] == "bK":
                            a = 0
                            b = 4
                            k = 1
                            tp = "bK"
                            # REY NEGRO

                        if mov_fin[0] == 7 and mov_fin[1] == 7 and tablero_temporal.board[mov_in[0]][mov_in[1]] == "wR":
                            a = 7
                            b = 7
                            k = 2
                            tp = "wR"
                            # TORRE BLANCA DERECHA

                        if mov_fin[0] == 7 and mov_fin[1] == 0 and tablero_temporal.board[mov_in[0]][mov_in[1]] == "wR":
                            a = 7
                            b = 0
                            k = 3
                            tp = "wR"
                            # TORRE BLANCA IZQUIERDA

                        if mov_fin[0] == 0 and mov_fin[1] == 7 and tablero_temporal.board[mov_in[0]][mov_in[1]] == "bR":
                            a = 0
                            b = 7
                            k = 4
                            tp = "bR"
                            # TORRE NEGRA DERECHA

                        if mov_fin[0] == 0 and mov_fin[1] == 0 and tablero_temporal.board[mov_in[0]][mov_in[1]] == "bR":
                            a = 0
                            b = 0
                            k = 5
                            tp = "bR"
                            # TORRE NEGRA IZQUIERDA

                        # Según las variables, se determina el tipo de pieza que se coloca,
                        # las posicones en las que se está colocando y se pregunta si la pieza
                        # ya ha realizado algún movimiento
                        if tablero_temporal.board[mov_in[0]][mov_in[1]] == tp:
                            if mov_fin[0] == a and mov_fin[1] == b:
                                primerMovimiento_temp[k] = preguntaPrimerMov(anchotemp, altotemp)

                        # Se determina el si número de promociones que se han realizado
                        # ha superado la  cantidad de peones aún disponibles para
                        # colocar (7 - num_pawns_w). En caso de superarse dicho límite, la variable
                        # de promociones disponibles se inhabilitará. También se comprueba la cantidad máxima de peones.

                        if num_promotion_w > (7 - num_pawns_w):
                            promotion_w_disponible = False

                        if num_promotion_b > (7 - num_pawns_b):
                            promotion_b_disponible = False

                        # Se definen los valores máximos para las piezas
                        # para los casos en que la promocion esté o no
                        # disponible. Cuando se encuentra disponible, para
                        # los rook, bishop y knight se puede colocar un máximo de
                        # 10 piezas (2 por defecto + 8 promociones) y para la reina
                        # un maximo de 9 (1 por defecto + 8 promociones).
                        # Cuando no esté disponible, el límite serán los valores
                        # por defecto de 2 piezas para rook, bishop y knight y 1 pieza
                        # para la reina.

                        if promotion_w_disponible:
                            max_rbn_w = 9
                            max_q_w = 8
                        else:
                            max_rbn_w = 1
                            max_q_w = 0

                        if promotion_b_disponible:
                            max_rbn_b = 9
                            max_q_b = 8
                        else:
                            max_rbn_b = 1
                            max_q_b = 0

                        # Se comprueban varias condiciones para inhabilitar colocar una pieza.
                        # - Inicialmente, que la pieza de origen provenga de seleccionador.
                        # - Para el caso del peón, cuando la variable promotion esté inhabilitada, esto
                        # indica que ya se han colocado todos los peones + promociones disponibles.
                        # - Para rook, bishop, knight y queen se comprueba que no se exceda la cantidad
                        # posible según el estado de la variable de promotion definida.
                        # - Para el rey se comprueba que no exista más de 1 pieza.

                        if mov_in[0] > 7:
                            if not promotion_w_disponible and tablero_temporal.board[mov_in[0]][mov_in[1]] == "wP":
                                if tablero_temporal.board[mov_fin[0]][mov_fin[1]] == "--" or tablero_temporal.board[mov_fin[0]][mov_fin[1]][0] == "b":
                                    destino = tablero_temporal.board[mov_fin[0]][mov_fin[1]]
                                    z = True
                            if not promotion_b_disponible and tablero_temporal.board[mov_in[0]][mov_in[1]] == "bP":
                                if tablero_temporal.board[mov_fin[0]][mov_fin[1]] == "--" or tablero_temporal.board[mov_fin[0]][mov_fin[1]][0] == "w":
                                    destino = tablero_temporal.board[mov_fin[0]][mov_fin[1]]
                                    z = True
                            if num_rook_w > max_rbn_w and tablero_temporal.board[mov_in[0]][mov_in[1]] == "wR":
                                destino = tablero_temporal.board[mov_fin[0]][mov_fin[1]]
                                z = True
                            if num_rook_b > max_rbn_b and tablero_temporal.board[mov_in[0]][mov_in[1]] == "bR":
                                destino = tablero_temporal.board[mov_fin[0]][mov_fin[1]]
                                z = True
                            if num_bishops_w > max_rbn_w and tablero_temporal.board[mov_in[0]][mov_in[1]] == "wB":
                                destino = tablero_temporal.board[mov_fin[0]][mov_fin[1]]
                                z = True
                            if num_bishops_b > max_rbn_b and tablero_temporal.board[mov_in[0]][mov_in[1]] == "bB":
                                destino = tablero_temporal.board[mov_fin[0]][mov_fin[1]]
                                z = True
                            if num_knights_w > max_rbn_w and tablero_temporal.board[mov_in[0]][mov_in[1]] == "wN":
                                destino = tablero_temporal.board[mov_fin[0]][mov_fin[1]]
                                z = True
                            if num_knights_b > max_rbn_b and tablero_temporal.board[mov_in[0]][mov_in[1]] == "bN":
                                destino = tablero_temporal.board[mov_fin[0]][mov_fin[1]]
                                z = True
                            if num_queen_w > max_q_w and tablero_temporal.board[mov_in[0]][mov_in[1]] == "wQ":
                                destino = tablero_temporal.board[mov_fin[0]][mov_fin[1]]
                                z = True
                            if num_queen_b > max_q_b and tablero_temporal.board[mov_in[0]][mov_in[1]] == "bQ":
                                destino = tablero_temporal.board[mov_fin[0]][mov_fin[1]]
                                z = True
                            if num_king_w > 0 and tablero_temporal.board[mov_in[0]][mov_in[1]] == "wK":
                                destino = tablero_temporal.board[mov_fin[0]][mov_fin[1]]
                                z = True
                            if num_king_b > 0 and tablero_temporal.board[mov_in[0]][mov_in[1]] == "bK":
                                destino = tablero_temporal.board[mov_fin[0]][mov_fin[1]]
                                z = True

                        # Se actualiza el tablero con la jugada
                        tablero_temporal.Jugada(mov_in, mov_fin, origen, destino)

                        # Se reinicia el contador de la cantidad de piezas y promociones;
                        # esto para que no se acumule con los de la iteración anterior
                        num_pawns_w = 0
                        num_pawns_b = 0
                        num_bishops_w = 0
                        num_bishops_b = 0
                        num_rook_w = 0
                        num_rook_b = 0
                        num_knights_w = 0
                        num_knights_b = 0
                        num_queen_w = 0
                        num_queen_b = 0
                        num_king_w = 0
                        num_king_b = 0
                        num_promotion_w = 0
                        num_promotion_b = 0

                        # Se lee la cantidad de piezas del color definido
                        # dentro de la matriz del tablero 8x8, sin contar, a las
                        # piezas presentes en el seleccionador
                        for f in range(dimension_temp-2):
                            num_pawns_w += tablero_temporal.board[f].count("wP")
                            num_pawns_b += tablero_temporal.board[f].count("bP")
                            num_bishops_w += tablero_temporal.board[f].count("wB")
                            num_bishops_b += tablero_temporal.board[f].count("bB")
                            num_rook_w += tablero_temporal.board[f].count("wR")
                            num_rook_b += tablero_temporal.board[f].count("bR")
                            num_knights_w += tablero_temporal.board[f].count("wN")
                            num_knights_b += tablero_temporal.board[f].count("bN")
                            num_queen_w += tablero_temporal.board[f].count("wQ")
                            num_queen_b += tablero_temporal.board[f].count("bQ")
                            num_king_w += tablero_temporal.board[f].count("wK")
                            num_king_b += tablero_temporal.board[f].count("bK")

                        # En caso de que la cantidad de piezas que se pueden dar
                        # por promoción excedan sus valores por defecto,
                        # se suma al contador de promociones
                        # dicha cantidad de piezas restando las 2 por defecto.
                        if num_bishops_w > 2:
                            num_promotion_w += (num_bishops_w-2)
                        if num_rook_w > 2:
                            num_promotion_w += (num_rook_w-2)
                        if num_knights_w > 2:
                            num_promotion_w += (num_knights_w-2)
                        if num_queen_w > 1:
                            num_promotion_w += (num_queen_w-1)
                        if num_bishops_b > 2:
                            num_promotion_b += (num_bishops_b-2)
                        if num_rook_b > 2:
                            num_promotion_b += (num_rook_b-2)
                        if num_knights_b > 2:
                            num_promotion_b += (num_knights_b-2)
                        if num_queen_b > 1:
                            num_promotion_b += (num_queen_b-1)

                        # Se reinician las variables de promoción disponible
                        promotion_b_disponible = True
                        promotion_w_disponible = True

                        # Se define que la pieza NO se encuentra en su posición inicial si se dan los siguientes casos:
                        #  - El usuario no ha colocado ninguna pieza en dicha posición.
                        #  - El usuario ha colocado otra pieza que no corresponde en dicha posición.
                        #  - El usuario ha borrado la pieza en dicha posición.
                        #  - El usuario ha movido la pieza a otra posición.

                        if tablero_temporal.board[7][4] == "--" or tablero_temporal.board[7][4] != "wK":  # REY BLANCO
                            primerMovimiento_temp[0] = 0
                        if tablero_temporal.board[0][4] == "--" or tablero_temporal.board[0][4] != "bK":  # REY NEGRO
                            primerMovimiento_temp[1] = 0
                        if tablero_temporal.board[7][7] == "--" or tablero_temporal.board[7][7] != "wR":  # TORRE BLANCA DERECHA
                            primerMovimiento_temp[2] = 0
                        if tablero_temporal.board[7][0] == "--" or tablero_temporal.board[7][0] != "wR":  # TORRE BLANCA IZQUIERDA
                            primerMovimiento_temp[3] = 0
                        if tablero_temporal.board[0][7] == "--" or tablero_temporal.board[0][7] != "bR":  # TORRE NEGRA DERECHA
                            primerMovimiento_temp[4] = 0
                        if tablero_temporal.board[0][0] == "--" or tablero_temporal.board[0][0] != "bR":  # TORRE NEGRA IZQUIERDA
                            primerMovimiento_temp[5] = 0

                        # Se resetean las variables que guardan el último click
                        # del usuario y el historial de clicks.
                        cuadro_selec_temp = ()
                        historial_clicks_temp = []

                        # Se copia cada elemento dentro del tablero temporal
                        # y se actualiza en el board del juego.
                        for f in range(dimension_temp-2):  # f: fila
                            for c in range(dimension_temp-2):  # c: columna
                                board[f][c] = tablero_temporal.board[f][c]

        if z:
            left = mov_fin[1] * SQ_size
            top = mov_fin[0] * SQ_size
            p.draw.rect(screen1, red, p.Rect(left, top, SQ_size_temp, SQ_size_temp))
            p.display.flip()

        colores = [white, blue]
        for f in range(dimension_temp):  # f: fila
            for c in range(dimension_temp-2):  # c: columna
                if f == 8:
                    color = blue
                elif f == 9:
                    color = white
                else:
                    color = colores[((f+c) % 2)]
                left = c * SQ_size
                top = f * SQ_size
                p.draw.rect(screen1, color, p.Rect(left, top, SQ_size_temp, SQ_size_temp))

        if z:
            left = mov_fin[1] * SQ_size
            top = mov_fin[0] * SQ_size
            p.draw.rect(screen1, red, p.Rect(left, top, SQ_size_temp, SQ_size_temp))

        for f in range(dimension_temp):  # f:fila
            for c in range(dimension_temp-2):  # c:columna
                pieza = tablero_temporal.board[f][c]
                rectangulo = p.Rect(c * SQ_size, f * SQ_size, SQ_size, SQ_size)
                if pieza != "--":  # No es un espacio vacío.
                    screen1.blit(imagenes[pieza], rectangulo)
        z = False
        reloj1.tick(max_FPS)
        p.display.flip()


# Le pregunta al usuario, si en el tablero planteado, la pieza colocada ya ha
# realizado un movimiento anterior. Esto se usa para discriminar
# un posible enroque.
def preguntaPrimerMov(anchotemp_original, altotemp_original):
    altotemp = 256
    anchotemp = 512
    dimension_temp = 2
    SQ_size_temp = anchotemp // dimension_temp
    screen1 = p.display.set_mode((anchotemp, altotemp))  # Genera el display
    reloj1 = p.time.Clock()
    screen1.fill(white)

    # Carga las imágenes desde la carpeta y las escala
    img1 = p.image.load("imagenes/" + "no" + ".png")
    img2 = p.image.load("imagenes/" + "yes" + ".png")
    img1 = p.transform.scale(img1, (SQ_size_temp//2, SQ_size_temp//2))
    img2 = p.transform.scale(img2, (SQ_size_temp//2, SQ_size_temp//2))

    # Se genera un rectangulo para poner la imagen encima
    rectangulo1 = p.Rect(64, 64, SQ_size_temp, SQ_size_temp)
    rectangulo2 = p.Rect(320, 64, SQ_size_temp, SQ_size_temp)

    # Se generan dos rectangulos para pintar el fondo
    rectangulo3 = p.Rect(0, 0, SQ_size_temp, SQ_size_temp)
    rectangulo4 = p.Rect(SQ_size_temp, 0, SQ_size_temp, SQ_size_temp)
    p.draw.rect(screen1, "white", rectangulo3)
    p.draw.rect(screen1, "blue", rectangulo4)

    # Pinta las imágenes
    screen1.blit(img1, rectangulo2)
    screen1.blit(img2, rectangulo1)

    p.font.init()
    font = p.font.Font('freesansbold.ttf', 16)
    texto = font.render('¿La pieza ya ha realizado un movimiento anteriormente?', True, white, black)
    screen1.blit(texto, (32, 32))

    # Se le hace flip a la pantalla
    reloj1.tick(max_FPS)
    p.display.flip()
    corriendo = True

    # Se obtiene cuál fue la selección del usuario y se retorna
    while corriendo:
        ubicacion_mouse1 = p.mouse.get_pos()
        colum = int(ubicacion_mouse1[0]//SQ_size_temp)
        for e in p.event.get():
            if e.type == p.QUIT:
                corriendo = False
            elif e.type == p.MOUSEBUTTONDOWN:
                colum = int(ubicacion_mouse1[0]//SQ_size_temp)
                corriendo = False
    screen1 = p.display.set_mode((anchotemp_original, altotemp_original))
    return colum


# Pregunta qué color debe de iniciar, esto en caso de no
# usar un tablero inicial. Si se le da x a la venta, se
# define el color blanco como defecto.
def quieninicia():
    altotemp = 256
    anchotemp = 512
    dimension_temp = 2
    SQ_size_temp = anchotemp // dimension_temp
    screen1 = p.display.set_mode((anchotemp, altotemp))  # Genera el display
    reloj1 = p.time.Clock()
    screen1.fill(white)

    # Se generan dos rectangulos para pintar el fondo
    rectangulo3 = p.Rect(0, 0, SQ_size_temp, SQ_size_temp)
    rectangulo4 = p.Rect(SQ_size_temp, 0, SQ_size_temp, SQ_size_temp)
    p.draw.rect(screen1, "white", rectangulo3)
    p.draw.rect(screen1, "black", rectangulo4)

    p.font.init()
    font = p.font.Font('freesansbold.ttf', 16)
    texto = font.render('¿Cuál equipo debe empezar?', True, white, black)
    screen1.blit(texto, (150, 32))

    # Se le hace flip a la pantalla
    reloj1.tick(max_FPS)
    p.display.flip()
    corriendo = True

    # Se obtiene cuál fue la selección del usuario y se retorna
    while corriendo:
        colum = False
        for e in p.event.get():
            if e.type == p.QUIT:
                corriendo = False
            elif e.type == p.MOUSEBUTTONDOWN:
                ubicacion_mouse1 = p.mouse.get_pos()
                colum = int(ubicacion_mouse1[0]//SQ_size_temp)
                corriendo = False
    screen1 = p.display.set_mode((640, 512))
    colum = bool(colum)
    if colum:
        colum = "b"
    else:
        colum = "w"
    return colum


# Le permite escoger al usuario con cuál color desea jugar. Si se 
# cierra la ventana, se escoge blanco por defecto
def escogerequipo():
    altotemp = 256
    anchotemp = 512
    dimension_temp = 2
    SQ_size_temp = anchotemp // dimension_temp
    screen2 = p.display.set_mode((anchotemp, altotemp))  # Genera el display
    reloj1 = p.time.Clock()
    screen2.fill(white)

    # Se generan dos rectangulos para pintar el fondo
    rectangulo3 = p.Rect(0, 0, SQ_size_temp, SQ_size_temp)
    rectangulo4 = p.Rect(SQ_size_temp, 0, SQ_size_temp, SQ_size_temp)
    p.draw.rect(screen2, "white", rectangulo3)
    p.draw.rect(screen2, "black", rectangulo4)

    p.font.init()
    font = p.font.Font('freesansbold.ttf', 16)
    texto = font.render('¿Con cuál equipo desea jugar?', True, white, black)
    screen2.blit(texto, (150, 32))

    # Se le hace flip a la pantalla
    reloj1.tick(max_FPS)
    p.display.flip()
    corriendo = True

    # Se obtiene cuál fue la selección del usuario y se retorna
    while corriendo:
        colum = False
        for e in p.event.get():
            if e.type == p.QUIT:
                corriendo = False
            elif e.type == p.MOUSEBUTTONDOWN:
                ubicacion_mouse1 = p.mouse.get_pos()
                colum = int(ubicacion_mouse1[0]//SQ_size_temp)
                corriendo = False
    # screen2 = p.display.set_mode((640, 512))
    colum = bool(colum)
    if colum:
        colum = "b"
    else:
        colum = "w"
    return colum


# Una vez que se cierra la ventana, le pregunta al usuario si
# desea volver a jugar.
def gameover():
    altotemp = 256
    anchotemp = 512
    dimension_temp = 2
    SQ_size_temp = anchotemp // dimension_temp
    screen1 = p.display.set_mode((anchotemp, altotemp))  # Genera el display
    reloj1 = p.time.Clock()
    screen1.fill(white)
    # Carga las imágenes desde la carpeta y las escala
    img1 = p.image.load("imagenes/" + "yes" + ".png")
    img2 = p.image.load("imagenes/" + "no" + ".png")
    img1 = p.transform.scale(img1, (SQ_size_temp//2, SQ_size_temp//2))
    img2 = p.transform.scale(img2, (SQ_size_temp//2, SQ_size_temp//2))

    # Se genera un rectangulo para poner la imagen encima
    rectangulo1 = p.Rect(64, 64, SQ_size_temp, SQ_size_temp)
    rectangulo2 = p.Rect(320, 64, SQ_size_temp, SQ_size_temp)

    # Se generan dos rectangulos para pintar el fondo
    rectangulo3 = p.Rect(0, 0, SQ_size_temp, SQ_size_temp)
    rectangulo4 = p.Rect(SQ_size_temp, 0, SQ_size_temp, SQ_size_temp)
    p.draw.rect(screen1, "white", rectangulo3)
    p.draw.rect(screen1, "white", rectangulo4)

    # Pinta las imágenes
    screen1.blit(img1, rectangulo2)
    screen1.blit(img2, rectangulo1)

    p.font.init()
    font = p.font.Font('freesansbold.ttf', 16)
    texto = font.render('¿Desea volver a jugar?', True, white, black)
    screen1.blit(texto, (160, 32))

    # Se le hace flip a la pantalla
    reloj1.tick(max_FPS)
    p.display.flip()
    corriendo = True

    # Se obtiene cuál fue la selección del usuario y se retorna
    while corriendo:
        ubicacion_mouse1 = p.mouse.get_pos()
        colum = int(ubicacion_mouse1[0]//SQ_size_temp)
        for e in p.event.get():
            if e.type == p.QUIT:
                corriendo = False
            elif e.type == p.MOUSEBUTTONDOWN:
                colum = int(ubicacion_mouse1[0]//SQ_size_temp)
                corriendo = False
    screen1 = p.display.set_mode((640, 512))
    return colum


# Para que se ejecute solo cuando corro este archivo.py
if __name__ == "__main__":
    jugando = True
    while jugando:
        main()
        jugando = gameover()