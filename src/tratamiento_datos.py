import numpy as np
from pandas.core.common import flatten
import pandas as pd


from pymongo import MongoClient
client = MongoClient("localhost:27017")
client

db = client.get_database("ironhack")

def calcular_coste_value(diccionario):
    '''
    Calculate value 'coste' by value 'numero' and value 'sueldo'
    Args:
        dictionary
    '''
    
    for k,v in diccionario.items():
        v['coste'] = v['numero'] * v['sueldo']
    
    maximo = 0
    for k, v in diccionario.items():
        if v['coste'] > maximo:
            maximo = v['coste']
            
    for k,v in diccionario.items():
        v['requirement_value'] = round( (v['coste'] * 10) / maximo, 2)



def calc_requirement_value(valor, maximo):
    '''
    Assign a proportional number (1-10) to a specific value
    Args:
        valor: int (is a value tu convert)
        maximo: int (is the convertion pattern)
    Returns:
        Rounded scaled value
    '''
    return round ((valor * 10) / maximo, 2)


def limpiar_offices(lista):
    '''
    Remove all useless info for this proyect in a list obatained by mongo query
    Args:
        List to reduce
    '''
    for empresa in lista:
        for elem in empresa['offices']:
            dato = elem['city']
            elem.clear()
            elem['city'] = dato


def pasar_float(lista):
    '''
    Convert a string that defines a value in the value itself
    Args:
        List that contains the value
    '''
    for elem in lista:
        try:
            
            elem['total_money_raised'] = elem['total_money_raised'].strip()[1:]
            

            if 'M' in elem['total_money_raised'].upper():
                dinero = float(elem['total_money_raised'][:-1])*1000000
                elem['total_money_raised'] = dinero

            elif 'B' in elem['total_money_raised'].upper():
                dinero = float(elem['total_money_raised'][:-1])*1000000000
                elem['total_money_raised'] = dinero

            elif 'K' in elem['total_money_raised'].upper():
                dinero = float(elem['total_money_raised'][:-1])*1000
                elem['total_money_raised'] = dinero
                
        except:
            #print (elem)
            pass



def limpiar_1m(lista):
    '''
    Create a list with the companies with more than 1000000$ raised
    Args:
        List that contains companies
    Return
        The new list: list()
    '''
    lista_1m = list()
    for elem in lista:
        try:
            if elem['total_money_raised'] >= 1000000:
                lista_1m.append(elem)
        except:
            pass
    return lista_1m



def limpiar_sector(lista):
    '''
    Create a list with the companies with more than 1000000$ raised and his field are the Tech
    Args:
        List that contains companies
    Return
        The new list: list()
    '''
    sector =['analytics', 'design', 'ecommerce', 'games_video', 'hardware', 'mobile', 'network_hosting',  'social', 'software', 'web']
    lista_1m_sector = list()
    
    for elem in lista:
        for tag in sector:
            try:
                if tag in elem['category_code']:
                    lista_1m_sector.append(elem)
            except:
                pass

    return lista_1m_sector



def seleccionar_ciudades(lista):
    '''
    Create a list with the cities in which have office the companies with more than 1000000$ raised and his field are the Tech
    Args:
        List that contains cities
    Return
        The new list: list()
    '''
    lista_ciudades = list()
    for elem in lista:
        for ciudad in elem['offices']:
            lista_ciudades.append(ciudad['city'])
    return lista_ciudades


def pasar_a_euros_cv(elem):
    '''
    Convert a value index into a value money for a 'cv' index
    Args:
        int 'elem': The value to convert
    Return
        float: Converted value rounded by two decimals
    '''    
    coste_vida_NY = [619, 2000, 2619]
    indice = 0
    return round((elem/100) * coste_vida_NY[indice], 2)
    
    
def pasar_a_euros_a(elem):
    '''
    Convert a value index into a value money for a 'a' index
    Args:
        int 'elem': The value to convert
    Return
        float: Converted value rounded by two decimals
    ''' 
    coste_vida_NY = [619, 2000, 2619]
    indice = 1
    return round((elem/100) * coste_vida_NY[indice], 2)


def pasar_a_euros_cva(elem):
    '''
    Convert a value index into a value money for a 'cva' index
    Args:
        int 'elem': The value to convert
    Return
        float: Converted value rounded by two decimals
    '''
    coste_vida_NY = [619, 2000, 2619]
    indice = 2
    return round((elem/100) * coste_vida_NY[indice], 2)



