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
                'dateIndex': None,
                "hours":None
                }

    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compare)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compare)
    analyzer["hours"] = om.newMap(omaptype='RBT',
                                      comparefunction=compare)
    #EN CASO DE QUE SEA EN GENERAL
    return analyzer

# Funciones para agregar informacion al catalogo

def addAccident(analyzer, accident):
    """
    """
    lt.addLast(analyzer['accidents'], accident)
    updateDateIndex(analyzer['dateIndex'], accident)
    updateHourIndex(analyzer["hours"], accident)
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

def updateHourIndex(map, accident):
    """
    Se toma la fecha del accidente, se aproxima la hora en 
    intervalos de 30 min y se busca si ya existe en el arbol
    dicha hora.  Si es asi, se adiciona a su lista de accidentes
    y se actualiza el indice de tipos de accidentes.
    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de accidentes
    """
    occurreddate = accident['Start_Time']
    accidentdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    hour = roundedTime(accidentdate)
    entry = om.get(map, hour)
    if entry is None:
        hourentry = newDataEntry()
        om.put(map, hour, hourentry)
    else:
        hourentry = me.getValue(entry)
    addDateIndex(hourentry, accident)
    return map

def addDateIndex(datentry, accident):
    """
    Actualiza un indice de tipo de accidentes.  Este indice tiene una lista
    de accidentes y un arreglo donde su posicion es el numero de severidad y
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

def getAccidentsByDateRange(analyzer, initialDate, finalDate):
    """
    Para una un rango de fechas determinado, retorna el numero
    de accidentes por severidad .
    """
    accidentdate = om.values(analyzer['dateIndex'], initialDate, finalDate)    
    return accidentdate

def getAccidentsByHourRange(analyzer, startHour, endHour):
    """
    Para una fecha determinada, retorna el numero de accidentes
    por severidad .
    """
    startHour = roundedTime(startHour)
    endHour = roundedTime(endHour)
    if startHour < endHour:
        accidentdate = om.values(analyzer["hours"], startHour, endHour)
    elif endHour.isoformat() == "00:00:00":
        maxKey = om.maxKey(analyzer["hours"])
        accidentdate = om.values(analyzer["hours"], startHour, maxKey)
    return accidentdate

def getSeverity(lst,severity):
    return lt.getElement(lst,severity)['lstseverities']

def severityPrecent (num_accidents, sev_num):
    """
    Obtiene el porcentaje de una severidad
    en la cantidad total de accidentes
    """
    percent = (sev_num / num_accidents)*100
    return str(percent)+"%"

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
    h1=om.height(analyzer['dateIndex'])
    h2=om.height(analyzer["hours"])
    return (h1,h2)


def indexSize(analyzer):
    """Cantidad llaves
    """
    s1=om.size(analyzer['dateIndex'])
    s2=om.size(analyzer["hours"])
    return (s1,s2)


def minKey(analyzer):
    """Llave menor
    """
    mi1=om.minKey(analyzer['dateIndex'])
    mi2=om.minKey(analyzer["hours"])
    return (mi1,mi2)


def maxKey(analyzer):
    """Llave mayor
    """
    ma1=om.maxKey(analyzer['dateIndex'])
    ma2=om.maxKey(analyzer["hours"])
    return (ma1,ma2)

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

# ==============================
# Funciones de Ayuda
# ==============================

def roundedTime (accidentdate):
    time = accidentdate.time()
    time = time.isoformat()
    if (int(time[3:5])) <15:
        minute = 00
        hour = (int(time[:2]))
    elif (int(time[3:5])) <45:
        minute = 30
        hour = (int(time[:2]))
    else:
        minute = 00
        hour = ((int(time[:2]))+1)%24
    new = accidentdate.replace(hour=hour, minute=minute, second=00)
    new = new.time()
    return new