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
    print("3-  Conocer los accidentes en una fecha")
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
        print('Accidentes cargados: ' + str(controller.totalAccidentSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Cantidad de fechas: ' + str(controller.indexSize(cont)))
        print('Primera fecha registrada: ' + str(controller.minKey(cont)))
        print('Ultima fecha registrada: ' + str(controller.maxKey(cont)))

    elif int(inputs[0]) == 3:
        print("\nBuscando accidentes en una fecha: ")
        initialDate = input("Fecha (YYYY-MM-DD): ")
        num_accidents,sev1,sev2,sev3,sev4 = controller.getAccidentsByDate(cont, initialDate)
        print("\nEl total de accidentes en la fecha " + initialDate + " son:  " + str(num_accidents))
        print("\nHubo " + str(sev1) + " accidentes con severidad 1,  "+ str(sev2) + " con severidad 2,  "+ str(sev3) + " con severidad 3 y  "+ str(sev4) + " con severidad 4." )

    else:
        sys.exit(0)
sys.exit(0)
