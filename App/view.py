"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config
from DISClib.ADT import list as lt
from App import controller
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________

accidents_megasmall = 'Copia_us_accidents_small.csv'
accidents_small = 'us_accidents_small.csv'
accidents_2016 = 'us_accidents_dis_2016.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Conocer los accidentes en una fecha")
    print("4- Conocer los accidentes anteriores a una fecha")
    print("5- Conocer los accidentes en un rango de fechas")
    print("6- Conocer el estado con mas accidentes ")
    print("7- Conocer los accidentes por rango de horas")
    print("8- Conocer la zona geográfica mas accidentada")
    print("0- Salir")
    print("*******************************************")

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()
        print("Se creo el analizador con exito")

    elif int(inputs[0]) == 2:
        print("\nCargando información de accidentes ....")
        controller.loadData(cont, accidents_small)
        alt1,alt2 = controller.indexHeight(cont)
        size1,size2 = controller.indexSize(cont)
        min1,min2 = controller.minKey(cont)
        max1,max2 = controller.maxKey(cont)
        print('Accidentes cargados: ' + str(controller.totalAccidentSize(cont)))
        print('Altura del arbol 1: ' + str(alt1))
        print('Cantidad de fechas: ' + str(size1))
        print('Primera fecha registrada: ' + str(min1))
        print('Ultima fecha registrada: ' + str(max1))
        print('Altura del arbol 2: ' + str(alt2))
        print('Cantidad de horas: ' + str(size2))
        print('Primera hora registrada: ' + str(min2))
        print('Ultima hora registrada: ' + str(max2))

    elif int(inputs[0]) == 3:
        print("\nBuscando accidentes en una fecha: ")
        initialDate = input("Fecha (YYYY-MM-DD): ")
        try:
            num_accidents,sev1,sev2,sev3,sev4 = controller.getAccidentsByDate(cont, initialDate)
            print("\nEl total de accidentes en la fecha " + initialDate + " son:  " + str(num_accidents))
            print("\nHubo " + str(sev1) + " accidentes con severidad 1,  "+ str(sev2) + " con severidad 2,  "+ str(sev3) + " con severidad 3 y  "+ str(sev4) + " con severidad 4." )
        except:
            print("Hubo un error al buscar la fecha ingresada")
    elif int(inputs[0]) == 5:
        print("\nBuscando los accidentes en un rango de fechas: ")
        print("\nIngresar las fechas del rango en formato YYYY-MM-DD")
        initialDate = input("Fecha inicial: ")
        finalDate = input("Fecha final: ")
        try:
            num_accidents,mayor = controller.getAccidentsByDateRange(cont, initialDate, finalDate)
            num_sev,sev = mayor
            print("\nEl total de accidentes entre " + initialDate + " y " + finalDate + " son:  " + str(num_accidents))
            print("\nLa severidad más reportada fue la "+ sev + ", esta fue reportada un total de "+ str(num_sev) + " en el rango de fechas" )
        except:
            print("Hubo un error al buscar el rango de fechas ingresado")

    elif int(inputs[0]) == 6:
        print("\nBuscando el estado con más accidentes en un rango de fechas: ")
        print("\nIngresar las fechas del rango en formato YYYY-MM-DD")
        initialDate = input("Fecha inicial: ")
        finalDate = input("Fecha final: ")
        try:
            date,state,num_state = controller.getStateByDateRange(cont, initialDate, finalDate)
            print("\nEl estado con más accidentes entre " + initialDate + " y " + finalDate + " fue "+ str(state) + ", con un total de "+ str(num_state) + " accidentes." )
            print("\nLa fecha con más accidentes en el rango de fechas es:  " + str(date)+ " , con un total de "+ str(num_state) + " accidentes." )
        except:
            print("Hubo un error al buscar el rango de fechas ingresado")
        
    elif int(inputs[0]) == 7:
        print("\nBuscando accidentes por rango de horas: ")
        print("\nIngresar las horas del rango en formato 24 horas (00:00 - 23:59)")
        startHour = input("Hora inicial: ")
        endHour = input("Hora final: ")
        try: 
            num_accidents,sev1,sev2,sev3,sev4 = controller.getAccidentsByHourRange(cont, startHour, endHour)
            per_1,per_2,per_3,per_4= controller.severityPrecent(num_accidents,sev1,sev2,sev3,sev4)
            print("\nEl total de accidentes entre " + startHour + " y " + endHour + " son:  " + str(num_accidents))
            print("\nHubo " + str(sev1) + " accidentes con severidad 1,  "+ str(sev2) + " con severidad 2,  "+ str(sev3) + " con severidad 3 y  "+ str(sev4) + " con severidad 4." )
            print("\nY sus porcentajes son " + str(per_1) + ",  "+ str(per_2) + ",  "+ str(per_3) + " y  "+ str(per_4) + " respectivamente." )
        except:
            print("Hubo un error al buscar el rango de horas ingresado")
    else:
        sys.exit(0)
sys.exit(0)
