import random

import pygame

class Obstacle:
    def __init__(self, path, x):
        self.image = pygame.image.load(path).convert_alpha()

        # Resize individually based on file name
        filename = path.split("/")[-1]

        if filename == "damaged-track.png":
            self.image = pygame.transform.scale(self.image, (50, 50))
        elif filename == "oil-barrel.png":
            self.image = pygame.transform.scale(self.image, (40, 60))
        elif filename == "rock.png":
            self.image = pygame.transform.scale(self.image, (45, 50))
        elif filename == "traffic-cone.png":
            self.image = pygame.transform.scale(self.image, (28, 40))
        elif filename == "traffic-easel.png":
            self.image = pygame.transform.scale(self.image, (35, 45))
        else:
            self.image = pygame.transform.scale(self.image, (40, 40))  # default

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = -random.randint(self.rect.height + 20, self.rect.height + 100)

    def update(self, speed):
        self.rect.y += speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_off_screen(self):
        return self.rect.top > 640
