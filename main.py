import pygame as pg
import random as rnd
import time


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pg.init()
    width ,columns, rows = 300, 15 ,30
    distance = width // columns
    height = distance*rows
    grid=[0]*columns*rows
    #load hinh
    picture =[]
    for i in range(8):
        picture.append(pg.transform.scale(pg.image.load(f'T_{i}.gif'),(distance,distance)))
        print(pg.image.load(f'T_{i}.gif'),(distance,distance))
    screen =pg.display.set_mode([300,height])

    grid[19]=2
    status=True
    while status:
        for even in pg.event.get():
            if even.type ==pg.QUIT:
                status =False
        screen.fill((128,128,128))
        for n, color in enumerate(grid):
            if color > 0:
                x=n % columns * distance
                y= n // columns * distance
                screen.blit(picture[color],(x,y))
        pg.display.flip()

    pg.quit()ádvhsavdjkbasjkbdh


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
