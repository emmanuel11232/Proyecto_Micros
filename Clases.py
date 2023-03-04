class pieza:
 
    def __init__(self, tipo,color,pos_x,pos_y, inicial,turno):
        self.tipo = tipo
        self.color = color
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.inicial = inicial
        self.turno = turno
        self.cas_avail = []
        self.cas_take = []

class pawn(pieza):

    def get_cas_avail(self, ficha: pieza, matriz):
        #super().__init__(self, tipo,color,pos_x,pos_y, inicial,turno)
        if self.color == "w": #Se revisa si la ficha es blanca para asignar los valores en los que se van a poner dos cuadros
            a = 1
            b = 6 
        else:
            a = -1
            b = 1
        if self.turno == True:
            if self.pos_y == b: #Se revisa si está en la posición inicial del pawn
                if matriz[self.pos_x][self.pos_y+(a*2)] == "--": self.cas_avail[1] = ("green",self.pos_x, self.pos_y+(a*2)) 
                    #Si la posición aledaña está vacía se asigna a su lista de posiciones disponibles, la posición 
            elif matriz[self.pos_x][self.pos_y+a] == "--": self.cas_avail[0] = ("green",self.pos_x, self.pos_y+a)
            if matriz[self.pos_x+a][self.pos_y+a] == "--" and matriz[self.pos_x+a][self.pos_y+a][0] != self.color:
                self.cas_avail[2] = ("yellow",self.pos_x+a, self.pos_y+a)
            if matriz[self.pos_x-a][self.pos_y+a] == "--" and matriz[self.pos_x-a][self.pos_y+a][0] != self.color:
                self.cas_avail[3] = ("yellow",self.pos_x-a, self.pos_y+a)

class bishop(pieza):

    def get_cas_avail( ficha, matriz):
        d1 = 0
        d2 = 0
        d3 = 0
        d4 = 0
        for i in range(1,8): #Se revisa en un rango de 8 
            if ficha.pos_x+i<=7 and ficha.pos_y+i<=7 and d1 == 0:
                #Se revisa también que no se salga de los límites del tablero ya que cuando la posición+número sea mayor a 7, ya se va a haber salido
                #Se revisa iteradamente la diagonal superior derecha, si el switch d1 no está activado...
                #... revisa todas las demás diagonales y esta la deja de revisar
                if matriz[ficha.pos_x+i][ficha.pos_y+i] == "--": ficha.cas_avail.append(("green", ficha.pos_x+i, ficha.pos_y+i))
                #Si la posición revisada está vacía, se mete dicha posición y el color en la lista de la clase
                else:
                    d1 = 1
                    if matriz[ficha.pos_x+i][ficha.pos_y+i][0] != ficha.color : #Si se sale del if anterior, significa que hay una pieza estorbando
                        # si esta pieza es de color contrario a la ficha que se está revisando, se asigna esta ficha como una posible ficha para comer 
                        ficha.cas_take.append(("yellow", ficha.pos_x+i, ficha.pos_y+i))
            if ficha.pos_x-i>=0 and ficha.pos_y+i<=7 and d2 == 0: #Lo mismo pero con la diagonal superior izquierda
                if matriz[ficha.pos_x-i][ficha.pos_y+i] == "--": ficha.cas_avail.append(("green", ficha.pos_x-i, ficha.pos_y+i))
                else:
                    d2 = 1
                    if matriz[ficha.pos_x-i][ficha.pos_y+i][0]  != ficha.color : 
                        ficha.cas_take.append(("yellow", ficha.pos_x-i, ficha.pos_y+i))
            if ficha.pos_x-i>=0 and ficha.pos_y-i>=0 and d3 == 0: #Lo mismo pero con la diagonal inferior izquierda
                if matriz[ficha.pos_x-i][ficha.pos_y-i] == "--": ficha.cas_avail.append(("green", ficha.pos_x-i, ficha.pos_y-i))
                else:
                    d3 = 1
                    if matriz[ficha.pos_x-i][ficha.pos_y-i][0]  != ficha.color : 
                        ficha.cas_take.append(("yellow", ficha.pos_x-i, ficha.pos_y-i))
            if ficha.pos_x+i<=7 and ficha.pos_y-i>=0 and  d4 == 0: #Lo mismo pero con la diagonal inferior derecha
                if matriz[ficha.pos_x+i][ficha.pos_y-i] == "--": ficha.cas_avail.append(("green", ficha.pos_x+i, ficha.pos_y-i))
                else:
                    d4 = 1
                    if matriz[ficha.pos_x+i][ficha.pos_y-i][0]  != ficha.color : 
                        ficha.cas_take.append(("yellow", ficha.pos_x+i, ficha.pos_y-i))

