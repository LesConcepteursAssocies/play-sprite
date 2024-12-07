#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
# Play-sprite
#
# 10/2024 PG (p.guillaumaud@laposte.net)
#
# permet de lire une planche de sprites, pour un rendu vite fait
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA
#
# exemple d'utilisation:
# python play-sprite.py -f'\src\assets\robots-sprites\Destroyer\Attack_1.png'
#
import sys, os
try:
    import pyray as rl
except ImportError as err:
    print("ImportError: {0}, did you install raylib? https://www.raylib.com".format(err))
    sys.exit(2)

# --------------------------------------------------------------------------------
# classe vide
class emptyClass:
    pass

SCREEN_WIDTH    = 1600
SCREEN_HEIGHT   = 800

FPS             = 60
MAX_FRAME_SPEED = 30
MIN_FRAME_SPEED = 1

TITRE           = "play-sprite"
DESC            = "a simple player for sprite-sheets"
FOOTER          = TITRE+" (by philippe Guillaumaud) "


# la feuille de sprites
spriteSheet       = emptyClass()
# le fichier
spriteSheet.sFile = ""
# taille par défaut d'un sprite dans la feuille
spriteSheet.sWidth, spriteSheet.sHeight = (64, 64)
spriteSheet.currentFrame  = 0
spriteSheet.framesCounter = 0
spriteSheet.maxFrames     = 0
spriteSheet.maxLines      = 0
spriteSheet.currentLine   = 0
spriteSheet.framesSpeed   = 8
# True si la feuille est plus large que l'écran
spriteSheet.doScroll      = False
# la taille de la vignette
spriteSheet.thumbX        = 260
spriteSheet.thumbY        = 260

fontSize  = 10
marginX   = 20
marginY   = 20

gamePause = False

# todo:
#       - dialogBox de sélection d'un fichier dans le programme avec navigation dans les répertoires
#       - lire une feuille de sprites en colonne?

