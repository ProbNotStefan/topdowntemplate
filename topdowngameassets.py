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
    def rendergame(self,camera,player,walls,floors):
        self.updatecamerapos(player)
        player.updatescreenpos(self)
        for rect in floors:
            rect.updatescreendata(walls,self,player)
            pygame.draw.rect(self.screen,rect.color,rect.sprite)
        pygame.draw.ellipse(self.screen,(55,255,55),player.sprite)
        for rect in walls:
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
            
            for offset in range(1, self.speed + 1):
                self.x = original_x + offset if self.collider_x.checkcollision(original_x + offset, original_y, walls, camera) else original_x + offset
                self.y = original_y + offset if self.collider_y.checkcollision(original_x, original_y + offset, walls, camera) else original_y + offset
                if not self.collider_y.checkcollision(original_x, self.y, walls, camera):
                    return self.x, self.y
                
                self.x = original_x - offset if self.collider_x.checkcollision(original_x + offset, original_y, walls, camera) else original_x + offset
                self.y = original_y - offset if self.collider_y.checkcollision(original_x, original_y - offset, walls, camera) else original_y - offset
                if not self.collider_y.checkcollision(original_x, self.y, walls, camera):
                    return self.x, self.y
            
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

class floorboard:
    def __init__(self,x,y,size):
        self.x = x
        self.y = y
        self.color = (255,255,55)
        self.size = size
        self.sprite = pygame.Rect(x,y,size,size)
        self.colcheck = collisionchecker(1)
    def updatescreendata(self, walls, camera, player):
        self.color = pygame.Color(255, 255, 55)
        self.sprite.x = self.x - camera.render_x
        self.sprite.y = self.y - camera.render_y
        dif_x = player.x - self.x
        dif_y = player.y - self.y
        distance = math.sqrt(dif_x ** 2 + dif_y ** 2)
        if distance < 200:
            for index in range(1, math.floor(distance/(self.size)) + 1):
                ratio = index * 30 / distance 
                pos_x = self.x+self.size/2 + dif_x * ratio
                pos_y = self.y+self.size/2 + dif_y * ratio
                if self.colcheck.checkcollision(pos_x, pos_y, walls, camera):
                    self.color = pygame.Color(max(0,int(60-distance/3)), max(0,int(60-distance/3)), 0)
                    break
                else:
                    self.color -= pygame.Color(40, 40, 40)
        else:
            self.color = (0, 0, 0)

class wallcollider:
    def __init__(self):
        self.boxsize = 30
        self.boundsize=30
        self.colliders = []
        self.floors = []
        cords = [[16,16]]
        for i in range(self.boundsize):
            for j in range(self.boundsize):
                if i == 0 or i == self.boundsize-1 or j == 0 or j == self.boundsize-1 or [i,j] in cords:
                    self.colliders.append(collider(i*self.boxsize-self.boxsize*self.boundsize/2,j*self.boxsize-self.boxsize*self.boundsize/2,self.boxsize))
                else:
                    if random.randint(1,3) == 1:
                        if [i,j] not in cords:
                            self.colliders.append(collider(i*self.boxsize-self.boxsize*self.boundsize/2,j*self.boxsize-self.boxsize*self.boundsize/2,self.boxsize))
                    else:
                        self.floors.append(floorboard(i*self.boxsize-self.boxsize*self.boundsize/2,j*self.boxsize-self.boxsize*self.boundsize/2,self.boxsize))