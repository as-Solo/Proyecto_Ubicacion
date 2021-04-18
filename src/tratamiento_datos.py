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