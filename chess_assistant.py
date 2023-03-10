# Este documento almacena toda la información actual del juego.
# También determina las jugadas válidas en el movimiento actual
# Mantiene un registro de los movimientos (puede deshacer jugadas y así)

class Estado_Juego():
    def __init__(self):
        # Se crea una nueva clase que va a representar el tablero del juego,
        # En este caso, es una lista 2D y 8x8, cada elemeto de la lista tiene
        # 2 caracteres strings, el primero indica el color b:black o w:white
        # El segundo indica el tipo de pieza R:Roock N:Nkight B:Bishop Q:Queen
        # K:King y P:Pawn. Por último, un espacio vacío se representa "--"
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"], ]
        self.mueve_blanco = True
        self.registro_movimiento = []  # Move log

    def Jugada(self, movimiento):
        # Se "mueven" las piezas
        self.board[movimiento.start_fila][movimiento.start_colum] = "--"
        pos_final = movimiento.pieza_movida
        self.board[movimiento.end_fila][movimiento.end_colum] = pos_final
        # Se almacena el movimiento realizado
        self.registro_movimiento.append(movimiento)
        # Esto es para que de fijo se tenga que mover una ficha negra después
        # de una blanca, ESTO PUEDE SER LO QUE SE MODIFIQUE AL HACER EL BOTÓN
        # QUE SALTA LA JUGADA DEL OPONENTE
        # NOTA:
        # DE MOMENTO NO HACE NADA, SOLO CAMBIA DE TRUE A FALSE,
        # PERO CUANDO YA SE PONGAN LAS REGLAS DE JUEGO AHÍ VA A SER ÚTIL ESTA
        # VARIABLE, LE PUEDO PONER UN IF PARA QUE SOLO PUEDA MOVER UNA BLANCA
        # Y LUEGO SOLO PUEDA MOVER UNA NEGRA PERO ESTO CAMBIA SI EN UNA JUGADA
        # SE PUEDEN MOVER 2 PIEZAS BLANCAS AL MISMO TIEMPO
        self.mueve_blanco = not self.mueve_blanco


class Movimiento():
    # Se usan diccionarios que le asigna valores a llaves string para
    # las filas y columna según la notación del ajedres (letras:columnas
    # y números:filas)
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1,
                     "8": 0}
    # Esta línea hace lo inverso de la anterior
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_colums = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6,
                       "h": 7}
    # Esta línea hace lo inverso de la anterior
    colums_to_files = {v: k for k, v in files_to_colums.items()}

    def __init__(self, start_sq, end_sq, board):
        # Variables que facilitan el manejo de los atributos de la clase
        # para tenerlos ya separados en filas y columnas.
        self.start_fila = start_sq[0]
        self.start_colum = start_sq[1]
        self.end_fila = end_sq[0]
        self.end_colum = end_sq[1]
        # Estas variables solo almacenan la información del movimiento o jugada
        # Y adicionalmente si se captura una pieza del oponente
        self.pieza_movida = board[self.start_fila][self.start_colum]
        self.pieza_capturada = board[self.end_fila][self.end_colum]

    def Notacion_chess(self):
        # Devuelve la notación de ajedrez para la casilla donde está la pieza
        # que quiero mover y la notación del cuadro a donde la quiero mover
        notacion_in = self.letra_numero(self.start_fila, self.start_colum)
        notacion_fi = self.letra_numero(self.end_fila, self.end_colum)
        return notacion_in + notacion_fi

    def letra_numero(self, fila, columna):
        # Devuelve la notación de ajedrez, primero columna y luego fila (ej:a1)
        return self.colums_to_files[columna] + self.rows_to_ranks[fila]
