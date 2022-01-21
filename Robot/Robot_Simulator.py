# https://rmgi.blog/pygame-2d-car-tutorial.html for reference

import os
from math import sin, radians, degrees, copysign

import pygame
from pygame.math import Vector2

class Car:
    def __init__(self, x, y, angle=0.0, length=4, max_steering=45, max_acceleration=5.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering

        self.acceleration = 0.0
        self.steering = 0.0
