#######################################################################################
#                              Distributed  PACMAN                                    #  
#                                   HARDMODE                                          #
#                                                                                     #
#                                 Designed by:                                        #
#                                                                                     #
#                        ********* BosiElGato*********                                #
#                                                                                     #
#                  Total or partial reproduction is prohibited                        #
#                                                                                     #
#                              All Rights Reserved                                    #
#######################################################################################

#La libreria ZMQ sirve para la parte de las conexiones, nos ayuda a manejar los mensajes
# a traves de los sockets
import zmq

#Libreria sys para manejar todos los eventos del sistema
import sys

#Se importa la libreria grafica de python, especial para el design de juegos
import pygame


#Se fenen variables globales las cuales no se van a modificar durante la ejecucion de la aplicacion

#Este valor sera en pixeles el ancho de la pantalla
ANCHO=1000

#Este valor sera en pixeles el alto de la pantalla
ALTO=600

#Se define una paleta de colores
BLANCO=(255,255,255)
NEGRO=(0,0,0)
ROJO=(255,0,0)
VERDE=(0,255,0)
AZUL=(0,0,255)

#Se toma el tiempo del reloj, el cual nos servira para deteriminar la tasa de frames por segundo 
#en la ejecucion de la aplicacion 
reloj = pygame.time.Clock()

#Se crea la calse Muro, la cual nos sirve para poner objetos en la pantalla en determinada posicion
#La clase Muro hereda todos las caracteristicas de la clase sprite en el modulo pygame
class Muro(pygame.sprite.Sprite):
    #La clase muro recibe una imagen y una posicion en x y otra posicion en y
    def __init__(self, archivoimagen,x,y):
        #Se inizializa la clase como herencia de el modulo sprite de la libreria pygame
        pygame.sprite.Sprite.__init__(self)
        #Se asigna la imagen que se recibio a la clase muro
        self.image=pygame.image.load(archivoimagen).convert_alpha()
        #Se reciben la ubicacion en x,y del objeto
        self.rect = self.image.get_rect()
        #Se asigna posicion en x al objeto
        self.rect.x = x
        #Se asigna posicion en y al objeto
        self.rect.y = y

    #Se define la clase update la cual se encarga de actualizar los atributos del objeto
    def update(self):
        #Este objeto no tiene funciones asociadas al cambio de sus atributos, por tal motivo
        # se deja como esta
        pass

#Se crea la calse Enemies, la cual nos sirve para poner objetos en la pantalla en determinada posicion
#La clase Enemies hereda todos las caracteristicas de la clase sprite en el modulo pygame
class Enemies(pygame.sprite.Sprite):
    #La clase Enemie recibe una imagen y una posicion en x y otra posicion en y
    def __init__(self, archivoimagen,x,y, direccion):
        #Se inizializa la clase como herencia de el modulo sprite de la libreria pygame
        pygame.sprite.Sprite.__init__(self)
        #Se asigna la imagen que se recibio a la clase muro
        self.image=pygame.image.load(archivoimagen).convert_alpha()
        #Se reciben la ubicacion en x,y del objeto
        self.rect = self.image.get_rect()
        #Se asigna posicion en x al objeto
        self.rect.x = x
        #Se asigna posicion en y al objeto
        self.rect.y = y
        #Este atributo sirve para modifica la posicion del objeto en x
        self.newx =self.rect.x
        #Este atributo sirve para modifica la posicion del objeto en y
        self.newy =self.rect.y
        #El atributo dir le da direccion al sprite, sirve para cambiar la imagen dependiendo de su direccion
        self.dir = 0
        #La velocidad del usuario nos ayuda a mover el objeto un numero de pixeles determinado
        self.speed = 50
        #La direccion es un apoyo que necesitaremos para el atributo dir mas adelante   
        self.dir = direccion

    #Se define la clase update la cual se encarga de actualizar los atributos del objeto
    def update(self):
        #Se actualiza la posicion en x del objeto
        self.rect.x = self.newx
        #Se actualiza la posicion en y del objeto
        self.rect.y = self.newy



