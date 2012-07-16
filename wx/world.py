#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  world.py
#
#  Copyright 2012 Developingo <a.wonderful.code@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

"""
Pruebas de la interfaz gráfica de python usando pygame
"""

import pygame, sys
import time

carpetas = ['default', 'challenger', 'monos', 'flechas']

if __name__ == "__main__":
    pygame.init()

    pantalla = pygame.display.set_mode((400,400), 0, 32)
    pantalla.fill((255,255,255))
    pygame.display.set_caption("Karel el robot")

    bkarel = pygame.image.load(carpetas[0]+'/bkarel.png')
    knorte = pygame.image.load(carpetas[0]+'/knorte.png')

    for i in xrange(20):
        for j in xrange(20):
            pantalla.blit(bkarel, (i*20,j*20))
    pantalla.blit(knorte, (0, 380))

    pygame.display.update() #Sin esta linea el juego no funciona

    vertical = 0
    horizontal = 0
    while True: #Este es el bucle principal
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print "Flecha arriba!"
                if event.key == pygame.K_DOWN:
                    print "Flecha abajo!"
                if event.key == pygame.K_LEFT:
                    print "Flecha izquierda!"
                if event.key == pygame.K_RIGHT:
                    print "Flecha derecha!"
            if event.type == pygame.KEYUP:
                pass

        pygame.display.update()

        time.sleep(0.02)

