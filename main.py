import pygame, sys
from pygame.locals import *
import threading
import time
import random
import collections
import sys
import numpy as np
from player import Player
from points import Points, Node



pygame.init()

WINDOWWIDTH = 720 
WINDOWHEIGHT = 655
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
pygame.display.set_caption('Paper Soccer')

# COLORS
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (128,128,128)
LIGHTSLATEGRAY = (119,136,153)
FOREST = (0,118,0)

#BOARD
size = 50
boardwidth = 8
boardheight = 11

#MOUSE COORDIATES
mouse_x = 0
mouse_y = 0

#TIMERS
clock = pygame.time.Clock()
frame_count = 0
frame_rate = 60
start_ticks = 20

#FONTS
font = pygame.font.Font('freesansbold.ttf', 32) 
font_player = pygame.font.Font('freesansbold.ttf', 16) 
font_button = pygame.font.Font('freesansbold.ttf', 24) 

POINTS_pos = [] #ALL POINTS ON BOARD
LINES = [] #ALL ACTIVE LINE ON BOARD
LINES_TEST  = []
PLAYERS = [] #PLAYERS
point_pos_cords = []
#ACTIVE STATEMENTS
active_player=None
unactive_player=None
possible_moves = True
possible_moves_minmax = True
someone_won = False
current_point_minmax = None
DISPLAYSURF.fill(FOREST)

# OMITTED POINTS TO DRAW THE BOARD
point_for_skip = [(1,1),(1,2),(1,3),(1,7),(1,8),(1,9),
                (boardheight+1,1),(boardheight+1,2),(boardheight+1,3),
                (boardheight+1,7),(boardheight+1,8),(boardheight+1,9)]
            
def draw_court(Points_list):
    """

    """
    left_side_idx = [x for x in range(0,10)] #LEFT SIDE BOARD
    right_side_idx = [y for y in range(86,96)] # RIGHT SIDE BOARD
    down_side_idx = [9,19,29,40,41,53,65,64,75,85,95] #DOWN SIDE BOARD
    up_side_idx = [0,10,20,31,30,42,54,55,66,76,86] # UP SIDE BOARD
    
    draw_line_in_court(left_side_idx)
    draw_line_in_court(right_side_idx)
    draw_line_unsorted_in_court(up_side_idx)
    draw_line_unsorted_in_court(down_side_idx)
    draw_line_unsorted_in_court([20,30])
    draw_line_unsorted_in_court([66,54])
    draw_line_unsorted_in_court([29,41])
    draw_line_unsorted_in_court([75,65])

def draw_line_unsorted_in_court(list_):
    """
    The function draws lines between points.
    The points are found after the indices in the received list.
    Indexes are unsorted, used to draw gates.
    """  
    points_in = []
    for x in list_:
        for idx,point in enumerate(POINTS_pos):
            if x == idx:
                points_in.append(point)
                
        for x in range(0,len(points_in)-1):
            start = (points_in[x].point_pos.centerx,points_in[x].point_pos.centery) #Start point
            end = (points_in[x+1].point_pos.centerx,points_in[x+1].point_pos.centery) #End point
            line = (start,end) #ex line ((150,200),(250,300))
            pygame.draw.line(DISPLAYSURF,BLACK,line[0],line[1],3) #Draw line beetween points
            LINES.append(line)
            LINES.append((line[1],line[0])) #Add line to existing lines
            
def draw_line_in_court(list_):
    """
    The function draws lines between points.
    The points are found after the indices in the received list.
    """
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
            LINES.append((line[1],line[0]))
              
def draw_points():
    """
    The function draw all points and their radius for better find on board.
    """
    goal_points_idx = [(1,4),(1,5),(1,6),(12,4),(12,5),(12,6)] #Points in gates
    cnt = 0
    for i in range(1,boardwidth+2):
        for z in range(1,boardheight+2):
            if (z,i) in point_for_skip:
                continue
            if cnt%2 == 0:
                point_radius = pygame.draw.circle(DISPLAYSURF,FOREST,(size*i,size*z),15) 
                point_p=pygame.draw.circle(DISPLAYSURF,WHITE,(size*i,size*z),4)                  
            else:
                point_radius = pygame.draw.circle(DISPLAYSURF,FOREST,(size*i,size*z),15)
                point_p =pygame.draw.circle(DISPLAYSURF,WHITE,(size*i,size*z),4)         
            x = (size*i,size*z)
            
            if (z,i) in goal_points_idx:
                if goal_points_idx.index((z,i)) in [0,1,2]:
                    POINTS_pos.append(Points(cords=x,point_pos=point_p,pointradius=point_radius,p1_goal=True)) #Points for upper gate (Player2-gate)
                else:
                    POINTS_pos.append(Points(cords=x,point_pos=point_p,pointradius=point_radius,p2_goal=True)) #Points for bottom gate (Player1-gate)
            else:
                POINTS_pos.append(Points(cords=x,point_pos=point_p,pointradius=point_radius))            
            cnt+=1
        cnt -= 1

