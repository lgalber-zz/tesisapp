# Para los acentos
# -*- encoding: utf-8 -*-
#!/usr/bin/python

# Aplicación simple para configuración de los nodos.
# Incluye compilación de código y grabado con avrdude.


# Tkinter in Python 2.7 & tkinter in 3.2
from Tkinter import *
import ttk
import subprocess as sub, os
from subprocess import Popen, PIPE
import tkMessageBox

# Funcion para realizar la grabación en la placa cuando se aprieta el botón
def AvrBurn():
	global DIR
	out = os.system("/usr/bin/avrdude -pm1281 -cjtagmkII -Pusb -b38400 -u -Uflash:w:"+DIR+"/examples/uDTN/simple-transceiver/simple-transceiver.hex:a -Ueeprom:w:"+DIR+"/examples/uDTN/simple-transceiver/simple-transceiver.eep:a -Ulfuse:w:0xe2:m -Uhfuse:w:0x9d:m -Uefuse:w:0xff:m -Ulock:w:0xff:m")
	#proc = sub.Popen(["/usr/bin/avrdude -pm1281 -cjtagmkII -Pusb -b38400 -u -Uflash:w:"+DIR+"/examples/uDTN/simple-transceiver/simple-transceiver.hex:a -Ueeprom:w:"+DIR+"/examples/uDTN/simple-transceiver/simple-transceiver.eep:a -Ulfuse:w:0xe2:m -Uhfuse:w:0x9d:m -Uefuse:w:0xff:m -Ulock:w:0xff:m"], stdout=sub.PIPE, shell=True)
	"""(out, err) = proc.communicate()
	s1 = out.split('avrdude')[1]
	print("S1:"+s1)
	print("ERROR:"+ str(err))
	"""	
	# Mensajes de error u éxito de la grabación
	if out != 0 :
		tkMessageBox.showerror("Error","Hubo un error en la grabación, Verifique el grabador y la placa.")
	else:
		tkMessageBox.showinfo("Terminado","Grabación realizada con éxito.")

# Función para realizar el Clean y luego el Make del código.
def DoMake():
	global burn,out,DIR
	DIR = dirEntry.get()	
	MACN = MACEntry.get()
    	ND = Nodo_Destino.get()
	NUM = numEntry.get()
#	ENVIAR = enviarEntry.get()
	FC = frecuenciaEntry.get()
	LIFETIME = str(int(lifetimeDias.get())*86400+int(lifetimeHoras.get())*3600+int(lifetimeMins.get())*60+int(lifetimeSegs.get()))
	LONGPAY = payloadEntry.get()

	# Mensaje de Path incorrecto
	if os.path.isdir(DIR) == False: 
		tkMessageBox.showerror("Error","Path incorrecto.")

	if int(LONGPAY) > 79 or int(NUM) > 100 or int(LONGPAY) < 0 or int(NUM) < 0 or int(ND) < 0 or int(FC) < 0 :
		error = 1
	else:

		error = 0

	COLLEC = colectorEntry.get()
	if int(COLLEC) == 1:
		ENVIAR = '0'
	else:
		ENVIAR = '1'
	TX = str(txEntry.get())
	RX = str(rxEntry.get())
	# Nos movemos de directorio	
	os.chdir(DIR+'/examples/uDTN/simple-transceiver')
	# Hacemos clean	
	out = os.system("make clean")
	os.system("rm -rf Makefile.zigbit")
	os.system("cp Makefile.zigbit.default Makefile.zigbit")	
	# Agregamos al Makefile.zigbit los parametros seteados con la app
        f = open(DIR+'/examples/uDTN/simple-transceiver/Makefile.zigbit', 'a')
    # Se escribe en el archivo Makefile.zigbit todas las configuraciones seteadas
	f.write("CONF_MAC=" + MACN + "\n" + "SEND_TO_NODE=" + ND + "\n" + "BUNDLE_CONF_STORAGE_SIZE=" + str(int(NUM)+1) + "\n" + "CONF_ENVIAR=" + ENVIAR + "\n")
	f.write("CONF_FRECUENCIA=" + FC + "\n" + "CONF_LIFETIME=" + LIFETIME + "\n" + "CONF_LONGITUD=" + LONGPAY + "\n")
	f.write("CONF_COLLECTOR=" + COLLEC + "\n" + "CONF_RF230_MAX_TX_POWER=" + TX + "\n" + "CONF_RF230_MIN_RX_POWER=" + RX + "\n")	
	f.close()	

	# Control de errores en los campos ingresados
	if error == 0:
		# Hacemos make

		#out = os.system("make")
		proc = sub.Popen(["make", DIR+"/examples/uDTN/simple-transceiver/"], stdout=sub.PIPE, shell=True)
		(out, err) = proc.communicate()
		s2 = out.split('avr-size -C --mcu=atmega1281 simple-transceiver.elf')[1]


		if err != None :	
			tkMessageBox.showerror("Error","Hubo un error en la compilacion, Verifique los parametros y vuelva a compilar.")
		else:
			burn = burn +1;		
			tkMessageBox.showinfo("Terminado","Configuración realizada con éxito.\n" + s2)
		if burn==1:		
			burn = 2		
			burnButton = Button(root, text='AVR - Burn', bd=1, fg='green',relief='groove',command=AvrBurn)
	        	burnButton.grid(row=200,column=0,columnspan=4)	
	else:
		tkMessageBox.showerror("Error","Error en configuración de parametros.\nChequear:\n Dirección MAC\n Nodo Destino\n Bundles en RAM\n Frecuencia de Toma de Datos\n")
		error = 0

