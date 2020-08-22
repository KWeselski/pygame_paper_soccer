import pygame, sys
from pygame.locals import *
import threading
import time

class Points():

    def draw_point(self,cords,color):
        point = pygame.draw.circle(DISPLAYSURF,color,(cords[0],cords[1]),5)

    def __init__(self,cords=(0,0),checked=False,point_pos=pygame.Rect,pointradius=pygame.Rect,p1_goal=False,p2_goal=False):
        self.cords = cords
        self.checked = checked
        self.point_pos = point_pos
        self.point_radius = pointradius
        self.p1_goal=p1_goal
        self.p2_goal=p2_goal

    def __repr__(self):
        return(str(self.cords))

class Player():

    def __init__(self,name,color,points=0,turn=False):    
        self.name = name
        self.color = color
        self.turn = turn
        self.points = points
    
pygame.init()

WINDOWWIDTH = 720
WINDOWHEIGHT = 655
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
frame_count = 0

clock = pygame.time.Clock()

frame_rate = 60
start_ticks = 15
font = pygame.font.Font('freesansbold.ttf', 32) 
font_player = pygame.font.Font('freesansbold.ttf', 16) 
POINTS_pos = []
LINES = []
PLAYERS = []
active_player=None
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
    goal_points_idx = [(1,4),(1,5),(1,6),(12,4),(12,5),(12,6)]
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
            
            if (z,i) in goal_points_idx:
                if goal_points_idx.index((z,i)) in [0,1,2]:
                    POINTS_pos.append(Points(cords=x,point_pos=point_p,pointradius=point_radius,p1_goal=True))
                else:
                    POINTS_pos.append(Points(cords=x,point_pos=point_p,pointradius=point_radius,p2_goal=True))
            else:
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

def countdown(seconds):    
    if int(seconds) > 15:
            seconds=-1
            return seconds       
    print("Seconds: {:.0f}".format(seconds))            

def change_turn():
    
    if player1.turn == False:
        player2.turn=False
        player1.turn=True
        print('Tura dla: ',player1.name)
    else:
        player1.turn=False
        player2.turn=True
        print('Tura dla: ', player2.name)

def clear_lines(LINES):
    DISPLAYSURF.fill(WHITE)

def pick_another_point(point_x):
    global frame_count
    global active_player
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
                for x in PLAYERS:
                    if x.turn == True:
                        active_player = x               
                pygame.draw.line(DISPLAYSURF,active_player.color,line[0],line[1],3)
                
                if obj.p1_goal == True:
                    print('GAME ENDED: PLAYER: ',player2.name + ' WON!')
                    clear_lines(LINES)
                    POINTS_pos.clear()
                if obj.p2_goal == True:
                    print('GAME ENDED: PLAYER: ',player1.name + ' WON!')
                    clear_lines(LINES)
                    POINTS_pos.clear()
                    
                LINES.append(line)          
                for x in POINTS_pos:
                    if x.cords == end_point:
                        current_point = x             
                        clear_display(POINTS_pos)          
                        find_near_points(current_point.point_pos)
                        change_turn()
                        frame_count=0
                        return current_point.point_pos
    current_point = point_x
    return current_point

def print_goal_points():
    i=0
    for idx,point in enumerate(POINTS_pos):
        if point.goalpoint==True:
            print(idx,point)
        else:
            i+=1
    print(i)

while True:

    if not POINTS_pos:
        player1 = Player('Jacek',RED)
        player2 = Player('Robert',BLUE)
        PLAYERS.append(player1)
        PLAYERS.append(player2)
        player1_name = player1.name
        player2_name = player2.name

        player1_points = "Points: {0}".format(player1.points)
        player2_points = "Points: {0}".format(player2.points)

        player1.turn = True
        frame_count=0
        LINES = []
        BALL = (250,300) #Startowa pozycja
        draw_points() #Rozrysuj punkty i in radius aby były łatwiejsze do wybierania 
        draw_court(POINTS_pos)      
        current_point = check_position(BALL,POINTS_pos)
        pick_another_point(current_point)
        
    total_seconds = start_ticks - (frame_count // frame_rate)
    if total_seconds == 0:
        change_turn()
        frame_count=0

    minutes = total_seconds // 60
    seconds = total_seconds % 60
    output_string = "Time: {0:02}".format(seconds)
    for x in PLAYERS:
        if x.turn == True:
            active_player_string ="Turn for: {0}".format(x.name)
    
    

    active_player_text = font_player.render(active_player_string, True, BLACK) 
    text = font.render(output_string, True, BLACK)
    player1_name_text = font_player.render(player1_name,True,BLACK)
    player2_name_text = font_player.render(player2_name,True,BLACK)
    player1_points_text = font_player.render(player1_points,True,BLACK)
    player2_points_text = font_player.render(player2_points,True,BLACK)

    pygame.draw.rect(DISPLAYSURF,WHITE,(460,0,300,640)) #WHITE BOX FOR REFRESH TEXT DRAWING
    pygame.draw.rect(DISPLAYSURF,GREEN,(0,0,720,45))
    pygame.draw.rect(DISPLAYSURF,GREEN,(0,610,720,45))

    DISPLAYSURF.blit(text, [540, 70])
    DISPLAYSURF.blit(active_player_text,[540,110])
    DISPLAYSURF.blit(player1_name_text, [20, 20])
    DISPLAYSURF.blit(player1_points_text, [90, 20])
    DISPLAYSURF.blit(player2_name_text, [20, 630])
    DISPLAYSURF.blit(player2_points_text, [90, 630])
    
    frame_count += 1
    clock.tick(frame_rate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos 
        elif event.type == MOUSEBUTTONUP:  
            current_point = pick_another_point(current_point)
            
        elif event.type == KEYDOWN:
            print(mouse_x,mouse_y)
    pygame.display.update()