def get_all_lines():
    all_lines = []
    for x in POINTS_pos:
        current_point = x                                
                 
        near = find_near_points(current_point.point_pos)                  
        for elem in near:
            all_lines.append((current_point.cords,elem.cords))
            all_lines.append((elem.cords,current_point.cords))  
    all_lines = removeDuplicates(all_lines)
    all_lines = list(set(all_lines)- set(LINES))
    return all_lines

def A_star_alg(lines, start_point, end_point):
    start_node = Node(None,start_point)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None,end_point)
    end_node.g = end_node.h = end_node.f = 0

    all_lines_ = get_all_lines()  
    open_list = []
    closed_list = set()

    open_list.append(start_node)
    
    while len(open_list) > 0: 
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        open_list.pop(current_index)
        closed_list.add(current_node)
       
        if current_node == end_node:
            path = []
            current = current_node           
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children = []
        for new_position in [(-50,-50),(-50,0),(-50,50),(0,-50),(0,50),(50,-50),(50,0),(50,50)]:
                       
            node_position = (current_node.position[0] + new_position[0],current_node.position[1]+new_position[1])
            tuple_new_node = (current_node.position,node_position)
            if (tuple_new_node[0],tuple_new_node[1]) and (tuple_new_node[1],tuple_new_node[0]) not in all_lines_:       
                continue 

            new_node = Node(current_node, node_position)      
            children.append(new_node)          
            pygame.display.flip()      
        #print("Ilosc mozliwych ruchow",len(children))
        #print("Mozliwe punkty dla danej galezi",children)
        for child in children: 

            if child in closed_list:             
                 continue
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h
            
            for open_node in open_list:               
                if child == open_node and child.g > open_node.g:
                    continue           
            open_list.append(child)   
    return None

def refresh_display(points_):
    """
    The function refresh points that are not within the ball.
    """
    for obj in points_:
        #obj.draw_point(obj.cords,FOREST,6) 
        obj.draw_point(DISPLAYSURF,obj.cords,WHITE,4)
        
def check_position(ball_, points_):
    """
    The function return coordinates ball.
    """
    points_cords = points_   
    ball_cords = ball_   
    for obj in points_cords:
        if(obj.cords == ball_cords):
            current_point_cord=obj.point_pos   
            return current_point_cord 

def check_index():
    """
    The function for check index of specific point.
    Used during development.
    """
    mouse_cords = (mouse_x,mouse_y)  
    for idx,obj in enumerate(POINTS_pos):
        if obj.point_radius.collidepoint(mouse_cords):
            print(idx)
            print(obj.cords)

def evaluate(LINES_):
    for line in LINES_:
        if line == ((200,100),(250,50)) or line == ((250,100),(250,50)) or line == ((300,100),(250,50)):
            return 1000
        elif line == ((200,550),(250,600))  or line == ((250,550),(250,600)) or line == ((300,550),(250,600)):
            return -1000
    return 0

def isMovesLeft(goal_point):
    if possible_moves_minmax is False:
        return False
    if goal_point is True:
        return False

