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

#Creamos la matriz que nos servira de guia para crear el mapa de cada usuario que se conecte
matrizmapa = [[3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
			  [0,1,0,1,0,0,1,1,1,0,0,1,0,0,1,1,1,1,0,0],
			  [0,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0],
			  [0,1,0,0,1,1,1,1,1,1,1,0,0,1,1,0,0,1,0,0],
			  [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1],
			  [0,1,0,1,0,0,1,1,1,1,1,1,1,1,0,1,0,1,0,1],
			  [0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1],
			  [0,1,0,1,0,0,1,0,0,0,0,0,0,1,0,1,0,1,0,1],
			  [0,1,0,1,0,0,1,1,1,1,1,1,1,1,0,1,0,1,0,0],
			  [0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			  [0,1,0,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
			  [3,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,3]]

#Se crea una funcion que mostrara varios titulos al inicio de la ejecucion
def Titulos():
	print("\t\t     BosiElGato ")
	print("\t\t All Rights Reserved ")
	print("\t\t    Activated Server ")
	print("\t\t    Enjoy The Game ")

#Creamos una funcioon donde se van a controlar todos los eventos entrantes y se va a hacer el broadcast hacia
#Todos los usuarios que se encuentren conectados
def main():

	#En la lista de jugadores se agregaran todos los usuarios nuevos que se vayan uniendo el juego
	ListaJugadores = []
	#El numero de jugadores nos ayudara a monitorear el numero de usuarios que ingresan al juego 
	NumeroDeJugadores = 0


	#Creamos el contexto o entorno donde ejecutaremos las conexiones 
	context = zmq.Context()

	#Se define de que tipo va a ser el contexto, en este caso vamos a trabajar con ROUTER y DEALER que son ideales
	#Para la difusion
	socket = context.socket(zmq.ROUTER)

	#Se le asigna una direccion IP y un puerto donde se van a recibir todas las solicitudes
	socket.bind("tcp://*:4444")

	# Se verifica que despues de la ejecucion del programa no haya ningun otro argumento
	if len(sys.argv) != 1:

		#En caso de haber un argumento se le indica al usuario que no debe poner argumentos
		print("Must be called with no arguments")

		#Se termina la ejecucion del programa para que el usuario pueda repetir la operacion
		exit()

	#Se llama la funcion Titulos previamente definida
	Titulos()
	
	#Se inicia el servidor y se mantiene activado mientras el usuario no lo cierre 
	while True:		
		#A traves de la libreria de ZMQ podemos recibir las peticiones de los usuarios, en este caso
		#Recibimos su nombre y lo almacenamos en una variable llamada nombre
		nombre = socket.recv()

		#Se recibe el mensaje asociado al usuario, este mensaje contiene varios campos de informacion que es
		#Enviada por los clientes
		MensajeEntrada = socket.recv_multipart()


		#Como ya dijimos el mensaje de cada cliente esta compuesto por varias partes, las partes que contiene son:
		# -Primera casilla se encuentra el numero de jugador que es asignado una vez se conecta 
		# -En la segunda casilla se encuentra la posicion en x del jugador en el mapa 
		# -En la tercera casilla se encuentra la posicion en y del jugador en el mapa
		# -En la cuarta casilla se encuenta un valor que indica si el pacman perteneciente al usuario ha 
		#	 colisionado con una galleta tipo1, en otras palabras si ha comido una galleta
		#- En la ultima posicion se encuentra un valor que indica si el pacman ha colisionado con la galleta tipo2
		#	la cual le da la habilidad de convertir a otros pacman en fantasmas y comerselos

		#Se deodifica el mensaje y se convierte a numeros para poder interpretarlo
		MensajeDecode = eval(MensajeEntrada[0].decode('ascii'))
		posicion = 0

		#Se verifica que el usuario que llega este registrado para proceder a enviarle informacion pertinente
		if MensajeDecode[0] != 0:
			#print(NumeroDeJugadores)
			#*************************Funcion de BROADCAST ****************
			#Esta funcion es la mas importante en esta seccion ya que le informa a todos lo clientes menos 
			#a quien envia el mensaje que ha recibido un evento para que los demas actualizen sus mapas y eventos

			# Se recorre toda la lista de jugadores registrados y se procede a enviar la informacion 
			#del ultimo usuario que registro un evento
			for Destino in ListaJugadores:
				#Se verifica si el ultimo jugador que registro el evento no sea igual al destino del 
				#Mensaje, esto para evitar que se envie la informacion a si mismo
				if Destino != nombre:
					#Se envia la informacion del ultimo usuario al destino osea a los otros jugadores
					socket.send_multipart([Destino,nombre,MensajeEntrada[0]])

			#*******************Fin       BROADCAST          ******************
		#Si el usuario no existe aun en el juego se procede a enviar informacion para que cargue su sistema
		else:
			print("{} Se ha conectado.".format(nombre.decode('ascii')))
			#Se agrega el nuevo usuario a la lista de usuarios
			ListaJugadores.append(nombre)
			
			#Se agrega uno a la variable que contiene el numero de jugadores
			NumeroDeJugadores += 1

			#Se envia la matriz del mapa actualizada y el numero de jugadores que hay 
			socket.send_multipart([nombre, bytes(str(matrizmapa),'ascii'),bytes(str(NumeroDeJugadores),'ascii')])

		#Por otra parte si el usuario existe se verifica si ha comido alguna galleta tipo1 o galleta tipo2
		if MensajeDecode[3] ==1 or MensajeDecode[4] == 1:
			#Si ha colisionado con alguna de las galletas se procede a actualizar la matriz para poder enviar
			#Informacion coherente a todos los usuarios que se vayan conectando
			#Se recibe la posicion en x de el evento
			a = int(MensajeDecode[1]/50)

			#Se recibe la posicion en y el evento
			b = int(MensajeDecode[2]/50)

			#Se actualiza la posicion x, y del evento en la matriz del mapa
			matrizmapa[b][a] = 4

#Se define la funcion principal del modulo servidor
if __name__ == '__main__':

	#Se llama a la funcion que contiene todas las funciones para cargar el servidor
	main()
