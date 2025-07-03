import pygame
from states.menu_state import MenuState
from states.game_state import GameState
from core.event_manager import EventManager

class GameOverState:
    def __init__(self, game, mode):
        self.game = game
        self.mode = mode
        self.event_manager = EventManager()

        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 30)
        self.small_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 18)
        self.restart_sound = pygame.mixer.Sound("assets/sounds/starting-sound.mp3")

        self.options = ["RESTART", "BACK TO MENU"]
        self.selected = 0
        self.show_options = False
        self.elapsed_time = 0

        # Background, the same of the game_pause
        self.background = pygame.image.load("assets/images/track-01.png").convert()
        self.background = pygame.transform.scale(self.background, (480, 640))

        # Buttons in the center
        self.button_width = 340
        self.button_height = 50
        self.button_rects = []

        start_y = 330
        spacing = 80
        for i in range(len(self.options)):
            x = (480 - self.button_width) // 2
            y = start_y + i * spacing
            rect = pygame.Rect(x, y, self.button_width, self.button_height)
            self.button_rects.append(rect)

        # No sounds after gameover
        pygame.mixer.stop()
        pygame.mixer.music.stop()

    def handle_events(self, events):
        if not self.show_options:
            return

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.options[self.selected] == "RESTART":
                        self.restart_sound.play()
                        self.game.change_state(GameState(self.game, self.mode))
                    else:
                        self.game.change_state(MenuState(self.game))

    def update(self):
        if not self.show_options:
            self.elapsed_time += self.game.clock.get_time()
            if self.elapsed_time > 2000:  # 2 seconds
                self.show_options = True

    def draw_text_with_outline(self, screen, text, pos, font, text_color, outline_color=(0, 0, 0)):
        x, y = pos
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    outline = font.render(text, False, outline_color)
                    screen.blit(outline, (x + dx, y + dy))
        label = font.render(text, False, text_color)
        screen.blit(label, (x, y))

    def render(self, screen):
        # background freeze
        screen.blit(self.background, (0, 0))

        # Game over text in the center
        text = "GAME OVER"
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(480 // 2, 240))
        self.draw_text_with_outline(screen, text, (text_rect.x, text_rect.y), self.font, (255, 255, 255))

        # after 2 seconds the buttons apear
        if self.show_options:
            for i, rect in enumerate(self.button_rects):
                color = (255, 255, 255) if i == self.selected else (0, 0, 0)
                pygame.draw.rect(screen, color, rect, border_radius=10)
                pygame.draw.rect(screen, (0, 200, 0), rect, 2, border_radius=10)

                label = self.small_font.render(self.options[i], False, (0, 200, 0))
                label_rect = label.get_rect(center=rect.center)
                screen.blit(label, label_rect)