class rook(pieza):

    def get_cas_avail(ficha, matriz):
        d1 = 0
        d2 = 0
        d3 = 0
        d4 = 0
        #Si la ficha es tipo Rook se revisa igual que el bishop, nada más que por filas y columnas, no por diagonales
        for i in range(1,8):
            if ficha.pos_y + i <= 7 and d1 == 0:
                if matriz[ficha.pos_x][ficha.pos_y+i] == "--": ficha.cas_avail.append(("green", ficha.pos_x, ficha.pos_y+i))
                else:
                    d1 = 1
                    if matriz[ficha.pos_x][ficha.pos_y+i][0]  != ficha.color : 
                        ficha.cas_take.append(("yellow", ficha.pos_x, ficha.pos_y+i))
            if ficha.pos_x+i<=7 and d2 == 0:
                if matriz[ficha.pos_x+i][ficha.pos_y] == "--": ficha.cas_avail.append(("green", ficha.pos_x+i, ficha.pos_y))
                else:
                    d2 = 1
                    if matriz[ficha.pos_x+i][ficha.pos_y][0]  != ficha.color : 
                        ficha.cas_take.append(("yellow", ficha.pos_x+i, ficha.pos_y))
            if ficha.pos_y-i>=0 and d3 == 0:
                if matriz[ficha.pos_x][ficha.pos_y-i] == "--": ficha.cas_avail.append(("green", ficha.pos_x, ficha.pos_y-i))
                else:
                    d3 = 1
                    if matriz[ficha.pos_x][ficha.pos_y-i][0]  != ficha.color : 
                        ficha.cas_take.append(("yellow", ficha.pos_x, ficha.pos_y-i))
            if ficha.pos_x-i>=0 and d4 == 0:
                if matriz[ficha.pos_x-i][ficha.pos_y] == "--": ficha.cas_avail.append(("green", ficha.pos_x-i, ficha.pos_y))
                else:
                    d4 = 1
                    if matriz[ficha.pos_x-i][ficha.pos_y][0]  != ficha.color : 
                        ficha.cas_take.append(("yellow", ficha.pos_x-i, ficha.pos_y))

