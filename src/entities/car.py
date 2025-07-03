import pygame

class Car:
    def __init__(self):
        """
        Represents the player's car.
        """
        self.image = pygame.image.load("assets/images/yellow-car.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (52, 105))

        self.rect = self.image.get_rect()
        self.rect.centerx = 240  # center of 480px screen
        self.rect.bottom = 620   # near bottom of 640px screen

        self.speed = 5

    def move(self, direction):
        """
        Moves the car left or right.
        """
        if direction == "left":
            self.rect.x -= self.speed
        elif direction == "right":
            self.rect.x += self.speed

        # Keep inside screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 480:
            self.rect.right = 480

    def draw(self, screen):
        screen.blit(self.image, self.rect)
