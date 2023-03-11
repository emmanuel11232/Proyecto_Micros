class pieza:

    def __init__(self, tipo, color, fila, col, cas_avail, cas_take, board):
        self.tipo = " "  # Define cuál pieza es
        self.color = color
        self.fila = fila
        self.col = col
        self.cas_avail = []  # Define las casillas donde se puede mover
        self.cas_take = []  # Define las casillas donde puede comer
        self.board = board


class pawn(pieza):

    def __init__(self, tipo, color, fila, col, cas_avail, cas_take, board):
        super().__init__(tipo, color, fila, col, cas_avail, cas_take, board)  # Define cuál pieza es
        self.tipo = tipo
        self.get_cas_avail()
        self.get_cas_take()

    def get_cas_avail(self):
        if self.color == "w":  # Se revisa si la self es blanca para asignar los valores en los que se van a poner dos cuadros
            a = -1
            b = 6
        else:
            a = 1
            b = 1
        print(self.board[self.fila+a][self.col])
        if self.board[self.fila+a][self.col] == "--":  # Si la posición aledaña está vacía se asigna a su lista de posiciones disponibles, la posición 
            self.cas_avail.append((self.fila+a, self.col))
        if self.fila == b:  # Se revisa si está en posición inicial del pawn
            if self.board[self.fila+(a*2)][self.col] == "--": 
                self.cas_avail.append((self.fila+(a*2), self.col))

    def get_cas_take(self):
        if self.color == "w":  # Se revisa si la self es blanca para asignar los valores en los que se van a poner dos cuadros
            a = -1
        else:
            a = 1
        if (self.col != 7 and self.color == "b") or self.color == "w":
            if self.board[self.fila+a][self.col+a] != "--" and self.board[self.fila+a][self.col+a][0] != self.color:
                self.cas_take.append((self.fila+a, self.col+a))
        if (self.col != 7 and self.color == "w") or self.color == "b":
            if self.board[self.fila+a][self.col-a] != "--" and self.board[self.fila+a][self.col-a][0] != self.color:
                self.cas_take.append((self.fila+a, self.col-a))


class bishop(pieza):

    def __init__(self, tipo, color, fila, col, cas_avail, cas_take, board):
        super().__init__(tipo, color, fila, col, cas_avail, cas_take, board)  # Define cuál pieza es
        self.tipo = tipo
        self.get_cas_avail_take()

    def get_cas_avail_take(self):
        d1 = 0
        d2 = 0
        d3 = 0
        d4 = 0
        for i in range(1, 8):  # Se revisa en un rango de 8 
            if self.col + i <= 7 and self.fila + i <= 7 and d1 == 0:
                # Se revisa también que no se salga de los límites del tablero ya que cuando la posición+número sea mayor a 7, ya se va a haber salido
                # Se revisa iteradamente la diagonal superior derecha, si el switch d1 no está activado...
                # ... revisa todas las demás diagonales y esta la deja de revisar
                if self.board[self.fila+i][self.col+i] == "--":
                    self.cas_avail.append((self.fila+i, self.col+i))
                # Si la posición revisada está vacía, se mete dicha posición y el color en la lista de la clase
                else:
                    d1 = 1
                    if self.board[self.fila+i][self.col+i][0] != self.color : #Si se sale del if anterior, significa que hay una pieza estorbando
                        # si esta pieza es de color contrario a la self que se está revisando, se asigna esta self como una posible self para comer 
                        self.cas_take.append((self.fila+i, self.col+i))

            if self.col-i >= 0 and self.fila+i <= 7 and d2 == 0:  # Lo mismo pero con la diagonal superior izquierda
                if self.board[self.fila+i][self.col-i] == "--":
                    self.cas_avail.append((self.fila+i, self.col-i))
                else:
                    d2 = 1
                    if self.board[self.fila+i][self.col-i][0] != self.color:
                        self.cas_take.append((self.fila+i, self.col-i))
            if self.col-i >= 0 and self.fila-i >= 0 and d3 == 0:  # Lo mismo pero con la diagonal inferior izquierda
                if self.board[self.fila-i][self.col-i] == "--":
                    self.cas_avail.append((self.fila-i, self.col-i))
                else:
                    d3 = 1
                    if self.board[self.fila-i][self.col-i][0]  != self.color: 
                        self.cas_take.append((self.fila-i, self.col-i))
            if self.col + i <= 7 and self.fila - i >= 0 and d4 == 0:  # Lo mismo pero con la diagonal inferior derecha
                if self.board[self.fila-i][self.col+i] == "--": 
                    self.cas_avail.append((self.fila-i, self.col+i))
                else:
                    d4 = 1
                    if self.board[self.fila-i][self.col+i][0] != self.color:
                        self.cas_take.append((self.fila-i, self.col+i))


