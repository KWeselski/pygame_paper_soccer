import pygame, sys
from pygame.locals import *

class Points():
    """
    Points objects on which the player moves
    """
    def draw_point(self,display,cords,color,size):
        point = pygame.draw.circle(display,color,(cords[0],cords[1]),size)

    def __init__(self,cords=(0,0),checked=False,point_pos=pygame.Rect,pointradius=pygame.Rect,p1_goal=False,p2_goal=False):
        self.cords = cords
        self.checked = checked
        self.point_pos = point_pos
        self.point_radius = pointradius
        self.p1_goal=p1_goal
        self.p2_goal=p2_goal

    def __repr__(self):
        return(str(self.cords))

class Node():

    def __init__(self,parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
    
    def __eq__(self, other):
        return self.position == other.position

    def __repr__(self):
        return str((self.position))
    
    def __hash__(self):              
        return hash(self.position)
    