# --------------------------------------------------------------------------------
if __name__ == '__main__':
    import argparse

    # les arguments éventuels
    # -----------------------
    parser = argparse.ArgumentParser(prog=TITRE, description=DESC, usage='%(prog)s -f\'<fichier>\' [options]', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", required=True, dest="sFile", action="store", help='sprite-sheet to load')
    parser.add_argument('-W', required=False, type=int, action='store', help='sprite width (px)')
    parser.add_argument('-H', required=False, type=int, action='store', help='sprite height (px)')
    parser.add_argument('-L', required=False, type=int, action='store', help='number of lines')
    parser.add_argument('-C', required=False, type=int, action='store', help='number of sprites/line')
    args = parser.parse_args()

    spriteSheet.sFile = args.sFile

    rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, TITRE)

    spriteSheet.sheet = rl.load_texture(spriteSheet.sFile)

    if args.W is not None:
        spriteSheet.sWidth = args.W

    if args.H is not None:
        spriteSheet.sHeight = args.H

    # nombre de sprites/ligne
    if args.C is not None:
        spriteSheet.maxFrames = args.C
        spriteSheet.sWidth    = spriteSheet.sheet.width // spriteSheet.maxFrames
    else:
        spriteSheet.maxFrames = spriteSheet.sheet.width // spriteSheet.sWidth

    # plusieurs lignes dans la feuille?
    if args.L is not None:
        spriteSheet.maxLines = args.L
        spriteSheet.sHeight  = spriteSheet.sheet.height // spriteSheet.maxLines
    else:
        spriteSheet.maxLines  = spriteSheet.sheet.height // spriteSheet.sHeight

    # le sprite courant
    spriteSheet.recSource = rl.Rectangle(0.0, 0.0, float(spriteSheet.sWidth), float(spriteSheet.sHeight))
    # la ligne courante dans la feuille
    spriteSheet.recLine   = rl.Rectangle(0.0, 0.0, float(spriteSheet.sheet.width), float(spriteSheet.sHeight))
    # pour la vignette
    spriteSheet.tscale    = min(float(SCREEN_WIDTH/spriteSheet.thumbX), float(SCREEN_HEIGHT/spriteSheet.thumbY))
    spriteSheet.twidth    = spriteSheet.sheet.width
    spriteSheet.theight   = spriteSheet.sheet.height
    if(spriteSheet.twidth>=(SCREEN_WIDTH-(marginX*2))):
        spriteSheet.twidth  = int(spriteSheet.thumbX*spriteSheet.tscale)
    if(spriteSheet.theight>=spriteSheet.thumbY):
        spriteSheet.theight = spriteSheet.thumbY

    # feuille plus large?
    spriteSheet.doScroll  = False
    if(spriteSheet.sheet.width>=SCREEN_WIDTH):
        spriteSheet.doScroll = True

    rl.set_target_fps(FPS)

    while not rl.window_should_close():
        # -----------------------
        # Update
        dt = rl.get_frame_time()

        if(rl.is_key_down(rl.KEY_SPACE)): gamePause = not gamePause

        if(gamePause):
            rl.draw_text("PAUSED", (SCREEN_WIDTH//2), (SCREEN_HEIGHT//2), 30, rl.GRAY)
        else:
            if(spriteSheet.doScroll):
                spriteSheet.framesCounter += 1
                if(spriteSheet.framesCounter >= (FPS/spriteSheet.framesSpeed)):
                    spriteSheet.framesCounter   = 0
                    spriteSheet.currentFrame   += 1
                    if(spriteSheet.currentFrame > (spriteSheet.maxFrames-1)):
                        spriteSheet.currentFrame  = 0
                    # plusieurs lignes?
                    spriteSheet.currentLine   += 1
                    if(spriteSheet.currentLine > (spriteSheet.maxLines-1)):
                        spriteSheet.currentLine  = 0
                    spriteSheet.recSource.x = float(spriteSheet.currentFrame)*float(spriteSheet.sWidth)
                    spriteSheet.recSource.y = float(spriteSheet.currentLine)*float(spriteSheet.sHeight)
                # scrolling horizontal de la ligne courante vers la gauche, de la largeur d'un sprite
                spriteSheet.recLine.x += (spriteSheet.sWidth * dt)
                if(spriteSheet.recLine.x >= spriteSheet.sheet.width):
                    spriteSheet.recLine.x = 0
            else:
                spriteSheet.framesCounter += 1
                if(spriteSheet.framesCounter >= (FPS/spriteSheet.framesSpeed)):
                    spriteSheet.framesCounter   = 0
                    spriteSheet.currentFrame   += 1
                    if(spriteSheet.currentFrame > (spriteSheet.maxFrames-1)):
                        spriteSheet.currentFrame  = 0
                        # plusieurs lignes?
                        spriteSheet.currentLine   += 1
                        if(spriteSheet.currentLine > (spriteSheet.maxLines-1)):
                            spriteSheet.currentLine  = 0
                    spriteSheet.recSource.x = float(spriteSheet.currentFrame)*float(spriteSheet.sWidth)
                    spriteSheet.recSource.y = float(spriteSheet.currentLine)*float(spriteSheet.sHeight)
                    # la ligne courante dans la feuille
                    spriteSheet.recLine = rl.Rectangle(0.0, float(spriteSheet.currentLine)*float(spriteSheet.sHeight), float(spriteSheet.sheet.width), float(spriteSheet.sHeight))

            # Control frames speed
            if(rl.is_key_pressed(rl.KEY_RIGHT)): spriteSheet.framesSpeed += 1
            elif(rl.is_key_pressed(rl.KEY_LEFT)): spriteSheet.framesSpeed -= 1

            if(spriteSheet.framesSpeed > MAX_FRAME_SPEED): spriteSheet.framesSpeed = MAX_FRAME_SPEED
            elif(spriteSheet.framesSpeed < MIN_FRAME_SPEED): spriteSheet.framesSpeed = MIN_FRAME_SPEED

            # -----------------------
            # Draw
            rl.begin_drawing()
            rl.clear_background(rl.BLACK)

            # on commence en haute à gauche
            position = rl.Vector2(marginX, marginY)
            # la ligne courant dans la planche de sprites
            txt      = "Line: {0:<3d}".format(spriteSheet.currentLine)
            rl.draw_text(txt, int(position.x), int(position.y+spriteSheet.recLine.height-fontSize), fontSize, rl.WHITE)
            position.x += (fontSize*6)
            rl.draw_texture_pro(
                spriteSheet.sheet,
                spriteSheet.recLine,
                rl.Rectangle(position.x, position.y, spriteSheet.recLine.width, spriteSheet.recLine.height),
                rl.Vector2(0,0), 0, rl.WHITE
            )

            # le défilement des frames dans la ligne courante
            rl.draw_rectangle_lines(int(position.x-1), int(position.y-1), int(spriteSheet.recLine.width+2), int(spriteSheet.recLine.height+2), rl.GREEN)
            if(not spriteSheet.doScroll):
                rl.draw_rectangle_lines(int(position.x)+int(spriteSheet.recSource.x), int(position.y), int(spriteSheet.recSource.width), int(spriteSheet.recSource.height), rl.RED)
            else:
                rl.draw_rectangle_lines(int(position.x), int(position.y), int(spriteSheet.recSource.width), int(spriteSheet.recSource.height), rl.RED)

            # la gauge des FPS
            position.x  = marginX
            txt         = "{0:<2.0f} FPS".format(spriteSheet.framesSpeed)
            position.y += spriteSheet.recLine.height+(fontSize*2)
            rl.draw_text(txt, int(position.x), int(position.y+fontSize), fontSize, rl.WHITE)
            position.x += (fontSize*6)
            i = 0
            while(i<MAX_FRAME_SPEED):
                if(i < spriteSheet.framesSpeed): rl.draw_rectangle(int(position.x + 21*i), int(position.y), 20, 20, rl.RED)
                i += 1
            position.y += fontSize*3
            rl.draw_text("Press RIGHT/LEFT keys to change SPEED", int(position.x), int(position.y), fontSize, rl.GRAY)

            # le sprite en action
            position.x  = marginX+(fontSize*6)
            position.y += fontSize*5
            rl.draw_texture_pro(
                spriteSheet.sheet,
                spriteSheet.recSource,
                rl.Rectangle(position.x, position.y, spriteSheet.recSource.width, spriteSheet.recSource.height),
                rl.Vector2(0,0), 0, rl.WHITE
            )
            # la bbox
            rl.draw_rectangle_lines_ex(rl.Rectangle(int(position.x-1), int(position.y-1), int(spriteSheet.recSource.width+2), int(spriteSheet.recSource.height+2)), 1.0, rl.BLUE)

            # on affiche les versions plus petites, jusqu'au 32x32 mini
            oldY      = position.y
            newWidth  = spriteSheet.sWidth-16
            newHeight = spriteSheet.sHeight-16
            while(newWidth>=32):
                position.x += (newWidth+(marginX*2))
                position.y += 16
                rl.draw_texture_pro(
                    spriteSheet.sheet,
                    spriteSheet.recSource,
                    rl.Rectangle(position.x, position.y, newWidth, newHeight),
                    rl.Vector2(0,0), 0, rl.WHITE
                )
                # la bbox
                rl.draw_rectangle_lines_ex(rl.Rectangle(int(position.x-1), int(position.y-1), int(newWidth+2), int(newHeight+2)), 1.0, rl.BLUE)
                txt        = "{0:d} x {1:d}".format(newWidth,newHeight)
                rl.draw_text(txt, int(position.x), int(oldY+spriteSheet.recSource.height+(fontSize*2)), fontSize, rl.GRAY)
                newWidth  -= 16
                newHeight -= 16
            position.y = oldY

            # quelques infos
            # taille du sprite
            position.x  = marginX
            position.y += spriteSheet.recSource.height+fontSize
            txt         = "Size"
            rl.draw_text(txt, int(position.x), int(position.y+fontSize), fontSize, rl.WHITE)
            position.x += (fontSize*6)
            txt         = "{0:d} x {1:d}".format(spriteSheet.sWidth,spriteSheet.sHeight)
            rl.draw_text(txt, int(position.x), int(position.y+fontSize), fontSize, rl.GRAY)
            position.y += fontSize*2

            # le fichier
            position.x  = marginX
            txt         = "File"
            rl.draw_text(txt, int(position.x), int(position.y+fontSize), fontSize, rl.WHITE)
            position.x += (fontSize*6)
            txt         = "\'{0}\'  ({1:d}x{2:d})".format(spriteSheet.sFile,spriteSheet.sheet.width,spriteSheet.sheet.height)
            rl.draw_text(txt, int(position.x), int(position.y+fontSize), fontSize, rl.GRAY)
            position.y += fontSize*3
            # le nombre de sprites
            txt         = "{0:d} line(s) of {1:d} sprite(s)".format(spriteSheet.maxLines,spriteSheet.maxFrames)
            rl.draw_text(txt, int(position.x), int(position.y+fontSize), fontSize, rl.GRAY)
            position.y += fontSize*3

            # la vignette
            rl.draw_texture_pro(
                spriteSheet.sheet,
                rl.Rectangle(0.0, 0.0, float(spriteSheet.sheet.width), float(spriteSheet.sheet.height)),
                rl.Rectangle(position.x, position.y, spriteSheet.twidth, spriteSheet.theight),
                rl.Vector2(0,0), 0, rl.WHITE
            )
            # la bbox
            rl.draw_rectangle_lines_ex(rl.Rectangle(int(position.x-1), int(position.y-1), int(spriteSheet.twidth+2), int(spriteSheet.theight+2)), 1.0, rl.YELLOW)

            # la signature en bas à droite
            rl.draw_text(FOOTER, SCREEN_WIDTH - rl.measure_text(FOOTER, fontSize), SCREEN_HEIGHT - int(fontSize*1.5), fontSize, rl.DARKGRAY);

            rl.end_drawing()

    # -----------------------
    # libération des ressources
    rl.unload_texture(spriteSheet.sheet)
    rl.close_window()

# eof