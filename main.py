import random
import time
import pygame
pygame.init()

# Window setup
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TITLE = "Package Peril"
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(TITLE)

# Self-explanatory
FONT = pygame.font.Font("assets/fonts/Bungee-Regular.ttf", 24)
TEXT_OFFSET_FROM_SCREEN = 16

# Fixed update system
# I'm doing my own fixed update system because for some reason that I don't exactly understand I get 
# smoother movement of the boxes using this system rather than using the built in one? It still has
# occasional jitters but for the most part it looks smooth.
FPS = 144  # Doing 144 instead of standard 60 because that's what my monitor runs at.
game_update_rate = 1 / FPS
accumulator = 0
previous_time = time.time()

# Define useful colors
BACKGROUND_COLOR = (50, 50, 50)
FLOOR_COLOR = (25, 25, 25)
TEXT_COLOR = (255, 255, 255)

# Utility functions
def get_delta_time():
    global previous_time
    current_time = time.time()
    delta_time = current_time - previous_time
    previous_time = current_time
    return delta_time

def get_fixed_delta_time():
    return 1 / FPS

# Define game classes
class Player():
    WIDTH, HEIGHT = 64, 64
    JUMP_FORCE = 10
    GRAVITY_FORCE = 35

    def __init__(self, left, top):
        self.sprite = pygame.image.load("assets/sprites/square_box.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.WIDTH, self.HEIGHT))

        self.rect = self.sprite.get_rect()
        self.rect.left = left
        self.rect.top = top

        self.is_grounded = True
        self.has_been_hit = False
        
        self.y_velocity = 0
        
        self.score = 1

    def check_for_ground(self):
        if self.rect.bottom - self.y_velocity > floor.top:
            self.rect.bottom = floor.top
            self.y_velocity = 0
            return True
        
        return False

    def jump(self):
        self.is_grounded = False
        self.y_velocity += self.JUMP_FORCE

    def update(self):
        if self.has_been_hit: return

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE] and self.is_grounded: self.jump() 

        self.y_velocity -= self.GRAVITY_FORCE * get_fixed_delta_time()
        self.is_grounded = self.check_for_ground()
        if not self.is_grounded: self.rect.top -= self.y_velocity 

class Box():
    # Initializes the box with default values so that the method in the BoxHandler can customize the box
    def __init__(self, speed):
        self.sprite = None
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.speed = speed

        self.can_add_to_score = True

    def update(self):
        if player.has_been_hit: return  

        self.rect.left -= self.speed
        if self.rect.left < -self.rect.width: 
            player.score += 1
            boxHandler.spawn_box()
            boxHandler.boxes.remove(self)

class BoxHandler():
    BOX_BASE_SPEED = 5
    BOX_MAX_SPEED = 15
    SPEED_CHANGE_FREQUENCY = 5

    def __init__(self):
        self.boxes = []
        self.current_box_speed = self.BOX_BASE_SPEED
        self.boxes_since_frequency_changed = 0 
        self.times_speed_changed = 0

    def calculate_boxes_until_speed_change(self):
        return self.SPEED_CHANGE_FREQUENCY - self.boxes_since_frequency_changed

    def spawn_box(self):
        self.boxes_since_frequency_changed += 1
        if self.boxes_since_frequency_changed >= self.SPEED_CHANGE_FREQUENCY:
            self.times_speed_changed += 1
            self.boxes_since_frequency_changed = 0
            self.current_box_speed = self.BOX_MAX_SPEED * (self.times_speed_changed / (self.times_speed_changed + self.BOX_MAX_SPEED)) + self.BOX_BASE_SPEED  # 10 is an arbitrary number
 
        box_type = random.randint(1, 4)
        newBox = Box(self.current_box_speed)

        match box_type:
            # Medium box
            case 1:
                newBox.rect.width = 96
                newBox.rect.height = 96
                newBox.sprite = pygame.image.load("assets/sprites/square_box.png")
            # Big box
            case 2:
                newBox.rect.width = 128
                newBox.rect.height = 128
                newBox.sprite = pygame.image.load("assets/sprites/square_box.png")

            # Tall box
            case 3: 
                newBox.rect.width = 64
                newBox.rect.height = 128
                newBox.sprite = pygame.image.load("assets/sprites/tall_box.png")

            # Long box
            case 4:
                newBox.rect.width = 160
                newBox.rect.height = 64
                newBox.sprite = pygame.image.load("assets/sprites/long_box.png")
        
        newBox.sprite = pygame.transform.scale(newBox.sprite, (newBox.rect.width, newBox.rect.height))
        newBox.rect.left = WINDOW_WIDTH
        newBox.rect.top = floor.top - newBox.rect.height
        self.boxes.append(newBox)

# Set up game objects
floor = pygame.Rect(0, WINDOW_HEIGHT - 150, WINDOW_WIDTH, 150)

player = Player(125, floor.top - Player.HEIGHT)

boxHandler = BoxHandler()
boxHandler.spawn_box()

# Game functions
def draw_scene():
    window.fill(BACKGROUND_COLOR)
    pygame.draw.rect(window, FLOOR_COLOR, floor)

def draw_UI():
    score_text = FONT.render(f"Score: {player.score}", True, TEXT_COLOR)
    window.blit(score_text, (TEXT_OFFSET_FROM_SCREEN, TEXT_OFFSET_FROM_SCREEN))

    speed_increase_text = FONT.render(f"Boxes until speed increase: {boxHandler.calculate_boxes_until_speed_change()}", True, TEXT_COLOR)
    window.blit(speed_increase_text, (TEXT_OFFSET_FROM_SCREEN, TEXT_OFFSET_FROM_SCREEN * 2 + score_text.get_size()[1]))

def update_objects():
    player.update()
    window.blit(player.sprite, player.rect)

    currentBox = boxHandler.boxes[0]
    currentBox.update()
    window.blit(currentBox.sprite, currentBox.rect)

    if currentBox.rect.colliderect(player.rect): player.has_been_hit = True

# Start game loop
game_running = True
while game_running:
    # Limit framerate to specified FPS
    delta_time = get_delta_time()
    accumulator += delta_time

    if accumulator < game_update_rate: continue
    else: accumulator -= game_update_rate

    for event in pygame.event.get():
        if event.type == pygame.QUIT: game_running = False

    draw_scene()
    draw_UI()
    update_objects()

    pygame.display.flip()

pygame.quit()