import pygame
from src.states.menu_state import MenuState
from src.states.game_state import GameState

class DemoNoticeState:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 16)
        self.small_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 14)

        # Load background image
        self.bg_image = pygame.image.load("assets/images/background-menu.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (480, 640))

        # The clouds
        self.cloud_img = pygame.image.load("assets/images/clouds.png").convert_alpha()
        self.cloud_x = 0
        self.cloud_speed = 1

        self.options = ["BACK TO MENU", "PLAY ENDURANCE MODE"]
        self.selected = 0

        self.button_width = 400
        self.button_height = 50
        self.button_rects = []

        start_y = 380
        spacing = 70
        for i in range(len(self.options)):
            x = (480 - self.button_width) // 2
            y = start_y + i * spacing
            rect = pygame.Rect(x, y, self.button_width, self.button_height)
            self.button_rects.append(rect)

        self.option_sound = pygame.mixer.Sound("assets/sounds/menubutton-option.mp3")
        self.selection_sound = pygame.mixer.Sound("assets/sounds/button-selection.mp3")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                    self.option_sound.play()

                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                    self.option_sound.play()

                elif event.key == pygame.K_RETURN:
                    self.selection_sound.play()
                    if self.selected == 0:
                        self.game.change_state(MenuState(self.game))
                    else:
                        self.game.change_state(GameState(self.game, "Endurance"))

    def update(self):
        self.cloud_x -= self.cloud_speed
        if self.cloud_x <= -self.cloud_img.get_width():
            self.cloud_x = 0


    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))  # Draw background like menu background
        screen.blit(self.cloud_img, (self.cloud_x, 0)) # The moving clouds
        screen.blit(self.cloud_img, (self.cloud_x + self.cloud_img.get_width(), 0))

        # Render outline for messages
        self.draw_text_with_outline(screen, "This mode is not available", (240, 160), self.font, (255, 255, 255))
        self.draw_text_with_outline(screen, "in the demo version.", (240, 200), self.font, (255, 255, 255))


        for i, rect in enumerate(self.button_rects):
            color = (255, 255, 255) if i == self.selected else (0, 0, 0)
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (0, 200, 0), rect, 2, border_radius=10)

            label = self.small_font.render(self.options[i], False, (0, 200, 0))
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)

    def draw_text_with_outline(self, screen, text, center, font, text_color, outline_color=(0, 0, 0)):
        x, y = center
        text_surface = font.render(text, False, text_color)
        outline_surface = font.render(text, False, outline_color)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    screen.blit(outline_surface, (x + dx - text_surface.get_width() // 2,
                                                  y + dy - text_surface.get_height() // 2))
        screen.blit(text_surface, (x - text_surface.get_width() // 2, y - text_surface.get_height() // 2))