#Se crea la clase Player1, la cual nos sirve para poner objetos en la pantalla en determinada posicion
#La clase Player1 hereda todos las caracteristicas de la clase sprite en el modulo pygame
class Player1(pygame.sprite.Sprite):
    #La clase Player1 recibe una imagen  
    def __init__(self, archivoimagen):
        #Se inizializa la clase como herencia de el modulo sprite de la libreria pygame
        pygame.sprite.Sprite.__init__(self)
        #Se asigna la imagen que se recibio a la clase Player1
        self.image=pygame.image.load(archivoimagen).convert_alpha()
        #Se reciben la ubicacion en x,y del objeto
        self.rect = self.image.get_rect()
        #El atributo dir le da direccion al sprite, sirve para cambiar la imagen dependiendo de su direccion
        self.dir = 0
        #Se ubica el objeto en una posicion por defecto en x
        self.rect.x = 500
        #Se ubica el objeto en una posicion por defecto en y
        self.rect.y = 300
        #La velocidad del usuario nos ayuda a mover el objeto un numero de pixeles determinado
        self.speed = 50
        #Se crea un lista donde se almacenaran todos los muros tipo1 del usuario
        self.muros = []
        #Se crea un lista donde se almacenaran todos los galletas tipo1 del usuario 
        self.galletas = []
        #Se crea una variable que cambia su valor si el usuario colisiona con una galleta tipo1
        self.comiogalleta = 0
        #Se crea una lista para las galletas tipo2
        self.galletas2 = []
        #Se crea una variable que cambia su valor si el usuario colisiona con una galleta tipo2
        self.super = 0
        #Se crea una variable de apoyo para la variable super
        self.super2 = 0
        #Se crea una variable para registrar el numero de galletas tipo 1 que han colisiondo con el usuario 
        self.puntaje = 0
        #Se crea una lista en la que van a almacenarse los enemigos del usuario(otros pacman)
        self.muros2 = []
        #Se crea una variable auxiliar de la variable self.dir
        self.dir2 = self.dir
        #Se crea una variable(atributo) del usuario que indica si esta activo en la partida
        self.activo = 1
        #Se crea un atributo para indicar que las galletas se acabaron
        self.finGalletas = 0

    #Se crea el metodo self que actualizara los atributos del usuario 
    def update(self):
        #Se verifica en que direccion va el usuario y se procede a actualizar su posicion
        if self.dir == 3: 
            self.rect.x += self.speed
        if self.dir == 4:
            self.rect.x -= self.speed
        if self.dir == 2:
            self.rect.y += self.speed
        if self.dir == 1:
            self.rect.y -= self.speed

        #Se detiene al usuario en caso de que alcance los bordes de la pantalla
        if self.rect.y > ALTO-50:
            self.rect.y = ALTO-50
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.x > ANCHO-50:
            self.rect.x = ANCHO-50
        if self.rect.x < 0:
            self.rect.x = 0

        #Se verifican las colisiones entre el usuario y las galletas tipo1
        l_col2=pygame.sprite.spritecollide(self,self.galletas,True)

        #Si verifica si hay colision entre el usuario y una galleta tipo1 
        for g in l_col2:
            #Se cambia de estado al atributo comio galleta indicando que colisiono con una galleta y la hizo desa
            #parecer
            self.comiogalleta = 1
            #Se le suma una unidad al puntaje del usuario
            self.puntaje += 1

        #Si verifica si hay colision entre el usuario y una galleta tipo2
        l_col3=pygame.sprite.spritecollide(self,self.galletas2,True)

        #Si verifica si hay colision entre el usuario y una galleta tipo2
        for g in l_col3:
            #Se cambia de estado al atributo super indicando que colisiono con una galleta y la hizo desa
            #parecer
            self.super = 1
            #Se asigna el mismo valor al atributo  auxiliar super2
            self.super2 = 1

        #Se verifica si el usuario colisiona con los muros del mapa
        l_col=pygame.sprite.spritecollide(self,self.muros,False)

        #Se verifica que el usuario no pueda pasar a traves de los muros del mapa
        for m in l_col:
            if self.dir==3:
                if self.rect.right > m.rect.left:
                    self.rect.right = m.rect.left
            if self.dir==4:
                if self.rect.left < m.rect.right:
                    self.rect.left = m.rect.right
            if self.dir==1:
                if self.rect.top < m.rect.bottom:
                    self.rect.top = m.rect.bottom
            if self.dir==2:
                if self.rect.bottom > m.rect.top:
                    self.rect.bottom = m.rect.top

        #Si el usuario no ha colisionoado con ninguna galleta tipo2 quiere decir que esta en un estado normal,
        #por lo cual no podra pasar a traves de sus enemigos(otros Pacman)
        if self.super == 0:

            #Se procede a verificar si el usuario ha colisionado con algun enemigo para que no pueda pasar
            #a traves de el, esta funcion hace que se mantenga en la misma posicion 
            l_col4=pygame.sprite.spritecollide(self,self.muros2,False)
            for m in l_col4:
                if self.dir==3:
                    if self.rect.right > m.rect.left:
                        self.rect.right = m.rect.left
                if self.dir==4:
                    if self.rect.left < m.rect.right:
                        self.rect.left = m.rect.right
                if self.dir==1:
                    if self.rect.top < m.rect.bottom:
                        self.rect.top = m.rect.bottom
                if self.dir==2:
                    if self.rect.bottom > m.rect.top:
                        self.rect.bottom = m.rect.top

        #Si el usuario colisiona con una galleta tipo2 podra hacer desaparecer a sus enemigos si colisiona
        #Con ellos
        else:
            l_col4=pygame.sprite.spritecollide(self,self.muros2,True)

