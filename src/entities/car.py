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

            # Define horizontal limits of the road
        ROAD_LEFT = 98
        ROAD_RIGHT = 382
        ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT  # = 284px
        ALLOWED_OVERLAP = 2

        # Clamp position: allow slight overlap for visual effect
        min_left = ROAD_LEFT - ALLOWED_OVERLAP
        max_right = ROAD_RIGHT + ALLOWED_OVERLAP

        if self.rect.left < min_left:
            self.rect.left = min_left
        if self.rect.right > max_right:
            self.rect.right = max_right

    def draw(self, screen):
        screen.blit(self.image, self.rect)
