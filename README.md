# Drobots

# 1. Introducción

CROBOTS es un juego basado en programación de computadores. A diferencia de los juegos tipo arcade que requiere interacción con un
humano para controlar algún objeto, toda la estrategia en CROBOTS está especificada antes del comienzo del juego. La estrategia
del juego está condensada en un programa C que tú diseñas y escribes. Tu programa controla un robot cuya misión es buscar,
perseguir y destruir otros robots, cada uno de ellos bajo el control de programas diferentes en ejecución. Cada robot está
igualmente equipado, y hasta un máximo de cuatro robots pueden competir a la vez. CROBOTS es mejor si lo juegan varias personas,
cada uno perfeccionando su propio programa, y después enfrentando a los programas entre sí. 

En DROBOTS, la arquitectura y la mecánica de la aplicación es muy diferente. El juego está orquestado por un servidor que crea
partidas a la que se conectan los jugadores. Los jugadores aportan controladores de robots y, opcionalmente, controladores de
detectores. Cuando la partida dispone del número de jugadores adecuado, crea robots y detectores para cada jugador y les solicita
los controladores para los mismos. Todos ellos: servidor, jugador, robot y controladores son objetos distribuidos. El detector no
se considera un objeto distribuido, ya que no dispone de ninguna funcionalidad que ofrecer de manera directa, y por tanto no tiene
interfaz. Después, el juego va indicando a cada controlador de robot un turno en el que puede interaccionar con el robot asociado.
En la modalidad más simple cada jugador tiene un único controlador y por tanto un único robot. Salvo por los aspectos de
comunicación entre programas, pasando de una máquina virtual y ejecución centralizada en CROBOTS, a un conjunto de programas que se comunican a través de la red.

En DROBOTS, el juego trata de respetar siempre que sea posible las reglas y funcionamiento del CROBOTS original.

# 2. Ejecución
Para probar la ejecución de este pequeño proyecto, necesitaremos conectar nuestra vpn a la red de la UCLM además de abrir un
terminal donde escribiremos el siguiente comando: make all. Con este comando se ejecutarán todos los programas necesarios para
que la aplicación funcione correctamente. Es importante resaltar, que si la aplicación no funciona, se debe a que el servidor
de la unviersidad(UCLM) ha sido modificado para la realización de otra práctica diferente a ésta.