class queen(pieza):

    def get_cas_avail(ficha,matriz):
        d1 = 0
        d2 = 0
        d3 = 0
        d4 = 0
        q1 = 0
        q2 = 0
        q3 = 0
        q4 = 0
        for i in range(1,8):
            if ficha.pos_x+i<=7 and ficha.pos_y+i<=7 and q1 == 0:
                if matriz[ficha.pos_x+i][ficha.pos_y+i] == "--": ficha.cas_avail.append(("green", ficha.pos_x+i, ficha.pos_y+i))
                else:
                    q1 = 1
                    if matriz[ficha.pos_x+i][ficha.pos_y+i][0] != ficha.color : #True==blanco False==Negro
                        ficha.cas_take.append(("yellow", ficha.pos_x+i, ficha.pos_y+i))
            if ficha.pos_x-i>=0 and ficha.pos_y+i<=7 and q2 == 0:
                if matriz[ficha.pos_x-i][ficha.pos_y+i] == "--": ficha.cas_avail.append(("green", ficha.pos_x-i, ficha.pos_y+i))
                else:
                    q2 = 1
                    if matriz[ficha.pos_x-i][ficha.pos_y+i][0]  != ficha.color : 
                        ficha.cas_take.append(("yellow", ficha.pos_x-i, ficha.pos_y+i))
            if ficha.pos_x-i>=0 and ficha.pos_y-i>=0 and q3 == 0:
                if matriz[ficha.pos_x-i][ficha.pos_y-i] == "--": ficha.cas_avail.append(("green", ficha.pos_x-i, ficha.pos_y-i))
                else:
                    q3 = 1
                    if matriz[ficha.pos_x-i][ficha.pos_y-i][0]  != ficha.color : 
                        ficha.cas_take.append(("yellow", ficha.pos_x-i, ficha.pos_y-i))
            if ficha.pos_x+i<=7 and ficha.pos_y-i>=0 and  q4 == 0:
                if matriz[ficha.pos_x+i][ficha.pos_y-i] == "--": ficha.cas_avail.append(("green", ficha.pos_x+i, ficha.pos_y-i))
                else:
                    q4 = 1
                    if matriz[ficha.pos_x+i][ficha.pos_y-i][0]  != ficha.color : 
                        ficha.cas_take.append(("yellow", ficha.pos_x+i, ficha.pos_y-i))
        for i in range(0,8):
            if ficha.pos_y + i <= 7 and d1 == 0:
                if matriz[ficha.pos_x][ficha.pos_y+i] == "--": ficha.cas_avail.append(("green", ficha.pos_x, ficha.pos_y+i))
                else:
                    d1 = 1
                    if matriz[ficha.pos_x][ficha.pos_y+i][0]  != ficha.color : 
                        ficha.cas_take.append(("yellow", ficha.pos_x, ficha.pos_y+i))
            if ficha.pos_x+i<=7 and d2 == 0:
                if matriz[ficha.pos_x+i][ficha.pos_y] == "--": ficha.cas_avail.append(("green", ficha.pos_x+i, ficha.pos_y))
                else:
                    d2 = 1
                    if matriz[ficha.pos_x+i][ficha.pos_y][0]  != ficha.color : 
                        ficha.cas_take.append(("yellow", ficha.pos_x+i, ficha.pos_y))
            if ficha.pos_y-i>=0 and d3 == 0:
                if matriz[ficha.pos_x][ficha.pos_y-i] == "--": ficha.cas_avail.append(("green", ficha.pos_x, ficha.pos_y-i))
                else:
                    d3 = 1
                    if matriz[ficha.pos_x][ficha.pos_y-i][0]  != ficha.color : 
                        ficha.cas_take.append(("yellow", ficha.pos_x, ficha.pos_y-i))
            if ficha.pos_x-i>=0 and d4 == 0:
                if matriz[ficha.pos_x-i][ficha.pos_y] == "--": ficha.cas_avail.append(("green", ficha.pos_x-i, ficha.pos_y))
                else:
                    d4 = 1
                    if matriz[ficha.pos_x-i][ficha.pos_y][0]  != ficha.color : 
                        ficha.cas_take.append(("yellow", ficha.pos_x-i, ficha.pos_y))

