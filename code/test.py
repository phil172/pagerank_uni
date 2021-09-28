import pygame, time
from pygame.locals import *

pygame.init()



while True:
    print( "doing a function")
    for event in pygame.event.get():
      if (event.type == KEYUP) or (event.type == KEYDOWN):
         print( "key pressed")
         time.sleep(0.1)