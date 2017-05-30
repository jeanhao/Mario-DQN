from pygame.locals import *
from gameSprites import Mario, Shell
from config import *
import cv2
import numpy as np
from BrainDQN_Nature import BrainDQN
import pygame
from gameUtils import loadImage
import random
# ----------------------------------------------------

class Game():

    def __init__(self):
        self.init()

    def checkEnemy(self):

        self.enemycounter -= 1

        if self.enemycounter == 0:
            self.enemycounter = random.choice(ENEMY_TICKS)
            start_pos = (random.choice(ENEMY_X_POS), random.choice(ENEMY_Y_POS))
            self.enemies.add(Shell(self.screen, start_pos))

    def renderStats(self):
        FONT = pygame.font.Font(None, 36)

        scoreline = FONT.render("Score: " + str(self.mario.score), True, TEXT_COLOR)
        scorepos = scoreline.get_rect(centerx=(self.background.get_width() / 5) * 4,)

        self.screen.blit(self.background, (0, 0))
        self.background.blit(scoreline, scorepos)


    def init(self):
        self.enemycounter = 10
        # initialize main pygame stuff
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Mario Shell Defense")

        # set up background
#         self.background = pygame.Surface(self.screen.get_size()).convert()
#         self.background.fill((0, 0, 0))
        bg, rect = loadImage("background.jpg")
        self.background_orig = pygame.transform.scale2x(bg).convert()
        self.background = pygame.transform.scale2x(bg).convert()
#         self.background_orig, _ = loadImage("background.jpg")
#         self.background, _ = loadImage("background.jpg")

        # set up sprites
        self.enemies = pygame.sprite.RenderClear()
        self.hero = pygame.sprite.RenderClear()
        self.mario = Mario(self.screen, self.enemies)
        self.hero.add(self.mario)

    def frame_step(self, actions):
        self.clock.tick(FRAMERATE)
        self.checkEnemy()

        image_data, reward = self.mario.update(actions)

        self.enemies.update()

        if not TRAIN:
            self.renderStats()
            self.hero.clear(self.screen, self.background)
            self.enemies.clear(self.screen, self.background)

            self.hero.draw(self.screen)
            self.enemies.draw(self.screen)

            pygame.display.flip()
        return image_data, reward

# ----------------------------------------------------

def preprocess(observation):
#     observation = cv2.resize(observation, (IMG_WIDTH, IMG_HEIGHT))
    observation = cv2.resize(observation, (IMG_HEIGHT, IMG_WIDTH))
    observation = cv2.cvtColor(observation, cv2.COLOR_BGR2GRAY)
    return np.reshape(observation, (IMG_WIDTH, IMG_HEIGHT, 1))

def train():

    actions = 4
    brain = BrainDQN(actions)

    while True:
        game = Game()
        # main game loop
        pygame.event.pump()

        action0 = np.array([1, 0, 0, 0])  # do nothing
#             HERO.update(action0)

        observation0, _ = game.frame_step(action0)
        observation0 = cv2.resize(observation0, (IMG_HEIGHT, IMG_WIDTH))
        observation0 = cv2.cvtColor(observation0, cv2.COLOR_BGR2GRAY)

        brain.setInitState(observation0)

        while True:
            action = brain.getAction()
            nextObservation, reward = game.frame_step(action)
            nextObservation = preprocess(nextObservation)
            brain.setPerception(nextObservation, action, reward)
            if reward == -1:
                break


if __name__ == "__main__":
    train()
    pygame.quit()
