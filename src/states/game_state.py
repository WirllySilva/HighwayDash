import pygame
from entities.car import Car
import random

class GameState:
    def __init__(self, game, game_mode):
        """
        Handles the main gameplay state.
        """
        self.game = game
        self.game_mode = game_mode # "Endurance" or "Classic"

        self.car = Car()
        self.track_y = 0
        self.scroll_speed = 3

        # Load and scale the track images
        self.tracks = [
            pygame.image.load("assets/images/track-01.png").convert(),
            pygame.image.load("assets/images/track-02.png").convert()
        ]
        self.tracks = [pygame.transform.scale(t, (480, 640)) for t in self.tracks]

        self.current_track = random.choice(self.tracks)
        self.next_track = random.choice(self.tracks)

        # Stop menu music
        pygame.mixer.music.stop()

        # Start race background music
        pygame.mixer.music.load("assets/sounds/race-song.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        # Load and play engine sound
        self.engine_sound = pygame.mixer.Sound("assets/sounds/car-engine.ogg")
        self.engine_sound.set_volume(0.6)
        self.engine_sound.play(-1)  # loop forever

        # Font for HUD
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 14)

        # Distance control
        self.distance_km = 0
        self.km_per_frame = 0.05  # Adjust based on desired rate
        self.last_milestone = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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
        self.track_y += self.scroll_speed
        if self.track_y >= 640:
            self.track_y = 0
            self.current_track = self.next_track
            self.next_track = random.choice(self.tracks)

            # Update distance
        if self.game_mode == "Endurance":
            self.distance_km += self.km_per_frame
            if int(self.distance_km) >= self.last_milestone + 20:
                self.last_milestone = int(self.distance_km)
                self.scroll_speed += 1  # Increase speed every 20km
                # You can also increase obstacle speed here in future


    def render(self, screen):
        screen.blit(self.current_track, (0, self.track_y - 640))
        screen.blit(self.next_track, (0, self.track_y))
        self.car.draw(screen)

        # HUD - show mode and distance
        mode_text = f"Mode: {self.game_mode}"
        distance_text = f"{self.distance_km:.1f} km"
        self.draw_text_with_outline(screen, mode_text, (8, 8), self.font, (255, 255, 255))
        self.draw_text_with_outline(screen, distance_text, (10, 35), self.font, (255, 255, 255))

    def draw_text_with_outline(self, screen, text, pos, font, text_color, outline_color=(0, 0, 0)):
        x, y = pos
        # Draw the outline at eight directions around
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    outline = font.render(text, False, outline_color)
                    screen.blit(outline, (x + dx, y + dy))
        # Current text
        label = font.render(text, False, text_color)
        screen.blit(label, (x, y))
