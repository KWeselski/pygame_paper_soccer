import pygame, sys
from pygame.locals import *
import threading
import time
import random
import collections
import sys
class Points():

    def draw_point(self,cords,color):
        point = pygame.draw.circle(DISPLAYSURF,color,(cords[0],cords[1]),4)

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
GRAY = (128,128,128)
LIGHTSLATEGRAY = (119,136,153)

size = 50
boardwidth = 8
boardheight = 11

mouse_x = 0
mouse_y = 0


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
liny =[]
PLAYERS = []
active_player=None
unactive_player=None
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
                point_p=pygame.draw.circle(DISPLAYSURF,GRAY,(size*i,size*z),4)                  
            else:
                point_radius = pygame.draw.circle(DISPLAYSURF,WHITE,(size*i,size*z),15)
                point_p =pygame.draw.circle(DISPLAYSURF,GRAY,(size*i,size*z),4)         
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
    #pygame.draw.rect(DISPLAYSURF,BLACK,[size,size,boardwidth*size,boardheight*size],1)

def clear_display(points_):
    for obj in points_:
        obj.draw_point(obj.cords,GRAY)

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

def change_turn():
    
    if player1.turn == False:
        player2.turn=False
        player1.turn=True
        print('Tura dla: ',player1.name)
    else:
        player1.turn=False
        player2.turn=True
def clear_lines(LINES):
    DISPLAYSURF.fill(WHITE)

def check_goal(obj):

    if obj.p1_goal == True:
        print('GAME ENDED: PLAYER: ',player2.name + ' WON!')
        player2.points = player2.points + 1
        clear_lines(LINES)
        POINTS_pos.clear()
    if obj.p2_goal == True:
        print('GAME ENDED: PLAYER: ',player1.name + ' WON!')
        player1.points = player1.points + 1
        clear_lines(LINES)
        POINTS_pos.clear()

def removeDuplicates(lst):       
    return [t for t in (set(tuple(i) for i in lst))] 


"""def find_shortest_path(graph,start,end,path=[]):

    path = path + [start]
    
    #path = removeDuplicates(path)
    if start == end:
        print("Znaleziono")
        return path 
    if not start in graph:
        None
    for node in graph[start]:
        if node.cords not in path:
            pygame.draw.line(DISPLAYSURF,GREEN,start,node.cords)
            newpath = find_shortest_path(graph, (node.point_pos.centerx,node.point_pos.centery), end, path)         
            if newpath: return newpath
    return None
    
    #dist = {start: [start]}
    #q = collections.deque(start)
    #print(q)
    #while len(q):
    #    at = q.popleft()
    #    print(at)
    #    for next in graph[at]:
    #        if next not in dist:
    #            dist[next] = [dist[at], next]
    #            q.append(next)
    #return dist.get(end)
    path = path + [start]
    if start == end:
        return path
    if not start in graph:  
        return None
    shortest = None
    for node in graph[start]:    
        if node.cords not in path:            
            newpath = find_shortest_path(graph,(node.point_pos.centerx,node.point_pos.centery),end,path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest"""

def make_graph():
    graph = {}
    for point in POINTS_pos:
        near = find_near_points(point.point_pos)
        graph[point.cords] = near
    return graph
    

def bot_move(current_point):
    current_point = pick_another_point(current_point,True)
    return current_point
    print('bocik')

def pick_another_point(point_x , bot=False):
    global current_point
    global frame_count
    global active_player
    global unactive_player
    print("POINT_X",(point_x.centerx,point_x.centery))
    neigh = find_near_points(point_x)
    if bot is True:
        neigh_choice = random.choice(neigh)
        mouse_cords = neigh_choice.cords       
    else:
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
            
            if (line[0],line[1]) in LINES or (line[1],line[0]) in LINES and bot==True:
                print('Bot utworzył ta sama linie')

            else:
                for x in PLAYERS:
                    if x.turn == True:
                        active_player = x
                    else:
                        unactive_player = x               
                pygame.draw.line(DISPLAYSURF,active_player.color,line[0],line[1],3)
                
                check_goal(obj)
                possible_lines = []
                LINES.append(line)


                for x in POINTS_pos:
                    if x.cords == end_point:
                        print('ENDPOINT', end_point)
                        current_point = x 
                                  
                        clear_display(POINTS_pos)          
                        near = find_near_points(current_point.point_pos)                  
                        for elem in near:
                            possible_lines.append((current_point.cords,elem.cords))
                            possible_lines.append((elem.cords,current_point.cords))

                        possibles_lines_test = possible_lines
                        last_line = LINES[-1:][0]
                        
                        possibles_lines_test.remove((last_line[0],last_line[1]))
                        possibles_lines_test.remove((last_line[1],last_line[0]))
                        
                        actual_lines = [] 
                        for ps_line in possible_lines:
                            for line_ in LINES:
                                
                                if ps_line == line_:
                                    actual_lines.append(ps_line)                                    
                                    if len(actual_lines) == len(near):
                                        print('Nie ma więcej ruchów')
                                        for player in PLAYERS:
                                            if player.turn != True:
                                                time.sleep(5)
                                                player.points += 1
                                                clear_lines(LINES)                                           
                                                POINTS_pos.clear()
                        if any(elem in LINES for elem in possibles_lines_test):
                            current_point = pick_another_point(current_point.point_pos,bot=False) 
                            return current_point                         
                        else:
                            change_turn()
                            frame_count=0
                            return current_point.point_pos
    current_point = point_x
    return current_point

while True:
    
    if not POINTS_pos:
        if not PLAYERS:
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
        pick_another_point(current_point,False)
        LINES = removeDuplicates(LINES)
        
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
    
    if player2.turn == True:
        pass
        #current_point = bot_move(current_point)

    active_player_text = font_player.render(active_player_string, True, BLACK) 
    text = font.render(output_string, True, BLACK)
    player1_name_text = font_player.render(player1_name,True,BLACK)
    player2_name_text = font_player.render(player2_name,True,BLACK)
    player1_points_text = font_player.render(player1_points,True,BLACK)
    player2_points_text = font_player.render(player2_points,True,BLACK)

    pygame.draw.rect(DISPLAYSURF,WHITE,(460,0,300,640)) #WHITE BOX FOR REFRESH TEXT DRAWING
    pygame.draw.rect(DISPLAYSURF,LIGHTSLATEGRAY,(0,0,720,45))
    pygame.draw.rect(DISPLAYSURF,LIGHTSLATEGRAY,(0,610,720,45))

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
            current_point = pick_another_point(current_point,False)
            
        elif event.type == KEYDOWN:
            pass
           
            
        elif event.type == KEYUP:
            pass  
            

    pygame.display.update()