class rook(pieza):

    def __init__(self, tipo, color, fila, col, cas_avail, cas_take, board):
        super().__init__(tipo, color, fila, col, cas_avail, cas_take, board)  # Define cuál pieza es
        self.tipo = tipo
        self.get_cas_avail_take()

    def get_cas_avail_take(self):
        d1 = 0
        d2 = 0
        d3 = 0
        d4 = 0
        # Si la self es tipo Rook se revisa igual que el bishop, nada más que por filas y columnas, no por diagonales
        for i in range(1, 8):
            if self.fila + i <= 7 and d1 == 0:
                if self.board[self.fila+i][self.col] == "--":
                    self.cas_avail.append((self.fila+i, self.col))
                else:
                    d1 = 1
                    if self.board[self.fila+i][self.col][0]  != self.color :
                        self.cas_take.append((self.fila+i, self.col))
            if self.col+i<=7 and d2 == 0:
                if self.board[self.fila][self.col+i] == "--":
                    self.cas_avail.append((self.fila, self.col+i))
                else:
                    d2 = 1
                    if self.board[self.fila][self.col+i][0] != self.color: 
                        self.cas_take.append((self.fila, self.col+i))
            if self.fila-i>=0 and d3 == 0:
                if self.board[self.fila-i][self.col] == "--": 
                    self.cas_avail.append((self.fila-i, self.col))
                else:
                    d3 = 1
                    if self.board[self.fila-i][self.col][0] != self.color:
                        self.cas_take.append((self.fila-i, self.col))
            if self.col - i >= 0 and d4 == 0:
                if self.board[self.fila][self.col-i] == "--":
                    self.cas_avail.append((self.fila, self.col-i))
                else:
                    d4 = 1
                    if self.board[self.fila][self.col-i][0] != self.color:
                        self.cas_take.append((self.fila, self.col-i))

