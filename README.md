# TIC TAC TOE

El proyecto consiste en la implementación de un juego “gato”/tic-tac-toe realizado con lógica puramente en Prolog y la implementación de una interfaz en Python.

## Technologies used

El proyecto utiliza Prolog para la lógica del juego y Python para la interfaz.

## How to use

### Dependencies

- ### Windows:

 -> instalar "swi-prolog" y reiniciar el equipo:
    
     https://www.swi-prolog.org/download/stable

- ### Linux:
  
 -> instalar "swi-prolog"...
     
   En distribuciones basadas en Debian/Ubuntu:
   
     sudo apt-get update
   
     sudo apt-get install swi-prolog

   En distribuciones basadas en Red Hat/Fedora:
    
     sudo dnf install swi-prolog
 

- ### Mac:

 -> Instalar SWI-Prolog utilizando Homebrew:

     brew install swi-prolog
   
 ### Start

 Ahora utiliza la IDE de tu preferencia (recomendamos Visual Studio Code, con la extención de Python instalada), para ejecutar el archivo de Python. Estoo debería desplegar una nueva ventana donde se mostrará la interfaz del juego.

- NOTA: Recuerda que el archivo de Python (.py) y el de Prolog (.pl) deben de encontrarse en la misma carpeta de dirección para su correcta comunicación.

*Para empezar el juego desde la terminal escribir el siguiente comando desde el directorio con ambos archivo:*

    python main.py

Adicionalmente, se puede acceder individualmente a cada interface con los siguientes comandos:

 -> Interface 1 contra 1

    python game1vs1.py

 -> Interface 1 contra CPU

    python game1vsPC.py

### Comentarios

Es importante destacar que el archivo *game1vsPC.py* puede no terminar el proceso correctamente. 

OJO: se recomienda cerrar la ventana manualmente.