class Knight(pieza):

    def get_cas_avail(ficha,matriz):
            #Si la ficha es tipo Knight, ya que este puede saltarse piezas, esta parte solo revisa todas las
            #casillas aledañas a las esquinas de un cuadrado de 3x3, o las 6 L que se forman, same shit
            #Esto se podría hacer más pequeño con un for, pero ocuparía más uso de memoria
        if ficha.pos_x+1<=7 and ficha.pos_y+2<=7: #Igual revisa que no se salga de los límites
            if matriz[ficha.pos_x+1][ficha.pos_y+2] == "--": ficha.cas_avail.append(("green", ficha.pos_x+1, ficha.pos_y+2))
            elif matriz[ficha.pos_x+1][ficha.pos_y+2][0]  != ficha.color : 
                ficha.cas_take.append(("yellow", ficha.pos_x+1, ficha.pos_y+2))    
        if ficha.pos_x+2<=7 and ficha.pos_y+1<=7:
            if matriz[ficha.pos_x+2][ficha.pos_y+1] == "--": ficha.cas_avail.append(("green", ficha.pos_x+2, ficha.pos_y+1))
            elif matriz[ficha.pos_x+2][ficha.pos_y+1][0]  != ficha.color : 
                ficha.cas_take.append(("yellow", ficha.pos_x+2, ficha.pos_y+1)) 
        if ficha.pos_x+2<=7 and ficha.pos_y-1>=0:
            if matriz[ficha.pos_x+2][ficha.pos_y-1] == "--": ficha.cas_avail.append(("green", ficha.pos_x+2, ficha.pos_y-1))
            elif matriz[ficha.pos_x+2][ficha.pos_y-1][0]  != ficha.color : 
                ficha.cas_take.append(("yellow", ficha.pos_x+2, ficha.pos_y-1))
        if ficha.pos_x+1<=7 and ficha.pos_y-2>=0:
            if matriz[ficha.pos_x+1][ficha.pos_y-2] == "--": ficha.cas_avail.append(("green", ficha.pos_x+1, ficha.pos_y-2))
            elif matriz[ficha.pos_x+1][ficha.pos_y-2][0] != ficha.color : 
                ficha.cas_take.append(("yellow", ficha.pos_x+1, ficha.pos_y-2))
        if ficha.pos_x-1>=0 and ficha.pos_y-2>=0: 
            if matriz[ficha.pos_x-1][ficha.pos_y-2] == "--": ficha.cas_avail.append(("green", ficha.pos_x-1, ficha.pos_y-2))
            elif matriz[ficha.pos_x-1][ficha.pos_y-2][0] != ficha.color : 
                ficha.cas_take.append(("yellow", ficha.pos_x-1, ficha.pos_y-2))
        if ficha.pos_x-2>=0 and ficha.pos_y-1>=0:
            if matriz[ficha.pos_x-2][ficha.pos_y-1] == "--": ficha.cas_avail.append(("green", ficha.pos_x-2, ficha.pos_y-1))
            elif matriz[ficha.pos_x-2][ficha.pos_y-1][0]  != ficha.color : 
                ficha.cas_take.append(("yellow", ficha.pos_x-2, ficha.pos_y-1))
        if ficha.pos_x-2>=0 and ficha.pos_y+1<=7:
            if matriz[ficha.pos_x-2][ficha.pos_y+1] == "--": ficha.cas_avail.append(("green", ficha.pos_x-2, ficha.pos_y+1))
            elif matriz[ficha.pos_x-2][ficha.pos_y+1][0]  != ficha.color : 
                ficha.cas_take.append(("yellow", ficha.pos_x-2, ficha.pos_y+1))
        if ficha.pos_x-1>=0 and ficha.pos_y+2<=7:
            if matriz[ficha.pos_x-1][ficha.pos_y+2] == "--": ficha.cas_avail.append(("green", ficha.pos_x-1, ficha.pos_y+2))
            elif matriz[ficha.pos_x-1][ficha.pos_y+2][0]  != ficha.color : 
                ficha.cas_take.append(("yellow", ficha.pos_x-1, ficha.pos_y+2))


        

