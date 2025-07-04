import pygame
from core.event_manager import EventManager
from states.game_state import GameState
from states.menu_state import MenuState

class PauseState:
    def __init__(self, game, previous_state):
        self.game = game
        self.previous_state = previous_state
        self.event_manager = EventManager()

        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)

        self.options = ["RESUME", "RESTART", "BACK TO MENU"]
        self.selected_index = 0

        self.button_width = 300
        self.button_height = 50
        self.button_rects = []

        start_y = 220
        spacing = 80
        for i in range(len(self.options)):
            x = (480 - self.button_width) // 2
            y = start_y + i * spacing
            rect = pygame.Rect(x, y, self.button_width, self.button_height)
            self.button_rects.append(rect)

        self.option_sound = pygame.mixer.Sound("assets/sounds/menubutton-option.mp3")
        self.selection_sound = pygame.mixer.Sound("assets/sounds/button-selection.mp3")
        self.restart_sound = pygame.mixer.Sound("assets/sounds/starting-sound.mp3")

        # Stop all sounds when the game is paused
        pygame.mixer.music.pause()
        if hasattr(previous_state, "engine_channel"):
            previous_state.engine_channel.pause()


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                    self.option_sound.play()

                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                    self.option_sound.play()

                elif event.key == pygame.K_RETURN:
                    self.selection_sound.play()
                    selected = self.options[self.selected_index]
                    if selected == "RESUME":
                        pygame.mixer.music.unpause()
                        if hasattr(self.previous_state, "engine_channel"):
                            self.previous_state.engine_channel.unpause()
                        self.game.change_state(self.previous_state)
                    elif selected == "RESTART":
                        self.restart_sound.play()
                        self.game.change_state(GameState(self.game, self.previous_state.game_mode))
                    elif selected == "BACK TO MENU":
                        self.game.change_state(MenuState(self.game))

                elif event.key in [pygame.K_ESCAPE, pygame.K_SPACE]:
                    self.resume_sound.play()
                    self.game.change_state(self.previous_state)
    # No update
    def update(self):
        pass

    def render(self, screen):
        self.previous_state.render(screen)  # draw paused screen as background overlay

        # Translucent overlay
        overlay = pygame.Surface((480, 640))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        for i, rect in enumerate(self.button_rects):
            color = (255, 255, 255) if i == self.selected_index else (0, 0, 0)
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (0, 200, 0), rect, 2, border_radius=10)

            label = self.font.render(self.options[i], False, (0, 200, 0))
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)