def find_best_move(point_x):
    global LINES_TEST, possible_moves_minmax
    bestValue = 0
    LINES_T = LINES.copy()
    nears = find_near_points(point_x)
    #moves = set()
    random.shuffle(nears)
    for move in nears:  
        LINES_TEST = LINES_T.copy()
        if (point_x.centerx,point_x.centery,move.cords) in LINES_TEST or (move.cords, (point_x.centerx,point_x.centery)) in LINES_TEST:
                continue    
        #if ((point_x.centerx,point_x.centery) ,move) in LINES:
        #    continue
        #moves.add(((point_x.centerx,point_x.centery), move))
        #moves.add((move, (point_x.centerx,point_x.centery)))
        
        near_m = find_near_points(move.point_pos)
        random.shuffle(near_m)
        for move_m in near_m:
            possible_moves_minmax=True
            move_value = minimax(move_m,0,False,LINES_TEST)
            #print('oho', move_value)
            LINES_TEST = LINES_T.copy()
            #DISPLAYSURF.fill(FOREST)
            #draw_court(POINTS_pos)
            #refresh_display(POINTS_pos)
            if move_value > bestValue:                
                bestMove = move     
                bestValue = move_value 
        #print('Value for near {0} : {1}'.format(move, move_value))
        #moves.remove(((point_x.centerx,point_x.centery), move))
        #moves.remove((move, (point_x.centerx,point_x.centery)))
            
    print('Value for best move {0} is {1}'.format(bestMove, bestValue))
    
    return bestMove

def minimax(point_pocz, depth, isMax,lines_test):
    #if(depth > 10):
     #   pygame.quit()
    #    sys.exit()
    global current_point_minmax, possible_moves_minmax
    x = LINES_TEST
    value = evaluate(lines_test)
    
    if value == 1000:
        return (value -50*depth)
    if value == -1000:
        return (value - 50*depth )
    if possible_moves_minmax == False and isMax == True:
        return (-200 - 20*depth)
    if possible_moves_minmax == False and isMax == False:
        return (200 - 20*depth)
    best_ = []

    if isMax:
        best = -1000
        nears = find_near_points(point_pocz.point_pos)
        random.shuffle(nears)
        for point in nears:
            possible_moves_minmax=True
            if (point_pocz.cords,point.cords) in LINES_TEST or (point.cords, point_pocz.cords) in LINES_TEST:
                continue
            current_point_minmax = pick_point_for_minmax(point_pocz,point,x,isMax=False)
            best = max(best, minimax(current_point_minmax,depth+1,isMax = False,lines_test=x))
        #print('Depth', depth)         
        return best
    else:
        best = 1000
        nears = find_near_points(point_pocz.point_pos)
        random.shuffle(nears)
        for point in nears:
            possible_moves_minmax=True
            if (point_pocz.cords,point.cords) in LINES_TEST or (point.cords, point_pocz.cords) in LINES_TEST:
                continue
            current_point_minmax = pick_point_for_minmax(point_pocz,point,x,isMax=True)
            best = min(best, minimax(current_point_minmax,depth+1,isMax = True,lines_test=x))         
            #lines_test = x.copy()
        #print('Depth', depth) 
        return best

def pick_point_for_minmax(point_x,punkt_sas,LINES_test,isMax):
    global current_point_minmax, possible_moves_minmax
    neigh = find_near_points(point_x.point_pos)
    
    for obj in neigh:
        if obj.point_radius.collidepoint(punkt_sas.cords):
            obj.checked = True       
        else:
            obj.checked = False

        if obj.checked is True:
            start_point = (point_x.point_pos.centerx, point_x.point_pos.centery)         
            end_point = obj.cords

            if (start_point, end_point) in LINES_test or (end_point,start_point) in LINES_test: #IF LINE EXIST RETURN             
               current_point_minmax = point_x
               return current_point_minmax
            else:
                if isMax is True:
                    color = RED
                else:
                    color = BLUE
                #time.sleep(0.1)
                #pygame.draw.line(DISPLAYSURF, color, start_point, end_point, 1)
                    
                #pygame.display.update()
                possible_lines = []
                possibles_lines_for_next_step = []
                LINES_test.append((start_point,end_point))
                LINES_test.append((end_point,start_point))
                
                for x in POINTS_pos:
                    if x.cords is end_point:                
                        current_point_minmax = x  

                        near = find_near_points(current_point_minmax.point_pos,double_lines=True)                  
                        for elem in near:
                            possible_lines.append((current_point_minmax.cords,elem.cords))
                            possible_lines.append((elem.cords,current_point_minmax.cords))

                        possibles_lines_for_next_step = possible_lines.copy()
                    
                        last_line = LINES_test[-1:][0]
                                        
                        possibles_lines_for_next_step.remove((last_line[0],last_line[1]))
                        possibles_lines_for_next_step.remove((last_line[1],last_line[0]))
                        

                        actual_lines = [line for line in possible_lines if line in LINES_test]

                               
                        if len(actual_lines) == (2 * len(near)):    
                            possible_moves_minmax = False
                            #print('Zacial sie')     
                            #next_n = True
                                                                                                                                                    
                        if any(elem in LINES_test for elem in possibles_lines_for_next_step):
                            for point in near:
                                if (point_x.cords,point.cords) in LINES_TEST or (point.cords, point_x.cords) in LINES_TEST:
                                    continue                                
                                current_point_minmax = pick_point_for_minmax(current_point_minmax,point,LINES_test,isMax)
                            return current_point_minmax                        
                        else:
                            return current_point_minmax
    current_point_minmax = point_x
    return current_point_minmax
        

