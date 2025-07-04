import pygame

class Car:
    def __init__(self):
        """
        Represents the player's car.
        """
        self.image = pygame.image.load("assets/images/yellow-car.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 93))

        self.rect = self.image.get_rect()
        self.rect.centerx = 240  # center of 480px screen
        self.rect.bottom = 620   # near bottom of 640px screen

        self.speed = 5

    def move(self, direction):
        """
            Moves the car in the specified direction.
            """
        if direction == "left":
            self.rect.x -= self.speed
        elif direction == "right":
            self.rect.x += self.speed
        elif direction == "up":
            self.rect.y -= self.speed
        elif direction == "down":
            self.rect.y += self.speed

        # Horizontal clamping (pista)
        ROAD_LEFT = 98
        ROAD_RIGHT = 382
        ALLOWED_OVERLAP = 14

        min_left = ROAD_LEFT - ALLOWED_OVERLAP
        max_right = ROAD_RIGHT + ALLOWED_OVERLAP
        if self.rect.left < min_left:
            self.rect.left = min_left
        if self.rect.right > max_right:
            self.rect.right = max_right

        # Vertical clamping (tela)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 640:
            self.rect.bottom = 640

    def draw(self, screen):
        screen.blit(self.image, self.rect)
