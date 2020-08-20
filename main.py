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



size = 50
boardwidth = 8
boardheight = 11

mouse_x = 0
mouse_y = 0

global current_point
global isClicked
global BALL
global first_move


POINTS_pos = []
LINES = []


DISPLAYSURF.fill(WHITE)

point_for_skip = [(1,1),(1,2),(1,3),(1,7),(1,8),(1,9),
                (boardheight+1,1),(boardheight+1,2),(boardheight+1,3),
                (boardheight+1,7),(boardheight+1,8),(boardheight+1,9)]


def draw_court(Points_list):
    left_side_idx = [x for x in range(0,10)]
    right_side_idx = [y for y in range(86,96)]
    down_side_idx = [9,19,29,40,41,53,65,64,75,85,95]
    up_side_idx = [0,10,20,31,30,42,54,55,66,76,86]
    draw_line_in_court(left_side_idx)
    draw_line_in_court(right_side_idx)
    draw_line_unsorted_in_court(up_side_idx)
    draw_line_unsorted_in_court(down_side_idx)
    
def draw_line_unsorted_in_court(list_):
    points_in = []
    for x in list_:
        for idx,point in enumerate(POINTS_pos):
            if x == idx:
                points_in.append(point)
        for x in range(0,len(points_in)-1):
            start = (points_in[x].point_pos.centerx,points_in[x].point_pos.centery)
            end = (points_in[x+1].point_pos.centerx,points_in[x+1].point_pos.centery)
            line = (start,end)
            pygame.draw.line(DISPLAYSURF,BLACK,line[0],line[1],3)
            LINES.append(line)

def draw_line_in_court(list_):
    points_in = []
    for idx,point in enumerate(POINTS_pos):
        if idx in list_:
            points_in.append(point)
        for x in range(0,len(points_in)-1):
            start = (points_in[x].point_pos.centerx,points_in[x].point_pos.centery)
            end = (points_in[x+1].point_pos.centerx,points_in[x+1].point_pos.centery)
            line = (start,end)
            pygame.draw.line(DISPLAYSURF,BLACK,line[0],line[1],3)
            LINES.append(line)

def draw_points():
    cnt = 0
    for i in range(1,boardwidth+2):
        for z in range(1,boardheight+2):
            if (z,i) in point_for_skip:
                continue
            if cnt%2 == 0:
                point_radius = pygame.draw.circle(DISPLAYSURF,WHITE,(size*i,size*z),15) 
                point_p=pygame.draw.circle(DISPLAYSURF,GREEN,(size*i,size*z),5)  
                 
            else:
                point_radius = pygame.draw.circle(DISPLAYSURF,WHITE,(size*i,size*z),15)
                point_p =pygame.draw.circle(DISPLAYSURF,GREEN,(size*i,size*z),5)         
            x = (size*i,size*z)
            
            POINTS_pos.append(Points(cords=x,point_pos=point_p,pointradius=point_radius))    
            cnt+=1
        cnt -= 1
    pygame.draw.rect(DISPLAYSURF,BLACK,[size,size,boardwidth*size,boardheight*size],1)
    

def clear_display(points_):
    for obj in points_:
        obj.draw_point(obj.cords,GREEN)

def check_position(ball_, points_):
    points_cords = points_   
    ball_cords = ball_   
    for obj in points_cords:
        if(obj.cords == ball_cords):
            current_point_cord=obj.point_pos   
            return current_point_cord 

def check_index():
    mouse_cords = (mouse_x,mouse_y)  
    for idx,obj in enumerate(POINTS_pos):
        if obj.point_radius.collidepoint(mouse_cords):
            print(idx)

def find_near_points(point_p):
    cords = (point_p.centerx,point_p.centery)
    near_points = [(cords[0]-size,cords[1]+size),(cords[0],cords[1]+size),(cords[0]+size,cords[1]+size),
                    (cords[0]-size,cords[1]),(cords[0]+size,cords[1]),
                    (cords[0]-size,cords[1]-size),(cords[0],cords[1]-size),(cords[0]+size,cords[1]-size)]
    near_n = []
    for n in near_points:
        for obj in POINTS_pos:
            cords_near = (obj.point_pos.centerx, obj.point_pos.centery)
         
            if n == cords_near:
                near_n.append(obj) 
    
    for obj in near_n:
        obj.draw_point((obj.point_pos.centerx, obj.point_pos.centery),BLACK)
    
    return near_n
    
def pick_another_point(point_x):
    neigh = find_near_points(point_x)
    mouse_cords = (mouse_x,mouse_y)

    for obj in neigh:
        if obj.point_radius.collidepoint(mouse_cords):
            obj.checked = True
           
        else:
            obj.checked = False
            

        if obj.checked == True:
           
            end_point = obj.cords
            line=((point_x.centerx,point_x.centery),end_point)
                
            if (line[0],line[1]) in LINES or (line[1],line[0]) in LINES:
                print('Ta linia juz istnieje')
            else:
                pygame.draw.line(DISPLAYSURF,BLACK,line[0],line[1],3)
                LINES.append(line)          
                for x in POINTS_pos:
                    if x.cords == end_point:
                        current_point = x
                
                        clear_display(POINTS_pos)
                        find_near_points(current_point.point_pos)
                        return current_point.point_pos
    current_point = point_x
    return current_point
            
while True:

    if not POINTS_pos:
        BALL = (250,300) #Startowa pozycja
        draw_points() #Rozrysuj punkty i in radius aby były łatwiejsze do wybierania 
        draw_court(POINTS_pos)      
        current_point = check_position(BALL,POINTS_pos)
        pick_another_point(current_point)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos 
        elif event.type == MOUSEBUTTONUP:
            #isClicked=True   
            current_point = pick_another_point(current_point)
        elif event.type == KEYDOWN:
            check_index()
       
    pygame.display.update()