import pygame
import random

HEIGHT = 800  # grid height
WIDTH = 800  # grid width
SIDE = 200  # side menu width
SQUARES = 25
SQUARE_SIDE = HEIGHT // SQUARES
MARGIN = 4
IMAGE_WIDTH = 24

# Class for grid
class Grid:
    def __init__(self, size):
        self.size = size

    def set_up(self):
        for i in range(self.size + 1):
            pygame.draw.line(screen, "black", ((HEIGHT // self.size) * i, 0), ((HEIGHT // self.size) * i, WIDTH))
            pygame.draw.line(screen, "black", (0, (WIDTH // self.size) * i), (HEIGHT, (WIDTH // self.size) * i))

# Class for rooms
class Room:
    def __init__(self, name, wall):
        self.name = name
        self.wall = wall
        off_limits.extend([(i[0] * SQUARE_SIDE + MARGIN, i[1] * SQUARE_SIDE + MARGIN) for i in self.wall])

    def show_room(self):
        for i in self.wall:
            pygame.draw.rect(screen, "white", pygame.Rect(i[0] * SQUARE_SIDE, i[1] * SQUARE_SIDE, SQUARE_SIDE, SQUARE_SIDE))

# Class for players
class Player:
    def __init__(self, name, current_pos, img):
        self.name = name
        self.current_pos = current_pos
        self.img = img
        self.steps_remaining = 0  # Steps remaining to move
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def show_player(self):
        screen.blit(self.img, self.current_pos)

    def move_player(self, direction):
        global illegal_move
        illegal_move = False
        original_pos = self.current_pos

        if direction == pygame.K_LEFT:
            self.current_pos = (self.current_pos[0] - SQUARE_SIDE, self.current_pos[1])
        elif direction == pygame.K_RIGHT:
            self.current_pos = (self.current_pos[0] + SQUARE_SIDE, self.current_pos[1])
        elif direction == pygame.K_UP:
            self.current_pos = (self.current_pos[0], self.current_pos[1] - SQUARE_SIDE)
        elif direction == pygame.K_DOWN:
            self.current_pos = (self.current_pos[0], self.current_pos[1] + SQUARE_SIDE)

        if self.current_pos in off_limits:
            illegal_move = True
            self.current_pos = original_pos

    def is_in_center(self):
        center_pos = ((WIDTH - SQUARE_SIDE) // 2, (HEIGHT - SQUARE_SIDE) // 2)
        return self.current_pos == center_pos

    def disprove_guess(self, guess):
        for card in self.cards:
            if card in guess.values():
                print(f"{self.name} podría contradecir la adivinanza con una de sus cartas.")
                return True
        return False

# Class for buttons
class Button:
    def __init__(self, pos, text):
        self.pos = pos
        self.text = text
        self.state = "not_pressed"

    def show_button(self):
        color_light = (170, 170, 170)
        color_dark = (100, 100, 100)
        smallfont = pygame.font.SysFont('Corbel', 35)
        text = smallfont.render(self.text, True, (255, 255, 255))
        mouse = pygame.mouse.get_pos()
        if self.pos[0] / 2 <= mouse[0] <= self.pos[0] / 2 + 140 and self.pos[1] / 2 <= mouse[1] <= self.pos[1] / 2 + 40:
            pygame.draw.rect(screen, color_light, [self.pos[0] / 2, self.pos[1] / 2, 140, 40])
        else:
            pygame.draw.rect(screen, color_dark, [self.pos[0] / 2, self.pos[1] / 2, 140, 40])
        screen.blit(text, (self.pos[0] / 2 + 50, self.pos[1] / 2))

    def action(self):
        self.state = "pressed"

# Logic for Clue Game
class ClueGame:
    def __init__(self, players):
        self.characters = ["Character1", "Character2", "Character3", "Character4", "Character5", "Character6"]
        self.weapons = ["Weapon1", "Weapon2", "Weapon3", "Weapon4", "Weapon5", "Weapon6"]
        self.rooms = ["Room1", "Room2", "Room3", "Room4", "Room5", "Room6"]
        self.players = players
        self.solution = {}
        self.knowledge_base = []

    def pick_solution(self):
        self.solution["murderer"] = random.choice(self.characters)
        self.solution["weapon"] = random.choice(self.weapons)
        self.solution["room"] = random.choice(self.rooms)

    def distribute_cards(self):
        remaining_cards = [c for c in self.characters if c != self.solution["murderer"]]
        remaining_cards += [w for w in self.weapons if w != self.solution["weapon"]]
        remaining_cards += [r for r in self.rooms if r != self.solution["room"]]
        random.shuffle(remaining_cards)

        for i, card in enumerate(remaining_cards):
            player = self.players[i % len(self.players)]
            player.add_card(card)

    def is_guess_consistent(self, guess):
        return all(rule(guess) for rule in self.knowledge_base)

    def make_informed_guess(self):
        while True:
            guess = {
                "murderer": random.choice(self.characters),
                "weapon": random.choice(self.weapons),
                "room": random.choice(self.rooms)
            }
            if self.is_guess_consistent(guess):
                return guess

    def add_knowledge(self, guess):
        print(f"Adivinanza: {guess} ha sido marcada como falsa.")
        self.knowledge_base.append(
            lambda model: model["murderer"] != guess["murderer"] or model["weapon"] != guess["weapon"] or model["room"] != guess["room"]
        )
        print(f"Actualizando KB: {guess} es incorrecta.")

    def guess_and_update(self, current_player):
        guess = self.make_informed_guess()
        print(f"\n{current_player.name} adivina: {guess}")

        disproved = False
        for other_player in self.players:
            if other_player != current_player:
                disproved = other_player.disprove_guess(guess)
                if disproved:
                    break

        if disproved:
            self.add_knowledge(guess)
        else:
            print(f"\n¡El jugador {current_player.name} ha adivinado correctamente!")
            print(f"La solución es: {guess}")
            return True  # Correct guess

        return False  # Incorrect guess

# Main game setup
pygame.init()
screen = pygame.display.set_mode((HEIGHT + SIDE, WIDTH))
run = True
smallfont = pygame.font.SysFont('Corbel', 20)

board = Grid(SQUARES)
off_limits = []  # Define walls and boundaries here

# Load player images
p1_img = pygame.image.load("./assets/basketball-player.png")
p2_img = pygame.image.load("./assets/basketball.png")
p3_img = pygame.image.load("./assets/player.png")
p4_img = pygame.image.load("./assets/tennis-player.png")
p5_img = pygame.image.load("./assets/tennis.png")
p6_img = pygame.image.load("./assets/writer (2).png")
players = [
    Player("Player1", (MARGIN, MARGIN), p1_img),
    Player("Player2", (HEIGHT - MARGIN - IMAGE_WIDTH, MARGIN), p2_img),
    Player("Player3", (MARGIN, HEIGHT - MARGIN - IMAGE_WIDTH), p5_img),
    Player("Player4", (HEIGHT - MARGIN - IMAGE_WIDTH, HEIGHT - MARGIN - IMAGE_WIDTH), p4_img),
    Player("Player5", (HEIGHT - MARGIN - IMAGE_WIDTH, (HEIGHT - IMAGE_WIDTH) // 2), p3_img),
    Player("Player6", (MARGIN, (HEIGHT - IMAGE_WIDTH) // 2), p6_img)
]

# Initialize the Clue game logic
clue_game = ClueGame(players)
clue_game.pick_solution()
clue_game.distribute_cards()

roll_button = Button((1650, 80), 'roll')
number_rolled = 0
current_player_index = 0

# Game loop
while run:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            current_player = players[current_player_index]
            if current_player.steps_remaining > 0:
                # Verifica si se presionan las teclas de movimiento
                if event.key == pygame.K_LEFT:
                    current_player.move_player(pygame.K_LEFT)
                elif event.key == pygame.K_RIGHT:
                    current_player.move_player(pygame.K_RIGHT)
                elif event.key == pygame.K_UP:
                    current_player.move_player(pygame.K_UP)
                elif event.key == pygame.K_DOWN:
                    current_player.move_player(pygame.K_DOWN)

                # Disminuye el contador de pasos
                current_player.steps_remaining -= 1

                # Si ya no quedan pasos, verifica si está en el centro
                if current_player.steps_remaining == 0 and current_player.is_in_center():
                    print(f"{current_player.name} ha llegado al centro y puede hacer una adivinanza.")
                    if clue_game.guess_and_update(current_player):
                        run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if roll_button.pos[0] / 2 <= mouse[0] <= roll_button.pos[0] / 2 + 140 and roll_button.pos[1] / 2 <= mouse[1] <= roll_button.pos[1] / 2 + 40:
                number_rolled = random.randint(1, 6)
                players[current_player_index].steps_remaining = number_rolled
                print(f"{players[current_player_index].name} tiró un {number_rolled}")

                # Cambia al siguiente jugador
                current_player_index = (current_player_index + 1) % len(players)

    screen.fill((60, 179, 113))
    board.set_up()

    for player in players:
        player.show_player()

    roll_button.show_button()

    pygame.display.flip()
