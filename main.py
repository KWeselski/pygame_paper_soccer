import pygame, sys
from pygame.locals import *
import threading
import time
class Points():

    def draw_point(self,cords,color):
        point = pygame.draw.circle(DISPLAYSURF,color,(cords[0],cords[1]),5)

    def __init__(self,cords=(0,0),checked=False,point_pos=pygame.Rect,pointradius=pygame.Rect):
        self.cords = cords
        self.checked = checked
        self.point_pos = point_pos
        self.point_radius = pointradius

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

starting_position = (250,300)
size = 50
boardwidth = 8
boardheight = 10
global isClicked
mouse_x = 0
mouse_y = 0
global current_point_cord

POINTS_pos = []
LINES = []


DISPLAYSURF.fill(WHITE)

def draw_points():
    cnt = 0
    for i in range(1,boardwidth+2):
        for z in range(1,boardheight+2):
            if cnt%2 == 0:
                point_p=pygame.draw.circle(DISPLAYSURF,GREEN,(size*i,size*z),5)  
                point_radius = pygame.draw.circle(DISPLAYSURF,WHITE,(size*i,size*z),15)  
            else:
                point_p =pygame.draw.circle(DISPLAYSURF,GREEN,(size*i,size*z),5)
                point_radius = pygame.draw.circle(DISPLAYSURF,WHITE,(size*i,size*z),15)
            x = (size*i,size*z)
            
            POINTS_pos.append(Points(cords=x,point_pos=point_p,pointradius=point_radius))    
            cnt+=1
        cnt -= 1
    pygame.draw.rect(DISPLAYSURF,BLACK,[size,size,boardwidth*size,boardheight*size],1)
    

def check_position(mouse_, points_):
    points_cords = points_   
    mouse_cords = mouse_   

    for obj in points_cords:
        
        if obj.point_radius.collidepoint(mouse_cords):
            obj.checked = True
        else:
            obj.checked = False

        if obj.checked == True:
            obj.draw_point(obj.cords,RED)  
            current_point_cord=obj.point_pos   
            return current_point_cord
        else:
            obj.draw_point(obj.cords,GREEN)

def find_near_points(point_p):

    point = point_p
    cords = (point.centerx,point.centery)
    near_points = [(cords[0]-size,cords[1]+size),(cords[0],cords[1]+size),(cords[0]+size,cords[1]+size),
                    (cords[0]-size,cords[1]),(cords[0]+size,cords[1]),
                    (cords[0]-size,cords[1]-size),(cords[0],cords[1]-size),(cords[0]+size,cords[1]-size)]
    near_n = []
    for n in near_points:
        for obj in POINTS_pos:
            cords_near = (obj.point_pos.centerx, obj.point_pos.centery)
         
            if n == cords_near:
                near_n.append(obj) 

    draw_neighbours(near_n)
    x = find_another_point(cords,near_n)
    return x

    

def draw_neighbours(neigh): 
        for obj in neigh:
            obj.draw_point((obj.point_pos.centerx, obj.point_pos.centery),BLACK)

def find_another_point(point,neigh):
    mouse_cords = (mouse_x,mouse_y)

    for obj in neigh:
        if obj.point_radius.collidepoint(mouse_cords):
            obj.checked = True
        else:
            obj.checked = False
        if obj.checked == True:
                    
            line = pygame.draw.line(DISPLAYSURF,WHITE,point,(obj.point_pos.centerx,obj.point_pos.centery),3)
            if line in LINES:
                print('Ta lini juz istnieje')
                line = pygame.draw.line(DISPLAYSURF,BLACK,point,(obj.point_pos.centerx,obj.point_pos.centery),3)
                return
            else:
                line = pygame.draw.line(DISPLAYSURF,BLACK,point,(obj.point_pos.centerx,obj.point_pos.centery),3)
                LINES.append(line)
            isClicked = False
            return isClicked  
        else:
            obj.draw_point(obj.cords,BLACK)
            

def print_points():
    print(POINTS_pos)


while True:
    if not POINTS_pos:
        draw_points()
        current_point_cord = check_position((mouse_x,mouse_y),POINTS_pos)         
        current_point_cord = check_position(starting_position,POINTS_pos)  
        find_near_points(current_point_cord)
        
        #time.sleep(3)         
        isClicked=True


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            if isClicked==False:
                mouse_x, mouse_y = event.pos 
                current_point_cord = check_position((mouse_x,mouse_y),POINTS_pos) 
            else:
                mouse_x, mouse_y = event.pos
                      
        elif event.type == MOUSEBUTTONUP:
            isClicked=True    
            done = find_near_points(current_point_cord)
            isClicked=done

        elif event.type == MOUSEWHEEL:
            isClicked=False
        
    pygame.display.update()