<a name='inicio'></a>
# LA MEJOR UBICACIÓN PARA MI EMPRESA

### Este proyecto pretende automatizar la búsqueda de la mejor ubicación posible para una recién fundada empresa según las necesidades de los trabajadores.

![portada](attachment:portada_Readme.jpg)

### Table of Contents

1. [Información General](#Información)
2. [Desarrollo del proyecto](#Pasos)
3. [Librerías](#Librerías:)
4. [Tecnología](#Tecnología:)

<a name='Información'></a>
## Información general

La idea básica de este proyecto es poder encontrar una **ubicación** que satisfaga las demandas de todos los miembros de la empresa. La meta es devolver unas coordenadas, o un grupo de coordenadas, en cuyas inmediaciones se encuentren todas las comodidades y recursos que la ciudad ofrece a nuestros empleados.

**La estructura de la empresa es la siguiente:**

- 20 Designers
- 5 UI/UX Engineers
- 10 Frontend Developers
- 15 Data Engineers
- 5 Backend Developers
- 20 Account Managers
- 1 Maintenance guy
- 10 Executives
- 1 CEO/President


**Las peticiones eran estas:**

- Designers like to go to design talks and share knowledge. There must be some nearby companies that also do design.
- 30% of the company staff have at least 1 child.
- Developers like to be near successful tech startups that have raised at least 1 Million dollars.
- Executives like Starbucks A LOT. Ensure there's a starbucks not too far.
- Account managers need to travel a lot.
- Everyone in the company is between 25 and 40, give them some place to go party.
- The CEO is vegan.
- If you want to make the maintenance guy happy, a basketball stadium must be around 10 Km.
- The office dog—"Dobby" needs a hairdresser every month. Ensure there's one not too far away.


<a name='Pasos'></a>
## Desarrollo del proyecto

1. [Priorización de peticiones](#priorización)
1. [Elección de ciudad](#ciudad)
1. [Creación de base de datos](#bbdd)
1. [Filtrado de peticiones](#filtrado)
1. [Creación de csv](#csv)
1. [Visualización oficina](#visualización)

<a name = priorización></a>
### 1. Priorización de peticiones

Lo primero era saber como valoraremos en la empresa las distintas peticiones, para jerarquizarlas y encontrar un orden de búsqueda posteriormente. La decisión que se tomó fue que se valorarían en relación al coste que genereba a la empresa las personas que hacían las peticiones, cuanto más se hubiese invertido en contratar a esas personas, más importancia tendría la petición. Para ello se realizó un diccionario con la estructura antes mencionada pero añadiendo los valores de *sueldo medio* (valor que recogimos de buscar en google el sueldo medio de cada puesto), *coste empresa*, *petición* y *peso de la petición* dado que la gran mayoría de peticiones venían de departamentos concretos.

Se valorarían las peticiones del uno al diez, entendiendo 10 como el coste empresa del departamento más caro. Se calculó el peso de cada petición por departamento y se hizo una tabla de peticiones y su valor, a la que se le añadirían las peticiones no relacionadas directamente con departamentos. Una vez tuvimos las peticiones y su fuerza, se ordenó de mayor a menor peso, ya teníamos un orden de prioridades.

<a name = ciudad></a>
### 2. Elección de ciudad

Tuvimos claro desde el principio que los criterios para la selección de ciudad tenían que ser aquellos elementos de la lista de prioridades que fuesen más anómalos. Cafeterías, aeropuertos, y peluquerías caninas íbamos a encontrar en todas las ciudades medianamente grandes donde buscásemos, pero empresas tecnológicas con áreas de diseño y que tuviesen unas ganancias superiores a un millón de dólares iba a ser más complicado.

Para ello, tuvimos la suerte de contar con la colección ['companies'](../data/companies.json) que nos permitió filtrar en Mongo DB. Tras algunas modificaciones con las [funciones de tratamiento de datos](../src/tratamiento_datos.py) conseguimos una lista de todas las ciudades que cumplían con la espectativa de tener una empresa tecnológica con área de diseño y más de un millón de dólares de ganancia. Lista que fue para nuestra sorpresa especialmente extensa.

Como seguiamos teniendo una lista con 745 posibles ciudades decidimos filtrar aún más, así que nos scrapeamos de [esta página](https://es.numbeo.com/coste-de-vida/clasificaciones-actuales) una tabla con el coste de vida de las principales ciudades del mundo. Sabíamos que la tabla usaba como referencia la ciudad de NY, así que buscamos [aquí](https://vivirenn.com/cuanto-cuesta-vivir-nueva-york/) el coste en dolares de la vida en NY y pasamos a dólares los índices porcentuales de la tabla scrapeda. Seleccionamos de esta tabla todas las ciudades cuyo coste anual no fuese inaccesible para nuestros trabajadores teniendo en cuenta el sueldo que les pagamos. Cruzamos la tabla de ciudades obtenidas mediante la colección 'companies' y la de ciudades viables que acababamos de obtener y conseguimos una nueva lista con 122 posibles ciudades.

Decidimos seguir discriminando y lo que se nos ocurrió fue valorar la calidad de vida de esas 122 ciudades. Scrapeamos una tabla con las ciudades con mayor calidad de vida del mundo en este [enlace](https://es.wikipedia.org/wiki/Anexo:Ciudades_por_calidad_de_vida) y volvimos a cruzar resultados. Esta vez teníamos una lista con 18 resultados y 3 de ellos se encontraban en la Península Ibérica: Madrid, Barcelona o Lisboa. La decisión fue Madrid.

<a name = ciudad></a>
### 3. Creación de base de datos

Una vez seleccionada la ciudad decidimos hacernos distintas colecciones de los requisitos exigidos. Para ello usamos la [API](https://developer.foursquare.com/docs/api-reference/venues/search/) de Four Square que nos devolvía la localización en coordenadas de las distintas peticiones que le hiciesemos atendiendo a que estuviesen en Madrid. Así pudimos hacernos con una base de datos de todos los sitios de interés de nuestra lista.
'''
- Colegios.
- Bares y centros de ocio.
- Starbucks.
- Estaciones de tren, intercambiadores de autobuses y aeropuertos.
- Peluquerías caninas y veterinarios
'''

<a name = filtrado></a>
### 4. Filtrado de peticiones

Con la ciudad decidida, una base de datos creada con todas los sitios de interés que pudimos recabar de la API, decidimos crear una función que hiciese una geoquery a nuestra base de datos y almacenase las distintas combinaciones de coordenadas con resultados positivos y descartase el resto, además nos devolvía una lista de coordenadas medias, que triangulaban la posición y servían para realizar la siguiente query con el siguiente requisito. Una vez hechas las queries de todas las peticiones de la lista teníamos una lista con todas las coordenadas que había en Madrid que cumplían con todos los requisitos propuestos.

<a name = csv></a>
### 5. Creación de csv

Para poder hacer una visualización de los alrededores de nuestra 'nueva oficina' creamos un documento json mediante la [API](https://developer.foursquare.com/docs/api-reference/venues/search/) de Four Square, pidiéndole que nos devolviese todas las coincidencias de nuestra lista de prioridades desde las coordenadas de nuestra oficina a 500 m a la redonda. Con ese documento hicimos un DataFrame y ese DataFrame lo exportamos a [csv](../data/visualizacion.csv)

<a name = visualización></a>
### 6. Visualización oficina

Mediante la tecnología de código abierto [Kepler.gl](https://kepler.gl/) usamos nuestro [csv](../data/visualizacion.csv) para cargar los datos y configuramos nuestro mapa para que representase cada tipo de petición en un color distinto representado con barras hexagonales. El resultado fue el [siguiente](../data/alrededores_oficina).

## Librerías:

***
Para este proyecto se han usado estas librerías y módulos. 
```
import sys
from itertools import zip_longest
import pandas as pd
import numpy as np
import src.scrapping as sc
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo import GEOSPHERE
import json
from dotenv import load_dotenv
import os
from functools import reduce
import operator
import geopandas as gpd
from keplergl import KeplerGl
```
***

## Tecnología: 

Distinto programas y utilidades usados en este proyecto:
* [Jupyter Notebook](https://jupyter.org/)
* [Python](https://www.python.org/): Version 3.8
* [Visual Studio Code](https://code.visualstudio.com/)
* [plotly](https://plotly.com/graphing-libraries/)
* [BeautifulSoap](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [MongoDBCompass](https://docs.mongodb.com/compass/master/)
* [API Four Square](https://developer.foursquare.com/docs/api-reference/venues/search/)
* [Kepler.gl](https://kepler.gl/)

## Autor:

* [Alejandro S. del Solo](https://github.com/as-Solo)

## Agradecimientos:

A mi profes (porque si no fuese por ellos no sabría ni abrir un Jupyter):
* [Amanda Corell](https://github.com/agalvezcorell)
* [Manuel Lopez Sheriff](https://github.com/sheriffff)

A mis ángeles de la guarda, aunque en Ironhack los llamen TA (por estar siempre ahí, por hacer más de lo que su trabajo les obliga, por cuidarnos, ayudarnos y entendernos a cada uno de manera distinta, pero a todos igual de bien. Por ayudarme a superarme desde hace un **mes**, aunque parece un año):
* [Ana García](https://github.com/AnaAGG)
* [Fernando Costa](https://github.com/breogann)

Y a mis compañeros de clase por aguantar mis preguntas tontas, mis preguntas pesadas, mis caras raras en el zoom, mis pintas de 'me acabo de despertar', por todo el apoyo, consejo, ayuda y risas.

***
```
ADVERTENCIA:
Imaginaos el discurso si gano un Oscar 😱😱😱
```
(Pero es que en una [guía muy molona](https://gist.github.com/Villanuevand/6386899f70346d4580c723232524d35a) ponía que fuesemos agradecidos)

[volver arriba](#inicio)