#La funcion poner titulo pone un titulo en la pantalla principal del juego 
def PonerTitulo(Nombre,Titulo):
    #Se crea una variable font que almacena la fuente y el tamano de la letra
    font = pygame.font.SysFont(None, 50)
    #Se crea una variable tecto y se le asigna una cadena un valor booleano y un color
    text = font.render(str(Nombre)+ " : " +str(Titulo), True, ROJO)

    #Se retorna la variable text
    return(text)

#Se crea una funcion que mostrara varios titulos al inicio de la ejecucion
def Titulos(nombre):
    print("\t\t     BosiElGato ")
    print("\t\t All Rights Reserved ")
    print("\t\t    User Online ")
    print("\t\t    Enjoy The Game ")
    print("\t\tHas iniciado como : {}".format(nombre.decode('ascii')))

#En la funcion main() es donde ocurren todos los eventos del juego, alli el usuario inteactuara con la interfaz
#grafica y vera sus eventos reflejados en la pantalla principal
def main():
    #Se recibe un nombre seguido a la ejecucion del juego, el cual se almacenara como su identificador
    if len(sys.argv) != 2:
        #Si no escribe un nombre se le envia un mensaje indicandole que debe hacerlo
        print("!!Debes colocar un nombre para iniciar!!")
        #Se saca al usuario de la ejecucion del juego 
        exit()

    #Creamos el contexto o entorno donde ejecutaremos las conexiones 
    context = zmq.Context()
    #Se define de que tipo va a ser el contexto, en este caso vamos a trabajar con ROUTER y DEALER que son ideales
    #Para la difusion
    socket = context.socket(zmq.DEALER)
    #Se guarda la identidad del usaurio la cual especifico al inicio del juego 
    identity = sys.argv[1].encode('ascii')
    #Se procede a asignar la identidad a su socket para que otros usuarios lo reconozcan
    socket.identity = identity
    ##Se le asigna una direccion IP y un puerto donde se van a recibir todas las solicitudes
    socket.connect("tcp://localhost:4444")

    #Se llama a la funcion Titulos
    Titulos(identity)  

    #El poller es una funcion propia de la libreria ZMQ la cual nos ayuda a registrar todos los eventos
    #Que han ocurrido en el socket y de esta manera poder desplegarlos hacia los demas usuarios
    #Se inicializa el poller
    poller = zmq.Poller()
    #Se Registra el scoket local en el poller
    poller.register(socket, zmq.POLLIN)

    #Se inicializa la libreria de graficos de python pygame
    pygame.init()

    #Se crea una ventana en la cual se mostrara la ejecucion del juego
    ventana = pygame.display.set_mode((ANCHO,ALTO))

    #Se crea el jugador local del juego 
    Judador = Player1("resources/pac_right.png")

    #Se crea una variable info con los parametros por defecto que son asignados al jugador
    info = [0, Judador.rect.x, Judador.rect.y, Judador.comiogalleta,Judador.super, Judador.dir2]

    #Se envia la informacion relacionada al jugador para el servidor a traves del socket 
    socket.send_multipart([bytes(str(info),'ascii')])

    #Se recibe informacion del estado de la partida a la que ha ingresado el usuario
    msg = socket.recv_multipart()
    
    #En la posicion [0] del mensaje se recibe la matriz actualizadad por parte del servidor
    matrizmapa = eval(msg[0].decode('ascii'))

    #En la posicion [1] del mensaje se recibe el numero de jugadores desde el servidor
    CodigoDeJugador = eval(msg[1].decode('ascii'))

    #Se crea una lista para almacenar los nombres de los  jugadores que se vayan conectando a la partida
    ListaDeJugadores = []

    #Se crea una lista para almacenar los datos de los  jugadores que se vayan conectando a la partida 
    ListaEnemigos = []   

    #Se crea una lista con los puntajes de cada usuario
    ListaPuntajes =  []

    #Se crea una variable booleada que indicara el final del juego cuando se le asigne el valor False
    Partida = True

    #La variable MeMori indica que el jugador ha desaparecido de la pantalla y se finaliza la partida para el 
    MeMori = 0

    #La variable booleana movio indica que el usuario ha presionado alguna tecla para moverse en alguna direccion
    movio = False  

    #Se crean los grupos que corresponden a cada sprite del mapa, los cuales se actualizaran con la
    #Informacion de la matriz para dar paso al juego
    muros = pygame.sprite.Group()  
    muros2 = pygame.sprite.Group()
    galletas = pygame.sprite.Group()
    galletas2 = pygame.sprite.Group()
    JudadorGroup = pygame.sprite.Group()
    todos=pygame.sprite.Group()

    #Se prueba si hay informacion suficiente para cargar todos los elementos del juego

    try:
        for i in range(20):
            for j in range(12):
                
                if matrizmapa[j][i]==1:
                    muro = Muro("resources/muro.png",i*50,j*50)
                    muros.add(muro)
                    #todos.add(Judador,muro)
                if matrizmapa[j][i]==0:
                    muro = Muro("resources/galleta.png",i*50,j*50)
                    galletas.add(muro)
                    #todos.add(Judador,muro)
                if matrizmapa[j][i]==3:
                    muro = Muro("resources/estrella.png",i*50,j*50)
                    galletas2.add(muro)

    #En caso de encontrar algun error al momento de la creacion del entrono se sale de la partida 
    #Esto como medida de sefuridad
    except:
        Partida = False
        
    #Se agregan los diferentes elementos a sus respectivos grupos de sprites
    JudadorGroup.add(Judador)
    Judador.muros = muros
    Judador.galletas = galletas
    Judador.galletas2 = galletas2    
    
    #Se verifica si no hay errores, de lo contrario se cierra la ejecucion
    if Partida == False:
        print("Usuario ya Existe!")

    #Se comienza con el loop o ciclo donde se hace la interaccion del usuario con todos los elementos 
    #del juego o partida
    while Partida:
        #Se verifica la informacion que hay en el poller 
        socks = dict(poller.poll(10))
        #Si hay informacion el el poller de mensajes entonces:
        if socket in socks:
            #Se recibe el mensaje que hay en el socket 
            sender, m = socket.recv_multipart()
            #Se imprime el mensaje que llega a traves del socket
            #print("{} {}".format(sender, m))

            #Se decodifica y se convierte a valores enteros el contenido del mensaje
            InformeJugador = eval(m.decode('ascii'))
            #Si el jugador que aparece en el poller no esta registrado de forma local, se procede a su registro
            if sender not in ListaDeJugadores:
                ListaDeJugadores.append(sender)
                ListaPuntajes.append(InformeJugador[7])
                Enemigo  = Enemies("resources/pac_right.png",InformeJugador[1],InformeJugador[2], InformeJugador[5])
                ##Se agrega a la lista de enemigos(pacmans enemigos)
                ListaEnemigos.append(Enemigo)
                #Se agrega al grupo donde iran todos los pacman enemigos para la interaccion con el usuario local
                muros2.add(Enemigo)
            #En caso de que el usuario ya exista se procede a actualizar todos su datos nuevos
            else:
                #Se crea una variable local llamada posicion para recorrer la lista de todos los enemigos
                posicion = 0
                #Se recorre la lista de jugadores enemigos
                for i in ListaDeJugadores:
                    #Se verifica que el usuario al que se le actualizan los datos corresponda con el usuario que
                    #genero el evento
                    if i == sender:
                        if InformeJugador[6] == 1:
                            #Si coincide entonces se actuliza su posicion en x
                            ListaEnemigos[posicion].newx = InformeJugador[1]
                            #Si coincide entonces se actuliza su posicion en y
                            ListaEnemigos[posicion].newy = InformeJugador[2]
                            ListaPuntajes[posicion] = InformeJugador[7]
                        else:
                            #Si coincide entonces se actuliza su posicion en x
                            ListaEnemigos[posicion].newx = 1000
                            #Si coincide entonces se actuliza su posicion en y
                            ListaEnemigos[posicion].newy = 600
                            ListaEnemigos.remove(ListaEnemigos[posicion])
                            ListaDeJugadores.remove(sender)                            

                        #Se verifica hacia que direccion apunta el usuario para proceder a actualizar su imagen en 
                        #el tablero
                        if InformeJugador[5] == 1:
                            ListaEnemigos[posicion].image = pygame.image.load('resources/pac_up.png').convert_alpha()
                        elif InformeJugador[5] == 2:
                            ListaEnemigos[posicion].image = pygame.image.load('resources/pac_down.png').convert_alpha()
                        elif InformeJugador[5] == 3:
                            ListaEnemigos[posicion].image = pygame.image.load('resources/pac_right.png').convert_alpha()
                        elif InformeJugador[5] == 4:
                            ListaEnemigos[posicion].image = pygame.image.load('resources/pac_left.png').convert_alpha()
                    else:
                        #Si el usuario no es el que esta en esta posicion de la lista se pasa a la siguiente
                        posicion += 1
                        if InformeJugador[4] == 1:
                            ListaEnemigos[posicion].image = pygame.image.load('resources/fantasma.png').convert_alpha()
                            Judador.image = pygame.image.load('resources/fantasma.png').convert_alpha()
                            #Aqui hay una restriccion que asiganmos en el diseno del juego la cual era que si algun usuario colisionaba
                            #con una galleta tipo2 los demas se convirtieran en fantasmas y pudieran ser devorados por el usuario 
                            #que colisiono con la galleta tipo2
                            ColisionEnemigoJugador = pygame.sprite.groupcollide(JudadorGroup,muros2,1,1)

                            for i in ColisionEnemigoJugador:
                                #En caso de encontrar esta colision, se da por terminada la partida para este usuario
                                MeMori = 1
                                Partida = False
                                Judador.activo = 0
                



        #Se procede a verificar la interaccion de los grupos de objetos con otros gupos y a actualizar todo el entorno
        ColisionesEnemigosGalletas = pygame.sprite.groupcollide(muros2,galletas,0,1)
        ColisionesEnemigosGalletas2 = pygame.sprite.groupcollide(muros2,galletas2,0,1)

        #Se hace una asignacion de variables para que el jugador aparezca interactuando con los demas objetos
        Judador.muros = muros
        Judador.muros2 = muros2

        #Se agregan todos los sprites a un grupo llamado todos el cual se encargara de hacer que todos actuzalizen su estado
        todos.add(Judador,galletas,muros,muros2, galletas2)

        #Se verifica que existe una colision entre el usaurio y una galleta tipo2
        if Judador.super == 1 and Judador.super2 == 1:
            #Si es asi se registra el momento de la ocurrencia 
            start_time = pygame.time.get_ticks()
            #Se le asigna a la variable super el valor de 0 para que no vuelva a hacer la asignacion del momento
            #De la ocurrencia
            Judador.super2 = 0

            #Si aun no han transcurrido 10 segundos despuesde la colision verifique 
        elif Judador.super == 1 and Judador.super2 == 0:

            #Recorra la lista en la que estan todos los enemigos registrados 
            for e in ListaEnemigos:
                # Y asigneles la imagen de un fantasma indicando que pueden destruirse o comerse
                e.image = pygame.image.load('resources/fantasma.png').convert_alpha()

            #Se verifica que no hayan pasado 10 segundos despues de la colison
            if pygame.time.get_ticks()-start_time> 15000:
                #En caso de que pasen 10 segundos despues de la colision asignele un valor de 0 a la variable super
                #para que otra vez vuelvan todos los usuarios a la normalidad
                Judador.super = 0
        #Asignele el valor de 5 al atributo dir, esto con el fin de que el objeto no se mueva solo por la pantalla
        Judador.dir = 5
        if not Judador.galletas:
            Judador.finGalletas = 1
        #Se verifica si hay eventos de usuario en la ventana de ejecucion
        for eventos in pygame.event.get():
            #Si el evento es salir de la venatan de ejecucion
            if eventos.type==pygame.QUIT:
                #Se cierra la ventana de ejecucion
                exit()

            # Si el usuario presiona una tecla para moerse en alguna direccion 
            if movio == True:
                #Se le envia un mensaje al servidor el cual registra el evento y lo reenvia a todos 
                #Los usuarios que esten conectados
                info = [CodigoDeJugador, Judador.rect.x, Judador.rect.y, Judador.comiogalleta, Judador.super,Judador.dir2, Judador.activo,Judador.puntaje, Judador.finGalletas]               
                
                #Se envia el mensaje a traves del socket 
                socket.send_multipart([bytes(str(info),'ascii')])
                
                #Se asigna el valor False a la variable movio para que no envie mas mensajes hasta que se 
                #mueva de nuevo el jugador
                movio = False
                #Se asigna el valor cero al atributo comiogalleta para indicarle que solo comio una  
                #este vuelve a cambiar de asignacion una vez colisiona con otra galleta tipo1
                Judador.comiogalleta = 0

            #Se verifica si se presiona un tecla 
            if eventos.type == pygame.KEYDOWN:
                #Si se presiona una tecla se procede a registrar que tecla fue y segun la tecla
                # Se procedera a a asignar diferentes parametros a los atributos del usaurio

                #############################################################################
                if eventos.key == pygame.K_w:
                    Judador.dir = 1
                    Judador.dir2 = 1
                    Judador.image = pygame.image.load('resources/pac_up.png').convert_alpha()
                    movio = True


                if eventos.key == pygame.K_s:
                    Judador.dir = 2
                    Judador.dir2 = 2
                    Judador.image = pygame.image.load('resources/pac_down.png').convert_alpha()
                    movio = True
                    
                if eventos.key == pygame.K_d:
                    Judador.dir = 3
                    Judador.dir2 = 3
                    Judador.image = pygame.image.load('resources/pac_right.png').convert_alpha()
                    movio = True
                    
                if eventos.key == pygame.K_a:
                    Judador.dir = 4
                    Judador.dir2 = 4
                    Judador.image = pygame.image.load('resources/pac_left.png').convert_alpha()
                    movio = True

                    
                #############################################################################
                if eventos.key == pygame.K_UP:
                    Judador.dir = 1
                    Judador.dir2 = 1
                    Judador.image = pygame.image.load('resources/pac_up.png').convert_alpha()
                    movio = True
                    

                if eventos.key == pygame.K_DOWN:
                    Judador.dir = 2
                    Judador.dir2 = 2
                    Judador.image = pygame.image.load('resources/pac_down.png').convert_alpha()
                    movio = True
                    
                if eventos.key == pygame.K_RIGHT:
                    Judador.dir = 3
                    Judador.dir2 = 3
                    Judador.image = pygame.image.load('resources/pac_right.png').convert_alpha()
                    movio = True
                    
                if eventos.key == pygame.K_LEFT:
                    Judador.dir = 4
                    Judador.dir2 = 4
                    Judador.image = pygame.image.load('resources/pac_left.png').convert_alpha()
                    movio = True
                    ##########################################################################

        #Se pone un refresco en fps de 15/segundo
        reloj.tick(15)
        
        #Se pinta la ventana de principal
        ventana.fill(NEGRO)

        #Se dibujan todos los elementos del juego en la ventana
        todos.draw(ventana)

        #Se actualizan todos los elementos del sistema
        todos.update()

        if Judador.finGalletas == 1:
            if Judador.puntaje < max(ListaPuntajes):
                ventana.blit(PonerTitulo("YOU","LOSE!!!"),(450,500))
            else:
                ventana.blit(PonerTitulo("YOU","WIN!!!"),(450,500))
        #Se verifica si el usuario sigue activo
        if MeMori == 1:
            #Si el usuario no esta activo se procede a mostrar un titulo 
            ventana.blit(PonerTitulo("YOU","LOSE!!!"),(450,500))
        #Se pone el puntaje del usuario en la pantalla
        ventana.blit(PonerTitulo(identity.decode('ascii'),Judador.puntaje),(300,570))
        #Se refresca la pantalla nuevamente
        pygame.display.flip()
        #Se actualiza la pantalla
        pygame.display.update()


#Se define la funcion principal del modulo  cliente   
if __name__ == '__main__':
    #Por ultimo se ejecuta la funcion principal, la cual contiene todas la actividades que se realizan al interior del 
    #entorno
    main()
