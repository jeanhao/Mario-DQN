import pygame, os
from pygame.locals import *

# ----------------------------------------------------

def loadImage(name, colorkey=None):

    fullname = os.path.join("data", name)

    image = pygame.image.load(fullname)

    image = image.convert()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    return image, image.get_rect()

# ----------------------------------------------------

def collide_edges(a, c):

    l, r, t, b = False, False, False, False

    Rect = pygame.Rect
    left = Rect(a.left, a.top + 1, 1, a.height - 2)
    right = Rect(a.right, a.top + 1, 1, a.height - 2)
    top = Rect(a.left + 1, a.top, a.width - 2, 1)
    bottom = Rect(a.left + 1, a.bottom, a.width - 2, 1)

    if left.colliderect(c):
        l = True
    if right.colliderect(c):
        r = True
    if top.colliderect(c):
        t = True
    if bottom.colliderect(c):
        b = True

    return (t, r, b, l)
