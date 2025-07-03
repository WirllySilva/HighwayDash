import pygame

class EnemyVehicle:
    def __init__(self, image_path, lane_x, is_truck=False):
        """
        Represents an enemy vehicle on the road.
        """
        self.image = pygame.image.load(image_path).convert_alpha()

        if is_truck:
            self.image = pygame.transform.scale(self.image, (110, 140))
            self.speed = -1
        else:
            self.image = pygame.transform.scale(self.image, (52, 105))
            self.speed = -3

        self.rect = self.image.get_rect()
        self.rect.x = lane_x - self.rect.width // 2
        self.rect.y = -self.rect.height

    def update(self, scroll_speed):
        """
        Updates the enemy vehicle position based on scroll speed + its own speed.
        """
        self.rect.y += scroll_speed + self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_off_screen(self):
        """
        Checks if the vehicle has gone beyond the screen height.
        """
        return self.rect.top > 640
