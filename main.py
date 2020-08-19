import pygame, sys
from pygame.locals import *

class Points():

    def draw_point(self,cords,color):
        pygame.draw.circle(DISPLAYSURF,color,(cords[0],cords[1]),3)
   
    def __init__(self,cords=(0,0),checked=False):
        self.cords = cords
        self.checked = checked

    def __repr__(self):
        return(str(self.cords))

pygame.init()

WINDOWWIDTH = 480
WINDOWHEIGHT = 640
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
pygame.display.set_caption('Paper Soccer')

BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

size = 50
boardwidth = 8
boardheight = 10

mouse_x = 0
mouse_y = 0


POINTS_pos = []

DISPLAYSURF.fill(WHITE)

def draw_points():
    cnt = 0
    for i in range(1,boardwidth+2):
        for z in range(1,boardheight+2):
            if cnt%2 == 0:
                pygame.draw.circle(DISPLAYSURF,BLUE,(size*i,size*z),3)    
            else:
                pygame.draw.circle(DISPLAYSURF,BLUE,(size*i,size*z),3)
            x = (size*i,size*z)
            POINTS_pos.append(Points(x))    
            cnt+=1
        cnt -= 1
    pygame.draw.rect(DISPLAYSURF,BLACK,[size,size,boardwidth*size,boardheight*size],1)
    #print(POINTS_pos)



def check_position(mouse_, points_):
    points_cords = points_   
    mouse_cords = mouse_   

    for obj in points_cords:
        #print('Mouse',mouse_cords)
        #print('POINTS',obj.cords)
        

        if mouse_cords in range(obj.cords-5,obj.cords+5):
            print('True')
            obj.checked = True
        else:
            obj.checked = False

        if obj.checked == True:
            obj.draw_point(obj.cords,RED)
        else:
            obj.draw_point(obj.cords,GREEN)

    
        #pygame.draw.circle(DISPLAYSURF,BLUE,(mouse_cords[0],mouse_cords[1]),3)

while True:
    if not POINTS_pos:
        draw_points() 

    check_position((mouse_x,mouse_y),POINTS_pos)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos
        
    pygame.display.update()