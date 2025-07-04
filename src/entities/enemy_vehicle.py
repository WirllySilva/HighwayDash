import pygame

class EnemyVehicle:
    def __init__(self, image_path, lane_x, is_truck=False, speed=2):
        """
        Represents an enemy vehicle on the road.
        """
        self.image = pygame.image.load(image_path).convert_alpha()

        if is_truck:
            self.image = pygame.transform.scale(self.image, (50, 140))
        else:
            self.image = pygame.transform.scale(self.image, (40, 93))

        self.rect = self.image.get_rect()
        self.rect.centerx = lane_x
        self.rect.bottom = -10
        self.speed = speed
        self.lane_index = None

    def update(self, scroll_speed):
        """
        Updates the enemy vehicle position based on scroll speed + its own speed.
        """
        self.rect.y += scroll_speed - self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_off_screen(self):
        """
        Checks if the vehicle has gone beyond the screen height.
        """
        return self.rect.top > 640
