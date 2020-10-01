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
    sev1 = model.accidentsSize(model.getSeverity(severities,1))
    sev2 = model.accidentsSize(model.getSeverity(severities,2))
    sev3 = model.accidentsSize(model.getSeverity(severities,3))
    sev4 = model.accidentsSize(model.getSeverity(severities,4))  
    return(num_accidents,sev1,sev2,sev3,sev4)

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