########################################################################################################################################
def EJEMPLO_INICIAL(ficha: pieza, matriz, array: list):
        #Se utiliza una variable tipo pieza, esta tiene la información en tiempo real de cada una de las piezas del juego
        #Se utiliza la matriz que tiene la información actual del tablero con las piezas
        d1 = 0
        d2 = 0
        d3 = 0
        d4 = 0
        #Las variables d son como switches para dejar de revisar las filas, diagonales o columnas apenas se encuentre otra pieza en el camino
        if ficha.tipo == "P": #Si la ficha es tipo Pawn
            if ficha.color == "w": #Se revisa si la ficha es blanca para asignar los valores en los que se van a poner dos cuadros
                a = 1
                b = 6 
            else:
                 a = -1
                 b = 1
            if ficha.pos_y == b: #Se revisa si está en la posición inicial del pawn
                if matriz[ficha.pos_x][ficha.pos_y+(a*2)] == "--": ficha.cas_avail[1] = ("green",ficha.pos_x, ficha.pos_y+(a*2)) 
                #Si la posición aledaña está vacía se asigna a su lista de posiciones disponibles, la posición 
            elif matriz[ficha.pos_x][ficha.pos_y+a] == "--": ficha.cas_avail[0] = ((ficha.pos_x*10)+ficha.pos_y+a)
        if ficha.tipo == "B": #Si la ficha es tipo Bishop
            for i in range(1,8): #Se revisa en un rango de 8 
                if ficha.pos_x+i<=7 and ficha.pos_y+i<=7 and d1 == 0:
                    #Se revisa también que no se salga de los límites del tablero ya que cuando la posición+número sea mayor a 7, ya se va a haber salido
                    #Se revisa iteradamente la diagonal superior derecha, si el switch d1 no está activado...
                    #... revisa todas las demás diagonales y esta la deja de revisar
                    if matriz[ficha.pos_x+i][ficha.pos_y+i] == "--": ficha.cas_avail.append(("green", ficha.pos_x+i, ficha.pos_y+i))
                    #Si la posición revisada está vacía, se mete dicha posición y el color en la lista de la clase
                    else:
                        d1 = 1
                        if matriz[ficha.pos_x+i][ficha.pos_y+i][0] != ficha.color : #Si se sale del if anterior, significa que hay una pieza estorbando
                            # si esta pieza es de color contrario a la ficha que se está revisando, se asigna esta ficha como una posible ficha para comer 
                            ficha.cas_take.append(("yellow", ficha.pos_x+i, ficha.pos_y+i))
                if ficha.pos_x-i>=0 and ficha.pos_y+i<=7 and d2 == 0: #Lo mismo pero con la diagonal superior izquierda
                    if matriz[ficha.pos_x-i][ficha.pos_y+i] == "--": ficha.cas_avail.append(("green", ficha.pos_x-i, ficha.pos_y+i))
                    else:
                        d2 = 1
                        if matriz[ficha.pos_x-i][ficha.pos_y+i][0]  != ficha.color : 
                            ficha.cas_take.append(("yellow", ficha.pos_x-i, ficha.pos_y+i))
                if ficha.pos_x-i>=0 and ficha.pos_y-i>=0 and d3 == 0: #Lo mismo pero con la diagonal inferior izquierda
                    if matriz[ficha.pos_x-i][ficha.pos_y-i] == "--": ficha.cas_avail.append(("green", ficha.pos_x-i, ficha.pos_y-i))
                    else:
                        d3 = 1
                        if matriz[ficha.pos_x-i][ficha.pos_y-i][0]  != ficha.color : 
                            ficha.cas_take.append(("yellow", ficha.pos_x-i, ficha.pos_y-i))
                if ficha.pos_x+i<=7 and ficha.pos_y-i>=0 and  d4 == 0: #Lo mismo pero con la diagonal inferior derecha
                    if matriz[ficha.pos_x+i][ficha.pos_y-i] == "--": ficha.cas_avail.append(("green", ficha.pos_x+i, ficha.pos_y-i))
                    else:
                        d4 = 1
                        if matriz[ficha.pos_x+i][ficha.pos_y-i][0]  != ficha.color : 
                            ficha.cas_take.append(("yellow", ficha.pos_x+i, ficha.pos_y-i))
        if ficha.tipo == "R": #Si la ficha es tipo Rook se revisa igual que el bishop, nada más que por filas y columnas, no por diagonales
            for i in range(1,8):
                if ficha.pos_y + i <= 7 and d1 == 0:
                    if matriz[ficha.pos_x][ficha.pos_y+i] == "--": ficha.cas_avail.append(("green", ficha.pos_x, ficha.pos_y+i))
                    else:
                        d1 = 1
                        if matriz[ficha.pos_x][ficha.pos_y+i][0]  != ficha.color : 
                            ficha.cas_take.append(("yellow", ficha.pos_x, ficha.pos_y+i))
                if ficha.pos_x+i<=7 and d2 == 0:
                    if matriz[ficha.pos_x+i][ficha.pos_y] == "--": ficha.cas_avail.append(("green", ficha.pos_x+i, ficha.pos_y))
                    else:
                        d2 = 1
                        if matriz[ficha.pos_x+i][ficha.pos_y][0]  != ficha.color : 
                            ficha.cas_take.append(("yellow", ficha.pos_x+i, ficha.pos_y))
                if ficha.pos_y-i>=0 and d3 == 0:
                    if matriz[ficha.pos_x][ficha.pos_y-i] == "--": ficha.cas_avail.append(("green", ficha.pos_x, ficha.pos_y-i))
                    else:
                        d3 = 1
                        if matriz[ficha.pos_x][ficha.pos_y-i][0]  != ficha.color : 
                            ficha.cas_take.append(("yellow", ficha.pos_x, ficha.pos_y-i))
                if ficha.pos_x-i>=0 and d4 == 0:
                    if matriz[ficha.pos_x-i][ficha.pos_y] == "--": ficha.cas_avail.append(("green", ficha.pos_x-i, ficha.pos_y))
                    else:
                        d4 = 1
                        if matriz[ficha.pos_x-i][ficha.pos_y][0]  != ficha.color : 
                            ficha.cas_take.append(("yellow", ficha.pos_x-i, ficha.pos_y))
        if ficha.tipo == "Q": #Si la ficha es tipo Queen es una combinación de rook y bishop
            q1 = 0
            q2 = 0
            q3 = 0
            q4 = 0
            for i in range(1,8):
                if ficha.pos_x+i<=7 and ficha.pos_y+i<=7 and q1 == 0:
                    if matriz[ficha.pos_x+i][ficha.pos_y+i] == "--": ficha.cas_avail.append(("green", ficha.pos_x+i, ficha.pos_y+i))
                    else:
                        q1 = 1
                        if matriz[ficha.pos_x+i][ficha.pos_y+i][0] != ficha.color : #True==blanco False==Negro
                            ficha.cas_take.append(("yellow", ficha.pos_x+i, ficha.pos_y+i))
                if ficha.pos_x-i>=0 and ficha.pos_y+i<=7 and q2 == 0:
                    if matriz[ficha.pos_x-i][ficha.pos_y+i] == "--": ficha.cas_avail.append(("green", ficha.pos_x-i, ficha.pos_y+i))
                    else:
                        q2 = 1
                        if matriz[ficha.pos_x-i][ficha.pos_y+i][0]  != ficha.color : 
                            ficha.cas_take.append(("yellow", ficha.pos_x-i, ficha.pos_y+i))
                if ficha.pos_x-i>=0 and ficha.pos_y-i>=0 and q3 == 0:
                    if matriz[ficha.pos_x-i][ficha.pos_y-i] == "--": ficha.cas_avail.append(("green", ficha.pos_x-i, ficha.pos_y-i))
                    else:
                        q3 = 1
                        if matriz[ficha.pos_x-i][ficha.pos_y-i][0]  != ficha.color : 
                            ficha.cas_take.append(("yellow", ficha.pos_x-i, ficha.pos_y-i))
                if ficha.pos_x+i<=7 and ficha.pos_y-i>=0 and  q4 == 0:
                    if matriz[ficha.pos_x+i][ficha.pos_y-i] == "--": ficha.cas_avail.append(("green", ficha.pos_x+i, ficha.pos_y-i))
                    else:
                        q4 = 1
                        if matriz[ficha.pos_x+i][ficha.pos_y-i][0]  != ficha.color : 
                            ficha.cas_take.append(("yellow", ficha.pos_x+i, ficha.pos_y-i))
            for i in range(0,8):
                if ficha.pos_y + i <= 7 and d1 == 0:
                    if matriz[ficha.pos_x][ficha.pos_y+i] == "--": ficha.cas_avail.append(("green", ficha.pos_x, ficha.pos_y+i))
                    else:
                        d1 = 1
                        if matriz[ficha.pos_x][ficha.pos_y+i][0]  != ficha.color : 
                            ficha.cas_take.append(("yellow", ficha.pos_x, ficha.pos_y+i))
                if ficha.pos_x+i<=7 and d2 == 0:
                    if matriz[ficha.pos_x+i][ficha.pos_y] == "--": ficha.cas_avail.append(("green", ficha.pos_x+i, ficha.pos_y))
                    else:
                        d2 = 1
                        if matriz[ficha.pos_x+i][ficha.pos_y][0]  != ficha.color : 
                            ficha.cas_take.append(("yellow", ficha.pos_x+i, ficha.pos_y))
                if ficha.pos_y-i>=0 and d3 == 0:
                    if matriz[ficha.pos_x][ficha.pos_y-i] == "--": ficha.cas_avail.append(("green", ficha.pos_x, ficha.pos_y-i))
                    else:
                        d3 = 1
                        if matriz[ficha.pos_x][ficha.pos_y-i][0]  != ficha.color : 
                            ficha.cas_take.append(("yellow", ficha.pos_x, ficha.pos_y-i))
                if ficha.pos_x-i>=0 and d4 == 0:
                    if matriz[ficha.pos_x-i][ficha.pos_y] == "--": ficha.cas_avail.append(("green", ficha.pos_x-i, ficha.pos_y))
                    else:
                        d4 = 1
                        if matriz[ficha.pos_x-i][ficha.pos_y][0]  != ficha.color : 
                            ficha.cas_take.append(("yellow", ficha.pos_x-i, ficha.pos_y))
        if ficha.tipo == "N":
             #Si la ficha es tipo Knight, ya que este puede saltarse piezas, esta parte solo revisa todas las
             #casillas aledañas a las esquinas de un cuadrado de 3x3, o las 6 L que se forman, same shit
             #Esto se podría hacer más pequeño con un for, pero ocuparía más uso de memoria
            if ficha.pos_x+1<=7 and ficha.pos_y+2<=7: #Igual revisa que no se salga de los límites
                if matriz[ficha.pos_x+1][ficha.pos_y+2] == "--": ficha.cas_avail.append(("green", ficha.pos_x+1, ficha.pos_y+2))
                elif matriz[ficha.pos_x+1][ficha.pos_y+2][0]  != ficha.color : 
                    ficha.cas_take.append(("yellow", ficha.pos_x+1, ficha.pos_y+2))    
            if ficha.pos_x+2<=7 and ficha.pos_y+1<=7:
                if matriz[ficha.pos_x+2][ficha.pos_y+1] == "--": ficha.cas_avail.append(("green", ficha.pos_x+2, ficha.pos_y+1))
                elif matriz[ficha.pos_x+2][ficha.pos_y+1][0]  != ficha.color : 
                    ficha.cas_take.append(("yellow", ficha.pos_x+2, ficha.pos_y+1)) 
            if ficha.pos_x+2<=7 and ficha.pos_y-1>=0:
                if matriz[ficha.pos_x+2][ficha.pos_y-1] == "--": ficha.cas_avail.append(("green", ficha.pos_x+2, ficha.pos_y-1))
                elif matriz[ficha.pos_x+2][ficha.pos_y-1][0]  != ficha.color : 
                    ficha.cas_take.append(("yellow", ficha.pos_x+2, ficha.pos_y-1))
            if ficha.pos_x+1<=7 and ficha.pos_y-2>=0:
                if matriz[ficha.pos_x+1][ficha.pos_y-2] == "--": ficha.cas_avail.append(("green", ficha.pos_x+1, ficha.pos_y-2))
                elif matriz[ficha.pos_x+1][ficha.pos_y-2][0] != ficha.color : 
                    ficha.cas_take.append(("yellow", ficha.pos_x+1, ficha.pos_y-2))
            if ficha.pos_x-1>=0 and ficha.pos_y-2>=0: 
                if matriz[ficha.pos_x-1][ficha.pos_y-2] == "--": ficha.cas_avail.append(("green", ficha.pos_x-1, ficha.pos_y-2))
                elif matriz[ficha.pos_x-1][ficha.pos_y-2][0] != ficha.color : 
                    ficha.cas_take.append(("yellow", ficha.pos_x-1, ficha.pos_y-2))
            if ficha.pos_x-2>=0 and ficha.pos_y-1>=0:
                if matriz[ficha.pos_x-2][ficha.pos_y-1] == "--": ficha.cas_avail.append(("green", ficha.pos_x-2, ficha.pos_y-1))
                elif matriz[ficha.pos_x-2][ficha.pos_y-1][0]  != ficha.color : 
                    ficha.cas_take.append(("yellow", ficha.pos_x-2, ficha.pos_y-1))
            if ficha.pos_x-2>=0 and ficha.pos_y+1<=7:
                if matriz[ficha.pos_x-2][ficha.pos_y+1] == "--": ficha.cas_avail.append(("green", ficha.pos_x-2, ficha.pos_y+1))
                elif matriz[ficha.pos_x-2][ficha.pos_y+1][0]  != ficha.color : 
                    ficha.cas_take.append(("yellow", ficha.pos_x-2, ficha.pos_y+1))
            if ficha.pos_x-1>=0 and ficha.pos_y+2<=7:
                if matriz[ficha.pos_x-1][ficha.pos_y+2] == "--": ficha.cas_avail.append(("green", ficha.pos_x-1, ficha.pos_y+2))
                elif matriz[ficha.pos_x-1][ficha.pos_y+2][0]  != ficha.color : 
                    ficha.cas_take.append(("yellow", ficha.pos_x-1, ficha.pos_y+2))
        