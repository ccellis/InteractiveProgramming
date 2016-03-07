"""
A simple GUI to generate circle plots based on mathematical constants

Authors: Coleman Ellis and Kaitlyn Keil

SoftDes Spring 2016
"""

from math import *
import pygame
from pygame.locals import QUIT
import time
from random import choice

class CirclePlotView(object):
    """ Visualizes the circle plot in a pygame window """
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen

    def draw(self):
        self.screen.fill(pygame.Color('black'))
        for element in self.model.elements:
            pygame.draw.arc(self.screen, pygame.Color(element.color), model.RECTANGLE, element.start_angle, element.stop_angle, element.width)
        for connection in self.model.connections:
            pygame.draw.line(self.screen, pygame.Color(connection.color), connection.start_pos, connection.end_pos, connection.width)
        pygame.display.update()

class ElementArc(object):
    """ An arc section that represents an element (integer or word) of the given 
        thing

        Rect = the bounds of the outer circle
        start_angle = the angle (in radians) at which the arc begins
        stop_angle = the angle (in radians) at which the arc ends
    """
#arc(Surface, color, Rect, start_angle, stop_angle, width=1)
    def __init__(self, start_angle, stop_angle, color, width):
        self.start_angle = start_angle
        self.stop_angle = stop_angle
        self.width = width
        self.color = color

class ConnectionArc(object):
    """ Connects two elements. Currently a straight line.
    """
    #line(Surface, color, start_pos, end_pos, width=1) -> Rect
    def __init__(self, start_pos, end_pos, color, width = 1):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = width
        self.color = color
    
class CirclePlotModel(object):
    """ Stores the state of the circle plot """
    def __init__(self, element_histogram, connection_list, circle_radius = 400):
        self.elements = []
        self.connections = []
        self.ELEMENT_MARGIN_MULTIPLIER = .05
        self.RECTANGLE = pygame.Rect(50, 50, circle_radius * 2, circle_radius * 2)
        self.RADIUS = circle_radius
        self.ELEMENT_WIDTH = 20
        inner_radius = circle_radius - self.ELEMENT_WIDTH

        # For now, we don't care what the elements actually are; we want to make sure it points
        # to the right place with all 10 integers.

        # element_list = sorted(element_histogram.keys())
        element_list = list('0123456789')

        colors = ['red','blue','green','orange','purple']

        wedge_angle = 2*pi / len(element_list)
        margin = wedge_angle * self.ELEMENT_MARGIN_MULTIPLIER
        starting_angle = pi/2 - wedge_angle/2 + margin
        d_theta = wedge_angle - margin

        #A dictionary of possible startpoints
        startpoint_dict = {}

        color_dict = {'0':'#29D5BD','1':'#AA8239','2':'#E43C4C','3':'#246B61','4':'#ECAE3E',
            '5':'#FB3044','6':'#279485','7':'#FFB531','8':'#A43741','9':'#1A413C'}

        for element in element_list:
            arc = ElementArc(starting_angle, starting_angle + d_theta, color_dict[element], self.ELEMENT_WIDTH)
            self.elements.append(arc)

            #Because the number might not have all 10 digits
            if element in element_histogram:
                startpoint_d_theta = d_theta / (element_histogram[element]+1)
                startpoints = [margin - starting_angle - startpoint_d_theta*i for i in range(1,element_histogram[element]+1)]
                startpoint_dict[element] = startpoints

            starting_angle -= wedge_angle

        # Assumes integers
        for first, second in connection_list:
            first_angle = startpoint_dict[first].pop(0)
            first_point_x = 500 + inner_radius*cos(first_angle)
            first_point_y = 500 + inner_radius*sin(first_angle)

            second_angle = startpoint_dict[second][0]
            second_point_x = 500 + inner_radius*cos(second_angle)
            second_point_y = 500 + inner_radius*sin(second_angle)
            connection = ConnectionArc((first_point_x, first_point_y), (second_point_x, second_point_y),color_dict[first])
            self.connections.append(connection)

def generate_connection_histogram(input_list):
    """Given a list of strings, generate two things:
    A list of each pair of adjacent elements as tuples
    A histogram of the number of occurences of each element, stored in a dictionary.

    >>> pair_list, list = generate_connection_histogram(['the','dog','and','the','dog'])
    >>> print pair_list[0]
    ('the', 'dog')
    >>> print pair_list[1]
    ('dog', 'and')
    """
    output_list = []
    element_histogram = {}

    for i in range(len(input_list)-1):
        first = input_list[i]
        second = input_list[i+1]
        pair = (first, second)
        output_list.append(pair)

    for element in input_list:
        element_histogram[element] = element_histogram.get(element,0)+1

    return output_list, element_histogram

def sanitize_float(flt):
    """Given a floating point number, returns a list of the digits of the
    number as strings

    >>> print sanitize_float(3.1415)
    ['3', '1', '4', '1', '5']
    """

    flt_string = str(flt)
    flt_list = list(flt_string)
    if '.' in flt_list:
        flt_list.remove('.')
    return flt_list

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    medium_pi = "3.1415926535897932384626433832795028841971693993751058209749445923078164"
    long_pi = "3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165271201909145648566923460348610454326648213393607260249141273724587006606315588174881520920962829254091715364367892590360011330530548820466521384146951941511609433057270365759591953092186117381932611793105118548074462379962749567351885752724891227938183011949129833673362440656643086021394946395224737190"
    connection_list, word_histogram = generate_connection_histogram(sanitize_float(0))
    pygame.init()
    size = (900, 1000)
    screen = pygame.display.set_mode(size)

    model = CirclePlotModel(word_histogram, connection_list)
    view = CirclePlotView(model, screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        view.draw()
        time.sleep(.001)