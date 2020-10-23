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

import config as cf
from App import model
from DISClib.DataStructures import listiterator as it
import datetime
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init():
    """
    Llama la funcion de inicializacion del modelo.
    """
    analizer = model.newAnalyzer()
    return analizer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, accidentsfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    accidentsfile = cf.data_dir + accidentsfile
    input_file = csv.DictReader(open(accidentsfile, encoding="utf-8"),
                                delimiter=",")
    for accident in input_file:
        model.addAccident(analyzer, accident)
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________
def getAccidentsByDate(analyzer, initialDate):
    """
    Retorna los accidentes por fecha y su severidad
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    dataentry = model.getAccidentsByDate(analyzer, initialDate.date())
    num_accidents = dataentry["num_accidents"]
    severities = dataentry['severityIndex']
    sev1,sev2,sev3,sev4 = getSeverities(severities)
    return(num_accidents,sev1,sev2,sev3,sev4)

def getAccidentsBeforeDate (analyzer, finalDate):
    """
    Retorna los accidentes anteriores a una fecha y la fecha con más accidentes
    """
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    dataentry,keys = model.getAccidentsBeforeDate(analyzer,finalDate.date())
    num_accidents,fecha = getInfo(dataentry,keys)
    return (num_accidents,fecha)


def getAccidentsByDateRange(analyzer, initialDate, finalDate):
    """
    Retorna los accidentes por fecha y su severidad
    más reportada
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    dataentry = model.getAccidentsByDateRange(analyzer, initialDate.date(), finalDate.date())
    num_accidents,sev1,sev2,sev3,sev4 = getTotalInfo(dataentry)
    mayor = (max((sev1,"severidad 1"),(sev2,"severidad 2"),(sev3,"severidad 3"),(sev4,"severidad 4")))
    return(num_accidents,mayor)

def getStateByDateRange(analyzer, initialDate, finalDate):
    """
    Retorna los accidentes por fecha y su severidad
    más reportada
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    accidentdate= model.getStateByDateRange(analyzer, initialDate.date(), finalDate.date())
    state,date,num=getDate(accidentdate)
    return(state,date,num)

def getAccidentsByHourRange(analyzer, startHour, endHour):
    """
    Retorna los accidentes por rango de horas y su severidad
    """
    startHour=startHour+":00"
    startHour = datetime.datetime.strptime(startHour, '%H:%M:%S')
    endHour=endHour+":00"
    endHour = datetime.datetime.strptime(endHour, '%H:%M:%S')
    hourentry = model.getAccidentsByHourRange(analyzer, startHour, endHour)
    return getTotalInfo(hourentry)

def getAccidentsByLat(analyzer, lat, lon, distance):
    """
    Retorna los accidentes dentro de un radio en un punto específico por días
    """
    dataentry=model.getAccidentsByLat(analyzer, lat, lon, distance)
    dias,total=getLatInfo(dataentry)
    return (dias,total)



def getTotalInfo(lstValues):
    """
    Obtiene la cantidad total de accidentes y severidades
    para una lista de valores
    """
    num_accidents = 0
    iterator = it.newIterator(lstValues)
    sev1 = 0
    sev2 = 0
    sev3 = 0
    sev4 = 0
    while  it.hasNext(iterator):
        element = it.next(iterator)
        num_accidents += element["num_accidents"]
        severities = element['severityIndex']
        sev_1,sev_2,sev_3,sev_4 = getSeverities(severities)
        sev1 = sev1 + sev_1
        sev2 = sev2 + sev_2
        sev3 = sev3 + sev_3
        sev4 = sev4 + sev_4
    
    return(num_accidents,sev1,sev2,sev3,sev4)


def getDate(lstValues):
    maxi=0
    date=''
    state=''
    iterator = it.newIterator(lstValues)
    while  it.hasNext(iterator):
        element = it.next(iterator)
        if element["num_accidents"] > maxi:
            maxi= element["num_accidents"]
            date=element["date"]
            state=element["lststate"]["elements"][0]
    return (date,state,maxi)

def getLatInfo(lstValues):
    """
    Obtiene la cantidad total de accidentes 
    """
    iterator=it.newIterator(lstValues)
    semana = [0,0,0,0,0,0,0]
    total = 0
    while it.hasNext(iterator):
        element1=it.next(iterator)
        iteratora=it.newIterator(element1)
        while it.hasNext(iteratora):
            contador=0
            element = it.next(iteratora)
            iterator1 = it.newIterator(element["weekday"])
            while it.hasNext(iterator1):
                element1 = it.next(iterator1)
                if element1>0:
                    semana[contador]+=element["num_accidents"]
                contador+=1
                total += 1
    return (semana,total)
    

def getSeverities(severities):
    """
    Obtiene la cantidad de elementos en la lista de
    cada severidad
    """
    sev1 = model.accidentsSize(model.getSeverity(severities,1))
    sev2 = model.accidentsSize(model.getSeverity(severities,2))
    sev3 = model.accidentsSize(model.getSeverity(severities,3))
    sev4 = model.accidentsSize(model.getSeverity(severities,4)) 
    return (sev1,sev2,sev3,sev4)

def severityPrecent (num_accidents,sev1,sev2,sev3,sev4):
    """
    Obtiene el porcentaje de una severidad
    """
    sev1 = model.severityPrecent(num_accidents, sev1)
    sev2 = model.severityPrecent(num_accidents, sev2)
    sev3 = model.severityPrecent(num_accidents, sev3)
    sev4 = model.severityPrecent(num_accidents, sev4)
    return (sev1,sev2,sev3,sev4)
  
def getInfo (lstValues1,lstValues2):
    """
    Obtiene la cantidad total de accidentes 
    """
    num_accidents = 0
    mayor = 0
    iterator1 = it.newIterator(lstValues1)
    iterator2 = it.newIterator(lstValues2)
    while  it.hasNext(iterator1):
        element1 = it.next(iterator1)
        element2 = it.next(iterator2)
        num_accidents += element1["num_accidents"]
        if element1["num_accidents"]>mayor:
            mayor=element1["num_accidents"]
            fecha=element2
    
    return (num_accidents,fecha)

def totalAccidentSize(analyzer):
    """
    Numero de accidentes
    """
    return model.accidentsSize(analyzer['accidents'])

def accidentSize(lst):
    """
    Numero de accidentes
    """
    return model.accidentsSize(lst)

def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)


def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)
