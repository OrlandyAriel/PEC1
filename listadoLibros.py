# -*- coding: utf-8 -*-
"""
@author: Orlandy Ariel Sánchez Acosta
"""
# LIBRERIAS
import urllib.request as request
import bs4 as bs
import pandas as pd
import re
import argparse

class ListadoLibros:
    '''
    Esta clase construye y realiza una petición a goodreads
    '''
    def __init__(self, opcion = "0"):
        if(opcion == "1"):
            self.opcion = opcion
        else:
            self.opcion = "0"
        self.nombreArchivo = ""
        self.dLibros = {}
        self.urlBase = 'https://www.goodreads.com/genres/'
        self.urlNuevosLanzamientos = "new_releases/"
        self.urlMasLeidosSemana = "most_read/"
        self.generos = ["historical-fiction", "cience","astronomy","business", 
                   "science-fiction","dystopia","mystery","detective", "horror"
                   ,"graphic-novels", "biography", "crime","adventure","childrens",
                   "paranormal", "self-help"]
        self._patronAvg = re.compile('\d\.\d{2}.avg.rating')
        self._patronCalifiados = re.compile('((\d{0,3}\,)+\d{1,3}|\d{1,3}).ratings')
        self._patronPublicado = re.compile('published.\d{4}')
    
    def extraerDatos(self, url, genero, dicLibros):
        '''
        Este método extrae los datos de la los libros de la página.
        @param url: primera parte de la url
        @param genero: completa la url
        @param dicLibros: diccionario donde se almacenan los datos de los libros desglozados.
        @return: diccionario actualizado con los nuevos libros
        '''
        page = request.urlopen(url+genero, timeout = 20)
    
        soup = bs.BeautifulSoup(page, 'html.parser')
       
        divLibros = soup.findAll("div", class_=  "leftAlignedImage bookBox")
        indexDic = len(dicLibros)
        nuevoSoupScript = None
        bandera = False
        inicio = 76 # posición en la que inicia la parte que interesa guardar del script incrustado en la página
        fin = None
        for i, cdata in enumerate(divLibros):
            dicDatosLibro = {}
            if(i == 0):
                script  = cdata.findAll('script', text = True)[1]
            if(i > 0 ):
                script  = cdata.script.find(text = True)
            scriptFormateado = ''.join(script)
            scriptFormateado = scriptFormateado.replace('\\', '')
            for index, caracter in enumerate(scriptFormateado): 
                if(caracter == "{" and bandera == False):
                    bandera = True
                    fin = index
            scriptFormateado = scriptFormateado[inicio:fin]
            bandera = False
            nuevoSoupScript = bs.BeautifulSoup(scriptFormateado, "html.parser")
            dicDatosLibro["Autor"] = nuevoSoupScript.find('a', class_="authorName").text
            dicDatosLibro["Portada"] = cdata.img['src']
            dicDatosLibro["Nombre del Libro"] = nuevoSoupScript.find('a',class_="readable bookTitle").text
            estadisticas = nuevoSoupScript.findAll('div')[1].text[3:len(nuevoSoupScript.findAll('div')[1].text)]
            dicDatosLibro["Valoración media"] = self.getDato(estadisticas, self._patronAvg)
            dicDatosLibro["Calificados"] = self.getDato(estadisticas, self._patronCalifiados)
            dicDatosLibro["Publicado"] = self.getDato(estadisticas, self._patronPublicado)
            try:
                dicDatosLibro["Descripción"] =  nuevoSoupScript.findAll('div')[2].text[8:(len(nuevoSoupScript.findAll('div')[2].text)-16)]
            except IndexError:
                dicDatosLibro["Descripción"] = "Sin descripción."
            dicDatosLibro["Genero"] = genero
            dicLibros[indexDic] = dicDatosLibro
            indexDic += 1
        return dicLibros
    
    def getDato(self, estadisticasCompletas, patron):
        '''
        Método que partiendo de una cadena, obtiene los datos especificos según el parámetro patron, este será una 
        expresión regular.
        '''
        resultado = re.compile(patron)
        resultado.search(estadisticasCompletas)
        try:
            return resultado.search(estadisticasCompletas).group(0)
        except AttributeError:
            return "--"
        
    def ejecutar(self):
        for genero in self.generos:
            if(self.opcion == "1"):
                url = self.urlBase + self.urlMasLeidosSemana
                self.nombreArchivo = "ListadoLibrosMasLeidosEnLaSemana.csv"
            else:
                url = self.urlBase + self.urlNuevosLanzamientos
                self.nombreArchivo = "ListadoLibrosNuevosLanzamientos.csv"
                
                
            self.dLibros = self.extraerDatos(url, genero, self.dLibros)
    
    def imprimirCSV(self):
        self.ejecutar()
        print(len(self.dLibros))
        pf = pd.DataFrame.from_dict(data = self.dLibros, orient = 'index')
        pf.to_csv(self.nombreArchivo, header = True, index = False)
                    
if __name__ == "__main__":
    #parámetro opción
    parser = argparse.ArgumentParser()
    parser.add_argument("--opcion", help="opción = 0: Listado de nuevos lanzamientos, opción = 1:Listado de los libros más leidos en la semana")
    args = parser.parse_args()
    if(args.opcion != None):
        ListadoLibros(args.opcion).imprimirCSV()
    else:
         ListadoLibros().imprimirCSV()
    
