import glm
import math
import pygame as pg

class Camera:
    def __init__(self, pos=(0,0,3), front=(0,0,-1), up=(0,1,0)):
        self.position = glm.vec3(pos)
        self.front = glm.vec3(front)
        self.up = glm.vec3(up)
        self.speed = 0.005
        self.sensitivity = 0.1
        self.first_mouse = True
        self.last_x = 0
        self.last_y = 0
        self.yaw = -90
        self.pitch = 0

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.front, self.up)

    def process_keyboard(self, keys, deltaT):
        if keys[pg.K_w]:
            self.position += self.speed * self.front * deltaT
        if keys[pg.K_s]:
            self.position -= self.speed * self.front * deltaT
        if keys[pg.K_a]:
            self.position -= glm.normalize(glm.cross(self.front, self.up)) * self.speed * deltaT
        if keys[pg.K_d]:
            self.position += glm.normalize(glm.cross(self.front, self.up)) * self.speed * deltaT

    def process_mouse(self, xpos, ypos):
        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False
        
        # Calculate mouse movement
        xoffset = xpos - self.last_x
        yoffset = self.last_y - ypos
        self.last_x = xpos
        self.last_y = ypos
        
        # Apply sensitivity
        xoffset *= self.sensitivity
        yoffset *= self.sensitivity
        
        print(xoffset, yoffset)
        
        # Update rotation angles
        self.yaw += xoffset  # Allow continuous horizontal rotation
        self.pitch = max(-89.0, min(89.0, self.pitch + yoffset))  # Limit vertical rotation
        
        # Calculate direction vector
        direction = glm.vec3()
        direction.x = math.cos(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        direction.y = math.sin(glm.radians(self.pitch))
        direction.z = math.sin(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        
        # Update camera front vector
        self.front = glm.normalize(direction)