# Se define una función que habilita o deshabilita los parámetros dependiendo de si se va a configurar un Colector o un nodo Generador
def Config(col):
	global dirEntry, MACEntry, Nodo_Destino, numEntry, frecuenciaEntry, lifetimeDias, lifetimeHoras, lifetimeMins, lifetimeSegs,payloadEntry,txEntry,rxEntry,colectorEntry
## Set root directory
	directory =  Label(root, text='Directorio raiz de Contiki')
	directory.grid(row=20,column=0,columnspan=7)
	dirEntry = Entry(root, bd=1, relief='sunken')
	dirEntry.insert(0,"/home/USUARIO/workspace/udtn")
	dirEntry.grid(row=21,column=0,columnspan=7)    	
	###############################################
## Set MAC
	MAC = Label(root, text='MAC Nodo')
	MAC.grid(row=30,column=0,columnspan=7)
	MACEntry = Entry(root, bd=1, relief='sunken')
	MACEntry.insert(0,"0x20")
	MACEntry.grid(row=31,column=0,columnspan=7)
###############################################
	## Set Nodo Destino
	NodoDestino = Label(root, text='Nodo Destino')
	NodoDestino.grid(row=40,column=0,columnspan=7)
	Nodo_Destino = Entry(root, bd=1, relief='sunken')
	Nodo_Destino.insert(0,80)
	Nodo_Destino.grid(row=41,column=0,columnspan=7)
###############################################
## Set Numero de Bundles
	numLabel = Label(root, text='Número de Bundles RAM')
	numLabel.grid(row=50,column=0,columnspan=7)
	numEntry = Entry(root, bd=1, relief='sunken')
	numEntry.insert(0,"10")
	numEntry.grid(row=51,column=0,columnspan=7)	
###############################################
## Set Frecuencia de Creacion
	frecuenciaLabel = Label(root, text='Frecuencia Toma de Datos')
	frecuenciaLabel.grid(row=60,column=0,columnspan=7)
	frecuenciaEntry = Entry(root, bd=1, relief='sunken')
	frecuenciaEntry.insert(0,"60")
	frecuenciaEntry.grid(row=61,column=0,columnspan=7)
