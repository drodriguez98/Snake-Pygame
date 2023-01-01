import random, pygame, sys
from pygame.locals import *


FPS = 15

ANCHO = 640
ALTO = 480
TAMAÑO_CELDA = 20

ANCHO_CELDA = int(ANCHO / TAMAÑO_CELDA)
ALTO_CELDA = int(ALTO / TAMAÑO_CELDA)

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
VERDE_OSCURO = (0, 155, 0)
GRIS_OSCURO  = (40, 40, 40)

COLOR_FONDO = NEGRO

ARRIBA = 'up'
ABAJO = 'down'
IZQUIERDA = 'left'
DERECHA = 'right'

CABEZA = 0 

assert ANCHO % TAMAÑO_CELDA == 0, "El ancho de la ventana debe ser un múltiplo del tamaño de la celda."
assert ALTO % TAMAÑO_CELDA == 0, "La altura de la ventana debe ser un múltiplo del tamaño de la celda."


def main():

    global RELOJ, VENTANA, FUENTE

    pygame.init()

    RELOJ = pygame.time.Clock()
    VENTANA = pygame.display.set_mode((ANCHO, ALTO))
    FUENTE = pygame.font.Font('freesansbold.ttf', 18)

    pygame.display.set_caption('Snake!')

    pantalla_inicial()

    while True:

        inicio()
        dibujar_game_over()


def inicio():
    
    x = random.randint(5, ANCHO_CELDA - 6)
    y = random.randint(5, ALTO_CELDA - 6)

    coordenadas = [{'x': x, 'y': y},
                  {'x': x - 1, 'y': y},
                  {'x': x - 2, 'y': y}]

    direccion = DERECHA

    manzana = posicion_aleatoria()

    while True:     

        for evento in pygame.event.get(): 

            if evento.type == QUIT:

                salir()

            if evento.type == KEYDOWN:

                if (evento.key == K_LEFT or evento.key == K_a) and direccion != DERECHA:

                    direccion = IZQUIERDA

                elif (evento.key == K_RIGHT or evento.key == K_d) and direccion != IZQUIERDA:

                    direccion = DERECHA

                elif (evento.key == K_UP or evento.key == K_w) and direccion != ABAJO:

                    direccion = ARRIBA

                elif (evento.key == K_DOWN or evento.key == K_s) and direccion != ARRIBA:

                    direccion = ABAJO

                elif evento.key == K_ESCAPE:

                    salir()

        if coordenadas[CABEZA]['x'] == -1 or coordenadas[CABEZA]['x'] == ANCHO_CELDA or coordenadas[CABEZA]['y'] == -1 or coordenadas[CABEZA]['y'] == ALTO_CELDA:

            return 

        for cuerpo in coordenadas[1:]:

            if cuerpo['x'] == coordenadas[CABEZA]['x'] and cuerpo['y'] == coordenadas[CABEZA]['y']:

                return 

        if coordenadas[CABEZA]['x'] == manzana['x'] and coordenadas[CABEZA]['y'] == manzana['y']:

            manzana = posicion_aleatoria() 

        else:

            del coordenadas[-1]     

        if direccion == ARRIBA:

            nueva_cabeza = {'x': coordenadas[CABEZA]['x'], 'y': coordenadas[CABEZA]['y'] - 1}

        elif direccion == ABAJO:

            nueva_cabeza = {'x': coordenadas[CABEZA]['x'], 'y': coordenadas[CABEZA]['y'] + 1}

        elif direccion == IZQUIERDA:

            nueva_cabeza = {'x': coordenadas[CABEZA]['x'] - 1, 'y': coordenadas[CABEZA]['y']}

        elif direccion == DERECHA:

            nueva_cabeza = {'x': coordenadas[CABEZA]['x'] + 1, 'y': coordenadas[CABEZA]['y']}

        coordenadas.insert(0, nueva_cabeza)

        VENTANA.fill(COLOR_FONDO)
        dibujar_cuadricula()
        dibujar_gusano(coordenadas)
        dibujar_manzana(manzana)
        dibujar_puntuacion(len(coordenadas) - 3)

        pygame.display.update()

        RELOJ.tick(FPS)


def dibujar_pulsar_tecla():

    animacion_pulsar_tecla = FUENTE.render('Pulsa cualquier tecla para jugar', True, BLANCO)
    recta_pulsar_tecla = animacion_pulsar_tecla.get_rect()
    recta_pulsar_tecla.topleft = (ANCHO - 300, ALTO - 30)

    VENTANA.blit(animacion_pulsar_tecla, recta_pulsar_tecla)


