import pygame
import random

class Obstacle:
    def __init__(self, image_path, lane_x):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 52))  # half car size
        self.rect = self.image.get_rect()
        self.rect.centerx = lane_x
        self.rect.y = -self.rect.height  # start off screen

    def update(self, speed):
        self.rect.y += speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_off_screen(self):
        return self.rect.top > 640  # screen height
