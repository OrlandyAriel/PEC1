# listadoLibros
#### Orlandy Ariel Sánchez Acosta

Práctica Scraping - PEC2
UOC
Máster Ciencia de Datos
** Explicación**
El script busca en la página goodreads los libros más leidos de la semana o los libros más recientes según el genero.
Goodreader es una red social donde compartes los libros que lees y de alguna manera llevar un historial de los libros que has leido, tambíen esta te recomienda libros según los libros que haz leido.

En el script hay que pasar 1 parámetro, este parámetro es opcional, si no se pone cogerá el valor por defecto que es 0. Si la opción es 0 entonces buscará los libros más recientes por cada genero, en caso de que sea 1 este buscará los datos de los libros más leidos durante la semana.


Automáticamente se guardará los datos recogidos en un archivo .csv y se localizará en el mismo directorio donde se encuentre el script.

El siguiente enlace, [Science Fiction Books](https://www.goodreads.com/genres/new_releases/science-fiction), muestra un ejemplo de como se muestran los datos de libros recientes por el genero de ciencia ficción en la web.

#### Librerías utilizadas
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [URLLib](https://docs.python.org/3/howto/urllib2.html)
* [Pandas](https://pandas.pydata.org/)
* [re](https://docs.python.org/2/library/re.html)
* [argparse](https://docs.python.org/3/library/argparse.html)

Para lanzar el script:
* Linux:
```python
 python listadoLibros.py --opcion 0 o --pocion 1
```
* Windows:
```python
 python.exe listadoLibros.py --opcion 0 o --pocion 1
```
Spyeder: pulsar el botón de play.