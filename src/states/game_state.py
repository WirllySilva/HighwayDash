import pygame
from entities.car import Car

class GameState:
    def __init__(self, game):
        """
        Handles the main gameplay state.
        """
        self.game = game
        self.car = Car()

        # Load background (optional track image or plain color)
        self.track = pygame.Surface((480, 640))
        self.track.fill((50, 50, 50))  # temporary visual background
        self.track_y = 0

        # Stop menu music
        pygame.mixer.music.stop()

        # Start race background music
        pygame.mixer.music.load("assets/sounds/race-song.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        # Load and play engine sound
        self.engine_sound = pygame.mixer.Sound("assets/sounds/car-engine.mp3")
        self.engine_sound.set_volume(0.6)
        self.engine_sound.play(-1)  # loop forever

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Stop engine sound before returning
                    self.engine_sound.stop()

                    from states.menu_state import MenuState
                    self.game.change_state(MenuState(self.game))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.car.move("left")
        elif keys[pygame.K_RIGHT]:
            self.car.move("right")

    def update(self):
        # Simple scrolling background effect
        self.track_y += 3
        if self.track_y >= 640:
            self.track_y = 0

    def render(self, screen):
        screen.blit(self.track, (0, self.track_y - 640))
        screen.blit(self.track, (0, self.track_y))

        self.car.draw(screen)