def find_near_points(point_p,double_lines=False):

    cords = (point_p.centerx,point_p.centery)
    near_points = [(cords[0]-size,cords[1]+size),(cords[0],cords[1]+size),(cords[0]+size,cords[1]+size),
                    (cords[0]-size,cords[1]),(cords[0]+size,cords[1]),
                    (cords[0]-size,cords[1]-size),(cords[0],cords[1]-size),(cords[0]+size,cords[1]-size)]
    near_n = []
    for n in near_points:
        for obj in POINTS_pos:
            cords_near = (obj.point_pos.centerx, obj.point_pos.centery)
            
            #if double_lines is False:
                #if (cords,cords_near) in LINES or (cords_near,cords) in LINES or (cords,cords_near) in LINES_TEST or (cords_near,cords) in LINES_TEST :
                    #continue 
            if n == cords_near:
                near_n.append(obj)  
    for obj in near_n:
        obj.draw_point(DISPLAYSURF,(obj.point_pos.centerx, obj.point_pos.centery),BLACK,4)  
    return near_n          

def clear_lines(LINES):
    DISPLAYSURF.fill(FOREST)

def check_goal(obj):
  
    global someone_won
    if obj.p1_goal == True:
        someone_won=True
        check_index()
        #value = evaluate(LINES)
        #print('Wartośc planszy', value)
        print('GAME ENDED: PLAYER: ',player2.name + ' WON!')
        player2.points = player2.points + 1       
    if obj.p2_goal == True:
        someone_won=True
        check_index()
        #value = evaluate(LINES)
        #print('Wartośc planszy', value)
        print('GAME ENDED: PLAYER: ',player1.name + ' WON!')
        player1.points = player1.points + 1       

def removeDuplicates(lst):       
    return [t for t in (set(tuple(i) for i in lst))] 

def bot_move(current_point):
    end = (250,50)     
    start_pos = (current_point.centerx,current_point.centery)         
    #path = A_star_alg(POINTS_pos, start_pos, end)
    path = find_best_move(current_point)
    #print(path)
    if path is not None:
        path_cords = path
    
        
    else:
        print('Nie ma juz wybrow lool')
        neigh = find_near_points(current_point)
        neigh_choice = random.choice(neigh)
        path_cords = neigh_choice.cords    
    current_point = pick_another_point(current_point,True,mouse_cords_=path_cords.cords)
    #print("Bot wykonał ruch: ",path_cords)
    return current_point

def name_moves(list_moves):
    dict_moves = {}
    for x in list_moves:
        if x == (-50,50):  
            dict_moves['7'] = x
        if x == (0,50):
            dict_moves['8'] = x
        if x == (50,50):
            dict_moves['9'] = x
        if x == (-50,0):
            dict_moves['4'] = x
        if x == (50,0):
            dict_moves['6'] = x
        if x == (-50,-50):
            dict_moves['1'] = x
        if x == (0,-50):
            dict_moves['2'] = x
        if x == (50,-50):
            dict_moves['3'] = x
    return dict_moves

def check_won():
        global POINTS_pos

        if someone_won is True:
                        time.sleep(5)
                        change_turn()
                        clear_lines(LINES)
                        POINTS_pos.clear()
                        
def change_turn():   
        if player1.turn is False:
            player2.turn=False
            player1.turn=True
        else:
            player1.turn=False
            player2.turn=True  