###############################################
## Set LIFETIME del Bundle
	lifetimeLabel = Label(root, text='LifeTime Bundle (DD:HH:MM:SS)')
	lifetimeLabel.grid(row=70,column=0,columnspan=7)
	lifetimeDias = StringVar()
	BoxDias = ttk.Combobox(root, textvariable=lifetimeDias, values= (range(0,11)),width= 3, cursor="left_ptr")
	BoxDias.set(0)
	BoxDias.grid(row=71,column=0)
	d = Label(root, text=':')
	d.grid(row=71,column=1)
	lifetimeHoras = StringVar()
	BoxHoras = ttk.Combobox(root, textvariable=lifetimeHoras, values= (range(0,24)),width= 3, cursor="left_ptr")
	BoxHoras.set(1)
	BoxHoras.grid(row=71,column=2)
	h = Label(root, text=':')
	h.grid(row=71,column=3)
	lifetimeMins = StringVar()
	BoxMinutos = ttk.Combobox(root, textvariable=lifetimeMins, values= (range(0,60)),width= 3, cursor="left_ptr")
	BoxMinutos.set(0)
	BoxMinutos.grid(row=71,column=4)
	m = Label(root, text=':')
	m.grid(row=71,column=5)
	lifetimeSegs = StringVar()
	BoxSegundos = ttk.Combobox(root, textvariable=lifetimeSegs, values= (range(0,60)),width= 3, cursor="left_ptr")
	BoxSegundos.set(0)
	BoxSegundos.grid(row=71,column=6)
	###############################################
	## Set Longitud Payload
	payloadLabel = Label(root, text='Longitud Payload')
	payloadLabel.grid(row=80,column=0,columnspan=7)
	payloadEntry = Entry(root, bd=1, relief='sunken')
	payloadEntry.insert(0,"79")
	payloadEntry.grid(row=81,column=0,columnspan=7)
	###############################################
	## Set TX_MAX
	txLabel = Label(root, text='Potencia TX (Max=0)')
	txLabel.grid(row=90,column=0,columnspan=7)
	txEntry = Scale(root, bd=1, cursor="left_ptr",digits="2",from_="15",orient="horizontal",relief='sunken',resolution="1",showvalue="1",to="0",length=200)
	txEntry.grid(row=91,column=0,columnspan=7)
###############################################
## Set RX_MIN
	rxLabel = Label(root, text='Sensibilidad RX (Max=0)')
	rxLabel.grid(row=100,column=0,columnspan=7)
	rxEntry = Scale(root, bd=1, cursor="left_ptr",digits="2",from_="84",orient="horizontal",relief='sunken',resolution="1",showvalue="1",to="0",length=200)
	rxEntry.grid(row=101,column=0,columnspan=7)
###############################################
	makeButton = Button(root, text='Clean & Make', bd=1, fg='white',relief='groove',command=DoMake)
	makeButton.grid(row=200,column=4,columnspan=4)
	colectorEntry = StringVar()
	
	# Si es Colector algunos parámetros se deshabilitan para que no puedan ser seteados.
	if col == 1:
		Nodo_Destino.configure(state='readonly')
		payloadEntry.configure(state='readonly')
		BoxDias.configure(state='disable')
		BoxHoras.configure(state='disable')
		BoxMinutos.configure(state='disable')
		BoxSegundos.configure(state='disable')
		frecuenciaEntry.configure(state='readonly')
		numEntry.configure(state='readonly')
		colectorEntry.set(1)
	else:
		colectorEntry.set(0)



root = Tk()
root.title("Config")
global out,burn	
out = 0
burn = 0 
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 4
root.geometry("+%d+%d" % (x, y))

## Set Collector o No
"""colectorLabel = Label(root, text='Colector?')
colectorLabel.grid(row=10,column=0,columnspan=7)
colectorEntry = StringVar()
colectorSi = Radiobutton(root, text="SI", variable= colectorEntry, value=1,cursor="hand2")
colectorSi.grid(row=11,column=2,columnspan=1)
colectorNo = Radiobutton(root, text="NO", variable= colectorEntry, value=0,cursor="hand2")
colectorNo.grid(row=11,column=4,columnspan=1)
"""
# Botones para seleccionar  Colector o NO
WelLabel = Label(root, text='Bienvenido a la API de configuración\n')
WelLabel.grid(row=0,column=0,columnspan=7)
ColectorLabel = Label(root, text='Configurar Colector')
ColectorLabel.grid(row=5,column=0,columnspan=7)
yesButton = Button(root, text='SI', bd=1, fg='white',relief='groove',command=lambda:Config(1))
yesButton.grid(row=10,column=0,columnspan=5)
noButton = Button(root, text='NO', bd=1, fg='white',relief='groove',command=lambda:Config(0))
noButton.grid(row=10,column=2,columnspan=5)



    
root.mainloop()
