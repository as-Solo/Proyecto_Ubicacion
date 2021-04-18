import numpy as np


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
        
        if type(elem[0]) != list:
            aux = [historico[contador], elem]
            respuesta.append(aux)
            
        elif type(elem[0]) == list:
            for lista in elem:
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