def pick_another_point(point_x, bot=False,key=None,mouse_cords_=False):
    global current_point
    global active_player
    global possible_moves
    
    neigh = find_near_points(point_x)
    #print(neigh)
    #NUMPAD MOVING
    pos_moves_numpad = []
    for x in neigh:
            tuple_current = (point_x.centerx,point_x.centery)
            move = tuple(map(lambda i,j: i - j,x.cords ,tuple_current))
            pos_moves_numpad.append(move)
    pos_moves_numpad = name_moves(pos_moves_numpad) 
    
    #BOT MOVING
    if bot is True:
        mouse_cords = mouse_cords_
    elif key is not None:       
        mouse_cords = tuple(map(lambda i,j: i + j,(point_x.centerx,point_x.centery) ,pos_moves_numpad[key]))     
    elif bot is False and key is None:
        mouse_cords = (mouse_x,mouse_y)
    
    for obj in neigh:
        if obj.point_radius.collidepoint(mouse_cords):
            obj.checked = True       
        else:
            obj.checked = False

        if obj.checked is True:
            start_point = (point_x.centerx,point_x.centery)         
            end_point = obj.cords
            line=(start_point,end_point) 

            if (start_point, end_point) in LINES or (end_point,start_point) in LINES: #IF LINE EXIST RETURN             
               current_point = point_x
               return current_point          
            
            else:
                for x in PLAYERS:
                    if x.turn is True:
                        active_player = x
                pygame.draw.line(DISPLAYSURF, active_player.color, start_point, end_point, 3)
                
                pygame.display.update()             
                possible_lines = []
                possibles_lines_for_next_step = []
                LINES.append((start_point,end_point))
                LINES.append((end_point,start_point))

                check_goal(obj)
                check_won()
                for x in POINTS_pos:
                    if x.cords is end_point:                
                        current_point = x  
                        refresh_display(POINTS_pos)                                                      
                        near = find_near_points(current_point.point_pos,double_lines=True)                  
                        for elem in near:
                            possible_lines.append((current_point.cords,elem.cords))
                            possible_lines.append((elem.cords,current_point.cords))

                        ### Do podwojnych ruchów
                        possibles_lines_for_next_step = possible_lines.copy()
                        last_line = LINES[-1:][0]    
                        possibles_lines_for_next_step.remove((last_line[0],last_line[1]))
                        possibles_lines_for_next_step.remove((last_line[1],last_line[0]))

                        actual_lines = [line for line in possible_lines if line in LINES]
                    
                        if len(actual_lines) == (2*len(near)):
                            #print('Nie ma więcej ruchów')
                            possible_moves = False
                                                                                                  
                        if any(elem in LINES for elem in possibles_lines_for_next_step):
                            if bot is True:                                                                
                                current_point = bot_move(current_point.point_pos)          
                            else:                         
                                current_point = pick_another_point(current_point.point_pos)
                            return current_point                         
                        else:
                            change_turn()
                            return current_point.point_pos
    current_point = point_x
    return current_point

def draw_text(text,font,color,surface,x,y):
    textObj = font.render(text,True,color)
    textRect = textObj.get_rect()
    textRect.topleft = (x, y)
    surface.blit(textObj, textRect)


click = False
 
