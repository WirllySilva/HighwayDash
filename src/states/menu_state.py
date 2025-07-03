import pygame
from states.game_state import GameState
from core.event_manager import EventManager


class MenuState:
    def __init__(self, game):
        """
        Represents the main menu screen with background, moving clouds, music and sound effects.
        """
        self.game = game
        self.event_manager = EventManager()

        # Fonts
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)

        # Background and clouds
        self.bg_image = pygame.image.load("assets/images/background-menu.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (480, 640))
        self.cloud_img = pygame.image.load("assets/images/clouds.png").convert_alpha()
        self.cloud_img = pygame.transform.scale(self.cloud_img, (480, 300))

        self.cloud_x = 0

        # Available game modes
        self.modes = ["Endurance", "Classic"]
        self.selected_mode_index = 0

        # Buttons
        self.buttons = [
            "START GAME",
            f"CHOOSE MODE ({self.modes[self.selected_mode_index]})",
            "EXIT"
        ]
        self.selected_index = 0
        self.button_width = 280
        self.button_height = 60
        self.button_rects = []

        start_y = 280
        spacing = 80

        for i in range(len(self.buttons)):
            x = (480 - self.button_width) // 2
            y = start_y + i * spacing
            rect = pygame.Rect(x, y, self.button_width, self.button_height)
            self.button_rects.append(rect)

        # Sound effects
        pygame.mixer.music.load("assets/sounds/menu-sound.mp3")
        pygame.mixer.music.play(-1)

        self.option_sound = pygame.mixer.Sound("assets/sounds/menubutton-option.mp3")
        self.selection_sound = pygame.mixer.Sound("assets/sounds/button-selection.mp3")
        self.start_sound = pygame.mixer.Sound("assets/sounds/starting-sound.mp3")

        # Subscribe sound methods to event manager
        self.event_manager.subscribe("NAVIGATION", self.play_navigation_sound)
        self.event_manager.subscribe("SELECTION", self.play_selection_sound)
        self.event_manager.subscribe("START_GAME", self.play_start_sound)

    def handle_events(self, events):
        """
        Handles user input for menu navigation and selection.
        """
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.buttons)
                    self.event_manager.notify("NAVIGATION")

                elif event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.buttons)
                    self.event_manager.notify("NAVIGATION")

                elif event.key == pygame.K_RETURN:
                    selected_option = self.buttons[self.selected_index]
                    if self.selected_index != 1:
                        self.event_manager.notify("SELECTION")

                    if selected_option == "START GAME":
                        self.event_manager.notify("START_GAME")
                        from states.game_state import GameState
                        game_mode = self.modes[self.selected_mode_index]
                        self.game.change_state(GameState(self.game, game_mode))

                    elif self.selected_index == 1:  # CHOOSE MODE
                        # Toggle mode with Enter
                        self.selected_mode_index = (self.selected_mode_index + 1) % len(self.modes)
                        self.update_mode_text()
                        self.event_manager.notify("NAVIGATION")

                    elif selected_option.startswith("EXIT"):
                        pygame.quit()
                        exit()

                elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    if self.selected_index == 1:
                        if event.key == pygame.K_RIGHT:
                            self.selected_mode_index = (self.selected_mode_index + 1) % len(self.modes)
                        else:
                            self.selected_mode_index = (self.selected_mode_index - 1) % len(self.modes)
                        self.update_mode_text()
                        self.event_manager.notify("NAVIGATION")

    def update_mode_text(self):
        self.buttons[1] = f"CHOOSE MODE ({self.modes[self.selected_mode_index]})"

    def update(self):
        """
        Updates the clouds' horizontal movement for parallax effect.
        """
        self.cloud_x -= 0.2
        if self.cloud_x <= -self.cloud_img.get_width():
            self.cloud_x = 0

    def render(self, screen):
        """
        Draws the full menu interface with background, clouds and buttons.
        """
        # Background
        screen.blit(self.bg_image, (0, 0))

        # Moving clouds
        screen.blit(self.cloud_img, (self.cloud_x, 0))
        screen.blit(self.cloud_img, (self.cloud_x + self.cloud_img.get_width(), 0))

        # Buttons
        for i, rect in enumerate(self.button_rects):
            pygame.draw.rect(screen, (255, 255, 255) if i == self.selected_index else (0, 0, 0), rect, border_radius=12)
            pygame.draw.rect(screen, (0, 200, 0), rect, width=2, border_radius=12)

            if i == 1:  # CHOOSE MODE
                # Tittle
                top_label = self.font.render("CHOOSE MODE", True, (0, 200, 0))
                top_rect = top_label.get_rect(center=(rect.centerx, rect.centery - 12))

                # Current mode
                small_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 14)
                mode_label = small_font.render(f"({self.modes[self.selected_mode_index]})", True, (0, 200, 0))
                mode_rect = mode_label.get_rect(center=(rect.centerx, rect.centery + 12))

                screen.blit(top_label, top_rect)
                screen.blit(mode_label, mode_rect)
            else:
                label = self.font.render(self.buttons[i], True, (0, 200, 0))
                label_rect = label.get_rect(center=rect.center)
                screen.blit(label, label_rect)

    # --- Event handlers for Observer ---
    def play_navigation_sound(self, _=None):
        self.option_sound.play()

    def play_selection_sound(self, _=None):
        self.selection_sound.play()

    def play_start_sound(self, _=None):
        self.start_sound.play()
