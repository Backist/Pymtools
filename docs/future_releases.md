En este archivo se comentarán las Propuestas de mejora y actualizaces de la librería.

## Propuestas de mejora:
- Manejo de los errores en inglés para que la librería sea accesible para todos los desarolladores.
- Mejora del tiempo de ejecucción de algunas de las funciones de algunos modulos.
- Intentar dar soporte de la librería a otros sistemas operativos (ya que actualmente solo funciona en sistemas POSIX (Windows)).
- Propuesta para averiguar la mejor forma de administrar los errores:
   Por ejemplo:
    - Los errores se muestran con el callback entero para que puedan ser reconocer su procedencia fácilmente en programas largos. (Como si fuera raises)
    - Todos los errores muestran el callback original del interprete de Python.
    - Los errores se mostrará con un logger que muestra el tipo de error y de que funcion proviene.
    - etc...


## Proximas versiones:
    Version actual: ``0.1.1-beta``
    - Proxima version: ``0.1.2-stable``
        - cambios: ...