def teclas_salir():

    if len(pygame.event.get(QUIT)) > 0:

        salir()

    evento_teclas = pygame.event.get(KEYUP)

    if len(evento_teclas) == 0:

        return None

    if evento_teclas[0].key == K_ESCAPE:

        salir()

    return evento_teclas[0].key


def pantalla_inicial():

    fuente_animacion = pygame.font.Font('freesansbold.ttf', 100)
    texto_animacion_1 = fuente_animacion.render('Snake!', True, BLANCO, VERDE_OSCURO)
    texto_animacion_2 = fuente_animacion.render('Snake!', True, VERDE)

    grados_1 = 0
    grados_2 = 0

    while True:

        VENTANA.fill(COLOR_FONDO)

        animacion_1 = pygame.transform.rotate(texto_animacion_1, grados_1)
        recta_animacion_1 = animacion_1.get_rect()
        recta_animacion_1.center = (ANCHO / 2, ALTO / 2)
        VENTANA.blit(animacion_1, recta_animacion_1)

        animacion_2 = pygame.transform.rotate(texto_animacion_2, grados_2)
        recta_animacion_2 = animacion_2.get_rect()
        recta_animacion_2.center = (ANCHO / 2, ALTO / 2)
        VENTANA.blit(animacion_2, recta_animacion_2)

        dibujar_pulsar_tecla()

        if teclas_salir():

            pygame.event.get() 
            return

        pygame.display.update()

        RELOJ.tick(FPS)

        grados_1 += 3  
        grados_2 += 7   


def salir():

    pygame.quit()
    sys.exit()


def posicion_aleatoria():

    return {'x': random.randint(0, ANCHO_CELDA - 1), 'y': random.randint(0, ALTO_CELDA - 1)}


def dibujar_game_over():

    fuente_game_over = pygame.font.Font('freesansbold.ttf', 75)

    animacion_game = fuente_game_over.render('Game', True, BLANCO)
    animacion_over = fuente_game_over.render('Over', True, BLANCO)

    recta_game = animacion_game.get_rect()
    recta_over = animacion_over.get_rect()
    
    recta_game.midtop = (ANCHO / 2, 10 + 140)
    recta_over.midtop = (ANCHO / 2, recta_game.height + 75 + 100)

    VENTANA.blit(animacion_game, recta_game)
    VENTANA.blit(animacion_over, recta_over)

    dibujar_pulsar_tecla()

    pygame.display.update()
    pygame.time.wait(500)

    teclas_salir() 

    while True:

        if teclas_salir():
            pygame.event.get() 
            return


def dibujar_puntuacion(puntuacion):

    animacion_puntuacion = FUENTE.render('Puntuación: %s' % (puntuacion), True, BLANCO)
    recta_puntuacion = animacion_puntuacion.get_rect()
    recta_puntuacion.topleft = (ANCHO - 150, 10)

    VENTANA.blit(animacion_puntuacion, recta_puntuacion)


def dibujar_gusano(coordenadas):

    for coord in coordenadas:

        x = coord['x'] * TAMAÑO_CELDA
        y = coord['y'] * TAMAÑO_CELDA

        recta_segmento = pygame.Rect(x, y, TAMAÑO_CELDA, TAMAÑO_CELDA)
        pygame.draw.rect(VENTANA, VERDE_OSCURO, recta_segmento)

        recta_segmento_interno = pygame.Rect(x + 4, y + 4, TAMAÑO_CELDA - 8, TAMAÑO_CELDA - 8)
        pygame.draw.rect(VENTANA, VERDE, recta_segmento_interno)


def dibujar_manzana(coord):

    x = coord['x'] * TAMAÑO_CELDA
    y = coord['y'] * TAMAÑO_CELDA
    recta_manzana = pygame.Rect(x, y, TAMAÑO_CELDA, TAMAÑO_CELDA)

    pygame.draw.rect(VENTANA, ROJO, recta_manzana)


def dibujar_cuadricula():


    for x in range(0, ANCHO, TAMAÑO_CELDA): 

        pygame.draw.line(VENTANA, GRIS_OSCURO, (x, 0), (x, ALTO))

    for y in range(0, ALTO, TAMAÑO_CELDA): 

        pygame.draw.line(VENTANA, GRIS_OSCURO, (0, y), (ANCHO, y))


if __name__ == '__main__':

    main()