#MAIN MENU
def main_menu():
    while True:
        DISPLAYSURF.fill(FOREST)
        draw_text('PAPER SOCCER', font, WHITE, DISPLAYSURF ,235, 20)
 
        mouse_x, mouse_y = pygame.mouse.get_pos()

        button_1player = pygame.Rect(260, 100, 200, 50)
        button_2players = pygame.Rect(260, 200, 200, 50)      
        if button_1player.collidepoint((mouse_x, mouse_y)):
            if click:
                game_loop()     
        if button_2players.collidepoint((mouse_x, mouse_y)):
            if click:
                game_loop(two_player=True)
        pygame.draw.rect(DISPLAYSURF, (255, 0, 0), button_1player)
        draw_text('1 PLAYER',font_button,WHITE,DISPLAYSURF,button_1player.centerx-85,button_1player.centery-10)
        pygame.draw.rect(DISPLAYSURF, (255, 0, 0), button_2players)
        draw_text('2 PLAYERS',font_button,WHITE,DISPLAYSURF,button_2players.centerx-85,button_2players.centery-10)
 
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
#GAME        
def game_loop(two_player=False):
    global mouse_x, mouse_y, player1, player2, POINTS_pos, LINES, current_point, someone_won, possible_moves
    #sys.setrecursionlimit(100000)
    running = True
    while running:       
        if not POINTS_pos:
            DISPLAYSURF.fill(FOREST)
            possible_moves=True
            someone_won=False

            if not PLAYERS:
                player1 = Player('Jacek',RED)
                player2 = Player('Robert',BLUE)
                    
                player1.turn=True
                PLAYERS.append(player1)
                PLAYERS.append(player2)

            player1_name = player1.name
            player2_name = player2.name
            player1_points = "Points: {0}".format(player1.points)
            player2_points = "Points: {0}".format(player2.points)
                
            
            LINES = []
            #point_pos_cords.clear()
            BALL = (250,300) #Startowa pozycja
            
            draw_points() #Rozrysuj punkty i in radius aby były łatwiejsze do wybierania 
            draw_court(POINTS_pos)     
            current_point = check_position(BALL,POINTS_pos)
                
            #for x in POINTS_pos:
                #point_pos_cords.append(x.cords) 
            pick_another_point(current_point,False)
            LINES = removeDuplicates(LINES)
                
            #total_seconds = start_ticks - (frame_count // frame_rate)
            #if total_seconds == 0:
            #    change_turn()
            #    frame_count=0
        
            #minutes = total_seconds // 60
            #seconds = total_seconds % 60
            #output_string = "Time: {0:02}".format(seconds)

        if player1.points == 3:
            POINTS_pos.clear()
            PLAYERS.clear()      
            print('Player 1 Won')
            running=False
            return running
        if player2.points == 3:
            POINTS_pos.clear() 
            PLAYERS.clear() 
            print('Player 2 Won') 
            running=False
            return running

        if two_player is True:
            if player2.turn is True:
                active_player_string ="Turn for: {0}".format(player2.name)
            else:
                active_player_string ="Turn for: {0}".format(player1.name)
        else: 
            if player2.turn is True:
                active_player_string ="Turn for: {0}".format(player2.name)      
                current_point = bot_move(current_point)
            else:
                active_player_string ="Turn for: {0}".format(player1.name)
            
        if possible_moves is False:    
            for player in PLAYERS:
                if player.turn is not True:                                    
                    player.points += 1
                    clear_lines(LINES)                                         
                    POINTS_pos.clear()
        
        pygame.draw.rect(DISPLAYSURF,WHITE,(460,0,300,640)) #WHITE BOX FOR REFRESH TEXT DRAWING
        pygame.draw.rect(DISPLAYSURF,LIGHTSLATEGRAY,(0,0,720,45))
        pygame.draw.rect(DISPLAYSURF,LIGHTSLATEGRAY,(0,610,720,45))

        draw_text(active_player_string,font_player,BLACK,DISPLAYSURF,540,110)
        draw_text(player1_name,font_player,BLACK,DISPLAYSURF,20,20)
        draw_text(player2_name,font_player,BLACK,DISPLAYSURF,20,630)
        draw_text(player1_points,font_player,BLACK,DISPLAYSURF,90,20)
        draw_text(player2_points,font_player,BLACK,DISPLAYSURF,90,630)
            
            #frame_count += 1
            #clock.tick(frame_rate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos 
            elif event.type == MOUSEBUTTONUP:
                    #refresh_display(POINTS_pos)        
                #print('Jacek start',(current_point.centerx, current_point.centery))
                current_point = pick_another_point(current_point,False)
                  
                # NUMPAD    
            elif event.type == KEYDOWN:
                if event.key == K_KP1:
                    k='7'
                    current_point = pick_another_point(current_point,False,k)
                if event.key == K_KP2:
                    k='8'
                    current_point = pick_another_point(current_point,False,k)
                if event.key == K_KP3:
                    k='9'
                    current_point = pick_another_point(current_point,False,k)
                if event.key == K_KP4:
                    k='4'
                    current_point = pick_another_point(current_point,False,k)
                if event.key == K_KP5:
                    find_best_move(current_point)  
                if event.key == K_KP6:
                    k='6'
                    current_point = pick_another_point(current_point,False,k)
                if event.key == K_KP7:
                    k='1'
                    current_point = pick_another_point(current_point,False,k)
                if event.key == K_KP8:
                    k='2'
                    current_point = pick_another_point(current_point,False,k)
                if event.key == K_KP9:
                    check_index()
                    #k='3'
                    #current_point = pick_another_point(current_point,False,k)      
                    
            elif event.type == KEYUP:
                pass  
                    
        pygame.display.update()

main_menu()