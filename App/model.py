import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria

"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------

def newAnalyzer():
    """ Inicializa el analizador
    Crea una lista vacia para guardar todos los accidentes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas
    Retorna el analizador inicializado.
    """
    analyzer = {'accidents': None,
                'dateIndex': None
                }

    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compare)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compare)
    return analyzer

# Funciones para agregar informacion al catalogo

def addAccident(analyzer, accident):
    """
    """
    lt.addLast(analyzer['accidents'], accident)
    updateDateIndex(analyzer['dateIndex'], accident)
    return analyzer

def updateDateIndex(map, accident):
    """
    Se toma la fecha del accidente y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de accidentes
    y se actualiza el indice de tipos de accidentes.
    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de accidentes
    """
    occurreddate = accident['Start_Time']
    accidentdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentdate.date())
    if entry is None:
        datentry = newDataEntry()
        om.put(map, accidentdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accident)
    return map

def addDateIndex(datentry, accident):
    """
    Actualiza un indice de tipo de accidentes.  Este indice tiene una lista
    de accidentes y una tabla de hash cuya llave es el tipo de accidente y
    el valor es una lista con los accidentes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    datentry['num_accidents'] += 1
    severityIndex = datentry['severityIndex']
    accidntentry = lt.getElement(severityIndex, int(accident['Severity']))
    entry = accidntentry
    lt.addLast(entry['lstseverities'], accident)
    return datentry

def newDataEntry():
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'severityIndex': None, "num_accidents":0}
    entry['severityIndex'] = lt.newList("ARRAY_LIST", compare)
    for i in range (0,4):
        sev_entry = newSeverityEntry(i+1)
        lt.addLast(entry['severityIndex'],sev_entry)
    return entry

def newSeverityEntry(severityNum):
    """
    Crea una entrada en el indice por numero de severidad del accidente, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    seventry = {'number': None, 'lstseverities': None}
    seventry['number'] = severityNum
    seventry['lstseverities'] = lt.newList('SINGLELINKED', compare)
    return seventry

# ==============================
# Funciones de consulta
# ==============================
def getAccidentsByDate(analyzer, initialDate):
    """
    Para una fecha determinada, retorna el numero de accidentes
    por severidad .
    """
    accidentdate = om.get(analyzer['dateIndex'], initialDate)    
    return me.getValue(accidentdate)

def getSeverity(lst,severity):
    return lt.getElement(lst,severity)['lstseverities']

def accidentsSize(lst):
    """
    Número de accidentes cargados
    """
    if lst is None:
        return 0
    else:
        return lt.size(lst)

def indexHeight(analyzer):
    """Altura del arbol
    """
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    """Cantidad de fechas
    """
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    """Fecha primer registro de accidentes
    """
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    """Fecha ultimo registro de accidentes
    """
    return om.maxKey(analyzer['dateIndex'])

# ==============================
# Funciones de Comparacion
# ==============================

def compare(elemnt1, elemnt2):
    """
    Compara elementos
    """
    if (elemnt1 == elemnt2):
        return 0
    elif elemnt1 > elemnt2:
        return 1
    else:
        return -1



