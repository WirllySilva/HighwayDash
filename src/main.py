import pygame
from states.menu_state import MenuState

class Game:
    def __init__(self):
        """
        Initializes the Pygame window and game state.
        """
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((480, 640))
        pygame.display.set_caption("Highway Dash")

        self.clock = pygame.time.Clock()
        self.state = MenuState(self)

    def change_state(self, new_state):
        """
        Changes the current game state.
        """
        self.state = new_state

    def run(self):
        """
        Main game loop that runs the current game state.
        """
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            self.state.handle_events(events)
            self.state.update()
            self.state.render(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