def filtrar_empresas_ciudad (lista_empresas, empresas_filtradas):
    '''
    Creates a new list based on the intersection of the cities obtained and the companies' cities filtered before
    Args:
        list(): List of the cities
        list(): List of the companies' cities
    Return:
        list(): The new list that contains the intersection values
    '''
    lista_limpia = list()
    respuesta = list()
    for elem in lista_empresas:
        lista_limpia.append(elem['name'])
    
    for elem in empresas_filtradas:
            
            for e in lista_limpia:
               
                try:
                    if e in elem['name']:
                        respuesta.append(e)
                except:
                    pass
    return respuesta


def guardar_historico(historico, lista_resultados):
    '''
    Creates a list that stores coordinate from queries, making a choices tree on successful results in queries
    Args:
        list(): Coordinates stored before
        list(): Queries' results
    Return:
        list(): A list that contains the combinations between the two args
    '''    
    respuesta = []
    contador = 0

    for elem in lista_resultados:
        
        if len(elem) == 0:
            print('No ha habido coincidencias en el elem')
            pass

        elif type(elem[0]) != list:
            
            if len(elem) == 0:
                pass
            else:
                aux = [historico[contador], elem]
                respuesta.append(aux)
            
        elif type(elem[0]) == list:
            for lista in elem:
                if len(lista) == 0:
                    pass
                else:
                    aux = [historico[contador], lista]
                    respuesta.append(aux)
            contador += 1
                
    respuesta = limpiar_historico(respuesta)          
    return respuesta



def limpiar_historico(historico):
    '''
    Cleans a list of lists to handle it properly
    Args:
        list(): List to clean
    Return:
        list(): A cleaned list
    '''    
    historico_limpio = []
    for elem in historico:
        flat_list = list(flatten(elem))
        nueva_lista = []

        for i in range(0,len(flat_list), 2):
            aux = [flat_list[i], flat_list[i+1]]
            nueva_lista.append(aux)

        historico_limpio.append(nueva_lista)
    return historico_limpio



def sacar_coord(lista):
    '''
    Creates a list with specific values from a source list
    Args:
        list(): The list with the required values
    Return:
        list(): A list with only values required
    '''  
    lista_peticiones = []
    
    for elem in lista:
        lat_lng = [elem['latitud'], elem['longitud']]
        lista_peticiones.append(lat_lng)
    
    return lista_peticiones



def sacar_media_historico(historico):
    '''
    Creates a list with coordinates' means
    Args:
        list(): The coordinates' list
    Return:
        list(): A list with the means
    '''
    lista_medias = list()
    for fila in historico:
        aux1 = 0
        aux2 = 0
        lista_fila = []
        divisor = len(fila)
        for elem in fila:
            aux1 += elem[0]
            aux2 += elem[1]
        #lista_fila.append([(aux1/divisor), (aux2/divisor)])
        #lista_medias.append(lista_fila)
        lista_medias.append([(aux1/divisor), (aux2/divisor)])

    return lista_medias



def hacer_consulta(coleccion, medias_historico, radio):
    '''
    Makes queries to Mongo collections
    Args:
        string: The collection's name
        list(): A list that contains the coordinates necessary to make the queries
        int: max distance in queries
    Return:
        list(): A list with the results' coordinates from queries
    '''
    lista_consulta = []
    lista_resultados = []
    
    colec = db.get_collection('bares_madrid')
    #colec.create_index([("geometry", GEOSPHERE)])
    for elem in medias_historico:
        media_point = {"type": "Point",  "coordinates": elem}

        consulta = {"location": {"$near": {"$geometry": media_point, "$maxDistance": radio}}}

        resultados = list(colec.find(consulta))

        lista_consulta = sacar_resultados(resultados)
        
        lista_resultados.append(lista_consulta)
    
    return lista_resultados



def sacar_resultados(resultados):
    '''
    Creates a list with the coordinates from a json document
    Args:
        json: The queries' return
    Return:
        list(): A list with the results' coordinates from json document
    '''
    if len(resultados) == 0:
        return []

    respuesta = list()
    
    for elem in resultados:
        #aux = [elem['location']['coordinates'][0], elem['location']['coordinates'][1]]
        #respuesta.append(aux)
        respuesta.append([elem['location']['coordinates'][0], elem['location']['coordinates'][1]])
    
    return respuesta