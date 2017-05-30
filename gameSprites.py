from gameUtils import collide_edges, loadImage
from config import *
import pygame
# ----------------------------------------------------

class Mario(pygame.sprite.Sprite):

    def __init__(self, screen, enemies):

        pygame.sprite.Sprite.__init__(self)

        self.enemies = enemies
        image, rect = loadImage('mario.png', -1)
        imagerun, rect = loadImage('mario_run.png', -1)
        self.stand = pygame.transform.scale2x(image).convert()
        self.run = pygame.transform.scale2x(imagerun).convert()
        self.standL = pygame.transform.flip(self.stand, 1, 0).convert()
        self.runL = pygame.transform.flip(self.run, 1, 0).convert()
        self.image = self.stand
        self.rect = self.image.get_rect()
        self.area = screen.get_rect()
        self.rect.topleft = (250, 300)
        self.x_vel, self.y_vel = 0, 0
        self.jumping = False
        self.midair = True
        self.walkingRight = True
        self.running = False
        self.fireball_lock = False
        self.jump_count = 0
        self.score = 0
        self.isDead = False
        self.animTick = 0

    def update(self, actions):

        self.running = False

        # increase/decrease x_vel if left/right keys are being pressed
        # then reduce x_vel according to friction
        if actions[1] == 1:
#         if keys[pygame.K_RIGHT]:
            self.x_vel += MARIO_X_ACC
            self.walkingRight = True
            self.running = True
        if actions[2] == 1:
#         if keys[pygame.K_LEFT]:
            self.x_vel -= MARIO_X_ACC
            self.running = True
            self.walkingRight = False
        self.x_vel *= MARIO_FRICTION

        if self.midair:
            self.animTick = 0
            oldrect = self.rect
            self.image = self.run
            self.rect = self.image.get_rect()
            self.rect.midbottom = oldrect.midbottom
            if not self.walkingRight:
                self.image = self.runL
        elif not self.running:
            self.animTick = 0
            oldrect = self.rect
            self.image = self.stand
            self.rect = self.image.get_rect()
            self.rect.midbottom = oldrect.midbottom
            if not self.walkingRight:
                self.image = self.standL
        else:
            self.animTick += 1
            if self.animTick == 10:
                self.animTick = 0
                oldrect = self.rect
                if self.walkingRight:
                    if self.image == self.stand or self.image == self.standL:
                        self.image = self.run
                    else:
                        self.image = self.stand
                else:
                    if self.image == self.run or self.image == self.runL:
                        self.image = self.standL
                    else:
                        self.image = self.runL
                self.rect = self.image.get_rect()
                self.rect.midbottom = oldrect.midbottom

        # if jumping, set y_vel to jump velocity
#         if keys[pygame.K_SPACE] and not self.midair:
        if actions[2] == 1 and not self.midair:
            self.jump_count += 1
            self.midair = True
            self.y_vel = MARIO_JUMP_VEL

        # effect of gravity pulling Mario to earth
        self.y_vel += MARIO_GRAVITY

        # move Mario
        self.rect.move_ip((self.x_vel, self.y_vel))

        # if he jumps on top of a shell, shell dies and mario gets another point.
        # mario bounces of shell, shell falls off screen. If he hits shell otherwise,
        # game ends
        reward = 0
        already_rebounded = False
        for shell in self.enemies:
            if shell.rect.colliderect(self.rect):
                top, right, bottom, left = collide_edges(self.rect, shell.rect)
                if bottom:
                    if not already_rebounded:
                        self.y_vel *= -1
                        already_rebounded = True
                    shell.fall()
                    self.score += 1
                    reward = 1
                elif top:
                    reward = -1
                    self.isDead = True
                elif right:
                    reward = -1
                    self.isDead = True
                elif left:
                    reward = -1
                    self.isDead = True

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.area.width:
            self.rect.right = self.area.width

        if self.rect.bottom > self.area.height - 45:
            self.rect.bottom = self.area.height - 45
            self.y_vel = 0
            self.midair = False
        elif self.rect.top < 0:
            self.rect.top = 0

        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        return image_data, reward
class Shell(pygame.sprite.Sprite):

    image = None

    def __init__(self, screen, start_pos):

        pygame.sprite.Sprite.__init__(self)

        if Shell.image is None:
            tempimage, rect = loadImage("shell.png", -1)
            Shell.image = pygame.transform.scale2x(tempimage).convert()

        self.image = Shell.image
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.area = screen.get_rect()
        self.onGround = False
        self.falling = False

        self.vel_y = SHELL_Y_VEL
        self.vel_x = SHELL_X_VEL

        if start_pos[0] > self.area.width / 2:
            self.vel_x *= -1

    def fall(self):

        self.falling = True

    def update(self):

        self._move()

    def _move(self):

        # if the shell hasn't been jumped on
        if not self.falling:
            if not self.onGround:
                self.vel_y += SHELL_GRAVITY

            self.rect.move_ip((self.vel_x, self.vel_y))

            if self.rect.right < 0:
                self.kill()
            elif self.rect.left > self.area.width:
                self.kill()

            if self.rect.bottom >= self.area.height - 45:
                self.rect.bottom = self.area.height - 45
                self.vel_y = 0
                self.onGround = True

        # if the shell HAS been jumped on
        else:
            self.rect.move_ip((self.vel_x, 4))

            if self.rect.right < 0:
                self.kill()
            elif self.rect.left > self.area.width:
                self.kill()

            if self.rect.top > self.area.height:
                self.kill()

# ----------------------------------------------------
