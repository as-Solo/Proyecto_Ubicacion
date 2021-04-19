import numpy as np
from pandas.core.common import flatten
import pandas as pd


from pymongo import MongoClient
client = MongoClient("localhost:27017")
client

db = client.get_database("ironhack")

def calcular_coste_value(diccionario):
    
    for k,v in diccionario.items():
        v['coste'] = v['numero'] * v['sueldo']
    
    maximo = 0
    for k, v in diccionario.items():
        if v['coste'] > maximo:
            maximo = v['coste']
            
    for k,v in diccionario.items():
        v['requirement_value'] = round( (v['coste'] * 10) / maximo, 2)



def calc_requirement_value(valor, maximo):

    return round ((valor * 10) / maximo, 2)


def limpiar_offices(lista):
    for empresa in lista:
        for elem in empresa['offices']:
            dato = elem['city']
            elem.clear()
            elem['city'] = dato


def pasar_float(lista):
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

    lista_1m = list()
    for elem in lista:
        try:
            if elem['total_money_raised'] >= 1000000:
                lista_1m.append(elem)
        except:
            pass
    return lista_1m



def limpiar_sector(lista):
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
    lista_ciudades = list()
    for elem in lista:
        for ciudad in elem['offices']:
            lista_ciudades.append(ciudad['city'])
    return lista_ciudades


def pasar_a_euros_cv(elem):
    
    coste_vida_NY = [619, 2000, 2619]
    indice = 0
    return round((elem/100) * coste_vida_NY[indice], 2)
    
    
def pasar_a_euros_a(elem):

    coste_vida_NY = [619, 2000, 2619]
    indice = 1
    return round((elem/100) * coste_vida_NY[indice], 2)


def pasar_a_euros_cva(elem):
    
    coste_vida_NY = [619, 2000, 2619]
    indice = 2
    return round((elem/100) * coste_vida_NY[indice], 2)



def filtrar_empresas_ciudad (lista_empresas, empresas_filtradas):
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
    
    lista_peticiones = []
    
    for elem in lista:
        lat_lng = [elem['latitud'], elem['longitud']]
        lista_peticiones.append(lat_lng)
    
    return lista_peticiones



def sacar_media_historico(historico):
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
    
    if len(resultados) == 0:
        return []

    respuesta = list()
    
    for elem in resultados:
        #aux = [elem['location']['coordinates'][0], elem['location']['coordinates'][1]]
        #respuesta.append(aux)
        respuesta.append([elem['location']['coordinates'][0], elem['location']['coordinates'][1]])
    
    return respuesta