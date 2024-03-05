import pygame
import math
import random

class gamecamera:
    def __init__(self,screen):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.render_x = 0
        self.render_y = 0
    def updatecamerapos(self,player):
        self.x += (player.x - self.x)/5
        self.y += (player.y - self.y)/5
        self.render_x = self.x - self.screen.get_size()[0]/2
        self.render_y = self.y - self.screen.get_size()[1]/2
    def rendergame(self,player,rects):
        self.updatecamerapos(player)
        player.updatescreenpos(self)
        pygame.draw.ellipse(self.screen,(55,255,55),player.sprite)
        for rect in rects:
            rect.updatescreenpos(self)
            pygame.draw.rect(self.screen,(0,0,0),rect.sprite)

class collisionchecker:
    def __init__(self,size):
        self.collider = pygame.Rect(0,0,size,size)
    def checkcollision(self, x, y, walls, camera):
        self.collider.x = x - camera.render_x
        self.collider.y = y - camera.render_y
        for wall in walls:
            if self.collider.colliderect(wall.sprite):
                if self.collider.bottom > wall.sprite.top and self.collider.top < wall.sprite.bottom:
                    return True
        return False
    

class gameplayer:
    def __init__(self):
        self.speed = 3
        self.movement_x = 0
        self.movement_y = 0
        self.x = 0
        self.y = 0
        self.size_x = 20
        self.size_y = 20
        self.sprite = pygame.Rect(0,0,20,20)
        self.collider_x = collisionchecker(self.size_x)
        self.collider_y = collisionchecker(self.size_x)
    def updatescreenpos(self,camera):
        self.sprite.x = self.x - camera.render_x
        self.sprite.y = self.y - camera.render_y
    def unstuck(self, walls, camera):
        col = False
        for wall in walls:
            if self.sprite.colliderect(wall.sprite):
                col = True
                break
        if col:
            original_x = self.x
            original_y = self.y

            for offset in range(1, self.speed + 1):
                self.x = original_x + offset if self.collider_x.checkcollision(original_x + offset, original_y, walls, camera) else original_x + offset
                if not self.collider_x.checkcollision(self.x, original_y, walls, camera):
                    return self.x,original_y
            
                self.x = original_x - offset if self.collider_x.checkcollision(original_x - offset, original_y, walls, camera) else original_x - offset
                if not self.collider_x.checkcollision(self.x, original_y, walls, camera):
                    return self.x, original_y
            
            for offset in range(1, self.speed + 1):
                self.y = original_y + offset if self.collider_y.checkcollision(original_x, original_y + offset, walls, camera) else original_y + offset
                if not self.collider_y.checkcollision(original_x, self.y, walls, camera):
                    return original_x, self.y
            
                self.y = original_y - offset if self.collider_y.checkcollision(original_x, original_y - offset, walls, camera) else original_y - offset
                if not self.collider_y.checkcollision(original_x, self.y, walls, camera):
                    return original_x, self.y
            self.x = original_x
            self.y = original_y
        return self.x,self.y

    def handlemovement(self, up, down, left, right, walls, camera):
        self.movement_x = int(right) - int(left)
        self.movement_y = int(down) - int(up)
        if self.movement_x != 0 and self.movement_y != 0:
            self.movement_x = 0.707 * self.movement_x
            self.movement_y = 0.707 * self.movement_y


        if self.movement_x != 0:
            for iter in range(self.speed):
                if not self.collider_x.checkcollision(self.x + self.movement_x, self.y, walls, camera):
                    self.x += self.movement_x
                else:
                    break

                
        
        if self.movement_y != 0:
            for iter in range(self.speed):
                if not self.collider_y.checkcollision(self.x, self.y + self.movement_y, walls, camera):
                    self.y += self.movement_y
                else:
                    break
        
        self.x,self.y = self.unstuck(walls,camera)
        
        self.updatescreenpos(camera)
        
class collider:
    def __init__(self,x,y,size):
        self.x = x
        self.y = y
        self.sprite = pygame.Rect(x,y,size,size)
    def updatescreenpos(self,camera):
        self.sprite.x = self.x - camera.render_x
        self.sprite.y = self.y - camera.render_y

class wallcollider:
    def __init__(self):
        self.boxsize = 30
        self.colliders = []
        for i in range(20):
            for j in range(20):
                if random.randint(1,3) == 1:
                    self.colliders.append(collider(i*30+20,j*30+20,self.boxsize))
