import pygame
from entities.car import Car
from entities.obstacle import Obstacle
from entities.enemy_vehicle import EnemyVehicle
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
        self.engine_channel = self.engine_sound.play(-1)  # loop forever

        # Font for HUD
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 14)

        # Distance control
        self.distance_km = 0
        self.km_per_frame = 0.05  # Adjust based on desired rate
        self.last_milestone = 0

        self.obstacles = []
        self.enemy_vehicles = []
        self.spawn_timer = 0
        self.spawn_interval = 1500  # ms

        self.lane_positions = self.get_lane_positions()
        self.lane_occupied = [False, False, False]

        self.explosion_img = pygame.image.load("assets/images/explosion.png").convert_alpha()
        self.explosion_img = pygame.transform.scale(self.explosion_img, (80, 80))  # ajuste conforme necessário

        self.crash_sound = pygame.mixer.Sound("assets/sounds/car-crash.mp3")

        # Explosion state control
        self.exploded = False
        self.explosion_timer = 0

    def get_lane_positions(self):
        return [168, 239, 312]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_SPACE]:
                    from states.pause_state import PauseState
                    self.game.change_state(PauseState(self.game, self))

        if self.exploded:
            return  # Do not allow movement if explosion occurred

        keys = pygame.key.get_pressed()
        if not self.exploded:
            if keys[pygame.K_LEFT]:
                self.car.move("left")
            elif keys[pygame.K_RIGHT]:
                self.car.move("right")
            elif keys[pygame.K_UP]:
                self.car.move("up")
            elif keys[pygame.K_DOWN]:
                self.car.move("down")

    def update(self):
        # Simple scrolling background effect
        if not self.exploded: # Stop track scroll after explosion
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
                if self.distance_km <= 200:
                    self.scroll_speed += 1

                # Increase spawn frequency after 60km
            if self.distance_km >= 60:
                self.spawn_interval = max(500, 1500 - int((self.distance_km - 60) * 10))


        ROAD_LEFT = 98
        ROAD_RIGHT = 382

        # Trigger game over if car is outside playable bounds
        GAMEOVER_LEFT = ROAD_LEFT + 5 # 103
        GAMEOVER_RIGHT = ROAD_RIGHT - 5 # 377

        if not self.exploded and (self.car.rect.left < GAMEOVER_LEFT or self.car.rect.right > GAMEOVER_RIGHT):
            self.trigger_explosion()

        # Update obstacles
        if not self.exploded:
            # Update obstacles
            for obstacle in self.obstacles[:]:
                obstacle.update(self.scroll_speed)
                if obstacle.is_off_screen():
                    self.obstacles.remove(obstacle)

            for vehicle in self.enemy_vehicles[:]:
                vehicle.update(self.scroll_speed)
                if vehicle.is_off_screen():
                    if vehicle.lane_index is not None:
                        self.lane_occupied[vehicle.lane_index] = False
                    self.enemy_vehicles.remove(vehicle)

            # Spawning
            self.spawn_timer += self.game.clock.get_time()
            if self.spawn_timer > self.spawn_interval:
                self.spawn_timer = 0
                self.spawn_random_entity()

        if not self.exploded:
            for obstacle in self.obstacles:
                if self.car.rect.colliderect(obstacle.rect):
                    self.trigger_explosion()

            for vehicle in self.enemy_vehicles:
                if self.car.rect.colliderect(vehicle.rect):
                    self.trigger_explosion()

        if self.exploded and pygame.time.get_ticks() - self.explosion_timer > 1000:
            from states.game_over_state import GameOverState
            self.game.change_state(GameOverState(self.game, self.game_mode, self.distance_km))

    def render(self, screen):
        screen.blit(self.current_track, (0, self.track_y - 640))
        screen.blit(self.next_track, (0, self.track_y))
        self.car.draw(screen)

        for obstacle in self.obstacles:
            obstacle.draw(screen)

        for vehicle in self.enemy_vehicles:
            vehicle.draw(screen)

        # HUD - show mode and distance
        mode_text = f"Mode: {self.game_mode}"
        distance_text = f"{self.distance_km:.1f} km"
        self.draw_text_with_outline(screen, mode_text, (8, 8), self.font, (255, 255, 255))
        self.draw_text_with_outline(screen, distance_text, (10, 35), self.font, (255, 255, 255))
        if self.distance_km >= 200:
            max_speed_text = "MAX SPEED!"
            self.draw_text_with_outline(screen, max_speed_text, (300, 10), self.font, (255, 255, 0))  # Amarelo vibrante

        if self.exploded:
            explosion_rect = self.explosion_img.get_rect(center=self.car.rect.center)
            explosion_rect.y -= 20  # ajusta para o capô
            screen.blit(self.explosion_img, explosion_rect)

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

    def spawn_random_entity(self):
        available_lanes = [i for i, occupied in enumerate(self.lane_occupied) if not occupied]
        if not available_lanes:
            return  # nenhuma faixa disponível

        lane_index = random.choice(available_lanes)
        lane_x = self.lane_positions[lane_index]

        if random.random() < 0.1:
            obstacle_file = random.choice([
                "damaged-track.png", "oil-barrel.png", "rock.png",
                "traffic-cone.png", "traffic-easel.png"
            ])
            path = f"assets/images/{obstacle_file}"
            self.obstacles.append(Obstacle(path, lane_x))
        else:
            vehicle_file = random.choice([
                "police-car.png", "red-car.png", "white-car.png", "truck.png"
            ])
            is_truck = vehicle_file == "truck.png"
            path = f"assets/images/{vehicle_file}"
            # The vehicles never have the same speed
            if len(self.enemy_vehicles) >= 2:
                # If you already have 2 vehicles on the track, make sure the new one has a higher speed
                base_speeds = [v.speed for v in self.enemy_vehicles if v.lane_index is not None]
                max_current_speed = max(base_speeds) if base_speeds else 2
                speed = max_current_speed + 1  # new car is more fast.
                speed = min(speed, 5)  # max limit of speed
            else:
                speed = self.get_unique_vehicle_speed()
                vehicle = EnemyVehicle(path, lane_x, is_truck, speed)
                self.enemy_vehicles.append(vehicle)
                self.lane_occupied[lane_index] = True  # mark the lane as busy lane
                vehicle.lane_index = lane_index  # save the used lane

    def trigger_explosion(self):
        self.exploded = True
        self.explosion_timer = pygame.time.get_ticks()
        pygame.mixer.stop()
        self.crash_sound.play()

    def get_unique_vehicle_speed(self):
        used_speeds = {v.speed for v in self.enemy_vehicles}
        possible_speeds = [1, 2, 3, 4, 5]

        available = [s for s in possible_speeds if s not in used_speeds]

        if available:
            return random.choice(available)
        else:
            return random.choice(possible_speeds)