class queen(pieza):

    def __init__(self, tipo, color, fila, col, cas_avail, cas_take, board):
        super().__init__(tipo, color, fila, col, cas_avail, cas_take, board)  # Define cuál pieza es
        self.tipo = tipo
        self.get_cas_avail_take()

    def get_cas_avail_take(self):
        d1 = 0
        d2 = 0
        d3 = 0
        d4 = 0
        q1 = 0
        q2 = 0
        q3 = 0
        q4 = 0
        for i in range(1, 8):
            if self.fila + i <= 7 and q1 == 0:
                if self.board[self.fila+i][self.col] == "--":
                    self.cas_avail.append((self.fila+i, self.col))
                else:
                    q1 = 1
                    if self.board[self.fila+i][self.col][0]  != self.color:
                        self.cas_take.append((self.fila+i, self.col))
            if self.col+i<=7 and q2 == 0:
                if self.board[self.fila][self.col+i] == "--":
                    self.cas_avail.append((self.fila, self.col+i))
                else:
                    q2 = 1
                    if self.board[self.fila][self.col+i][0] != self.color: 
                        self.cas_take.append((self.fila, self.col+i))
            if self.fila-i>=0 and q3 == 0:
                if self.board[self.fila-i][self.col] == "--": 
                    self.cas_avail.append((self.fila-i, self.col))
                else:
                    q3 = 1
                    if self.board[self.fila-i][self.col][0] != self.color:
                        self.cas_take.append((self.fila-i, self.col))
            if self.col - i >= 0 and q4 == 0:
                if self.board[self.fila][self.col-i] == "--":
                    self.cas_avail.append((self.fila, self.col-i))
                else:
                    q4 = 1
                    if self.board[self.fila][self.col-i][0] != self.color:
                        self.cas_take.append((self.fila, self.col-i))
        for i in range(1, 8):  # Se revisa en un rango de 8 
            if self.col + i <= 7 and self.fila + i <= 7 and d1 == 0:
                # Se revisa también que no se salga de los límites del tablero ya que cuando la posición+número sea mayor a 7, ya se va a haber salido
                # Se revisa iteradamente la diagonal superior derecha, si el switch d1 no está activado...
                # ... revisa todas las demás diagonales y esta la deja de revisar
                if self.board[self.fila+i][self.col+i] == "--":
                    self.cas_avail.append((self.fila+i, self.col+i))
                # Si la posición revisada está vacía, se mete dicha posición y el color en la lista de la clase
                else:
                    d1 = 1
                    if self.board[self.fila+i][self.col+i][0] != self.color : #Si se sale del if anterior, significa que hay una pieza estorbando
                        # si esta pieza es de color contrario a la self que se está revisando, se asigna esta self como una posible self para comer 
                        self.cas_take.append((self.fila+i, self.col+i))

            if self.col-i >= 0 and self.fila+i <= 7 and d2 == 0:  # Lo mismo pero con la diagonal superior izquierda
                if self.board[self.fila+i][self.col-i] == "--":
                    self.cas_avail.append((self.fila+i, self.col-i))
                else:
                    d2 = 1
                    if self.board[self.fila+i][self.col-i][0] != self.color:
                        self.cas_take.append((self.fila+i, self.col-i))
            if self.col-i >= 0 and self.fila-i >= 0 and d3 == 0:  # Lo mismo pero con la diagonal inferior izquierda
                if self.board[self.fila-i][self.col-i] == "--":
                    self.cas_avail.append((self.fila-i, self.col-i))
                else:
                    d3 = 1
                    if self.board[self.fila-i][self.col-i][0]  != self.color: 
                        self.cas_take.append((self.fila-i, self.col-i))
            if self.col + i <= 7 and self.fila - i >= 0 and d4 == 0:  # Lo mismo pero con la diagonal inferior derecha
                if self.board[self.fila-i][self.col+i] == "--": 
                    self.cas_avail.append((self.fila-i, self.col+i))
                else:
                    d4 = 1
                    if self.board[self.fila-i][self.col+i][0] != self.color:
                        self.cas_take.append((self.fila-i, self.col+i))

class knight(pieza):
    
    def __init__(self, tipo, color, fila, col, cas_avail, cas_take, board):
        super().__init__(tipo, color, fila, col, cas_avail, cas_take, board)  # Define cuál pieza es
        self.tipo = tipo
        self.get_cas_avail_take()

    def get_cas_avail_take(self):
        # Si la self es tipo Knight, ya que este puede saltarse piezas, esta parte solo revisa todas las
        # casillas aledañas a las esquinas de un cuadrado de 3x3, o las 6 L que se forman
        # Esto se podría hacer más pequeño con un for, pero ocuparía más uso de memoria
        if self.col + 1 <= 7 and self.fila + 2 <= 7:  # Igual revisa que no se salga de los límites
            if self.board[self.fila+2][self.col+1] == "--":
                self.cas_avail.append((self.fila+2, self.col+1))
            elif self.board[self.fila+2][self.col+1][0]  != self.color:
                self.cas_take.append((self.fila+2, self.col+1))
        if self.col + 2 <= 7 and self.fila + 1 <= 7:
            if self.board[self.fila+1][self.col+2] == "--":
                self.cas_avail.append((self.fila+1, self.col+2))
            elif self.board[self.fila+1][self.col+2][0] != self.color:
                self.cas_take.append((self.fila+1, self.col+2))
        if self.col + 2 <= 7 and self.fila - 1 >= 0:
            if self.board[self.fila-1][self.col+2] == "--":
                self.cas_avail.append((self.fila-1, self.col + 2))
            elif self.board[self.fila-1][self.col+2][0] != self.color:
                self.cas_take.append((self.fila-1, self.col+2))
        if self.col + 1 <= 7 and self.fila - 2 >= 0:
            if self.board[self.fila-2][self.col+1] == "--":
                self.cas_avail.append((self.fila-2, self.col+1))
            elif self.board[self.fila-2][self.col+1][0] != self.color:
                self.cas_take.append((self.fila-2, self.col+1))
        if self.col - 1 >= 0 and self.fila-2 >= 0:
            if self.board[self.fila-2][self.col-1] == "--":
                self.cas_avail.append((self.fila-2, self.col-1))
            elif self.board[self.fila-2][self.col-1][0] != self.color:
                self.cas_take.append((self.fila-2, self.col-1))
        if self.col - 2 >= 0 and self.fila - 1 >= 0:
            if self.board[self.fila-1][self.col-2] == "--":
                self.cas_avail.append((self.fila-1, self.col-2))
            elif self.board[self.fila-1][self.col-2][0] != self.color:
                self.cas_take.append((self.fila-1, self.col-2))
        if self.col - 2 >= 0 and self.fila + 1 <= 7:
            if self.board[self.fila+1][self.col-2] == "--":
                self.cas_avail.append((self.fila+1, self.col-2))
            elif self.board[self.fila+1][self.col-2][0] != self.color:
                self.cas_take.append((self.fila+1, self.col-2))
        if self.col - 1 >= 0 and self.fila + 2 <= 7:
            if self.board[self.fila+2][self.col-1] == "--":
                self.cas_avail.append((self.fila+2, self.col-1))
            elif self.board[self.fila+2][self.col-1][0] != self.color:
                self.cas_take.append((self.fila+2, self.col-1))

    class king(pieza):
        def __init__(self, tipo, color, fila, col, cas_avail, cas_take, board):
            super().__init__(tipo, color, fila, col, cas_avail, cas_take, board)  # Define cuál pieza es
            self.tipo = tipo
            self.get_cas_avail_take()
        
        def get_cas_avail_take(self):

            #Agregar que esto se haga solo si el rey no está siendo atacado
            if self.fila + 1 <= 7:
                if self.board[self.fila+1][self.col] == "--":
                    self.cas_avail.append((self.fila+1, self.col))
                elif self.board[self.fila+1][self.col][0] != self.color:
                    self.cas_take.append((self.fila+1, self.col))
            if self.col +1 <= 7 :
                if self.board[self.fila][self.col+1] == "--":
                    self.cas_avail.append((self.fila, self.col+1))
                elif self.board[self.fila][self.col+1][0] != self.color:
                    self.cas_take.append((self.fila, self.col+1))
            if self.col - 1 >= 0:
                if self.board[self.fila][self.col-1] == "--":
                    self.cas_avail.append((self.fila, self.col-1))
                elif self.board[self.fila][self.col-1][0] != self.color:
                    self.cas_take.append((self.fila, self.col-1))
            if self.fila -1 >= 0:
                if self.board[self.fila-1][self.col] == "--":
                    self.cas_avail.append((self.fila-1, self.col))
                elif self.board[self.fila-1][self.col][0] != self.color:
                    self.cas_take.append((self.fila-1, self.col))
            if self.col - 1 >= 0 and self.fila + 1 <= 7:
                if self.board[self.fila+1][self.col-1] == "--":
                    self.cas_avail.append((self.fila+1, self.col-1))
                elif self.board[self.fila+1][self.col-1][0] != self.color:
                    self.cas_take.append((self.fila+1, self.col-1))
            if self.col +1 <= 7 and self.fila - 1 >= 0:
                if self.board[self.fila-1][self.col+1] == "--":
                    self.cas_avail.append((self.fila-1, self.col+1))
                elif self.board[self.fila-1][self.col+1][0] != self.color:
                    self.cas_take.append((self.fila-1, self.col+1))
            if self.col +1 <= 7 and self.fila + 1 <= 7:
                if self.board[self.fila+1][self.col+1] == "--":
                    self.cas_avail.append((self.fila+1, self.col+1))
                elif self.board[self.fila+1][self.col+1][0] != self.color:
                    self.cas_take.append((self.fila+1, self.col+1))
            if self.col - 1 >= 0 and self.fila - 1 >= 0:
                if self.board[self.fila-1][self.col-1] == "--":
                    self.cas_avail.append((self.fila-1, self.col-1))
                elif self.board[self.fila-1][self.col-1][0] != self.color:
                    self.cas_take.append((self.fila-1, self.col-1))
