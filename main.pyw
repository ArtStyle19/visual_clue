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
            pygame.draw.line(screen, "green", ((HEIGHT // self.size) * i, 0), ((HEIGHT // self.size) * i, WIDTH))
            pygame.draw.line(screen, "green", (0, (WIDTH // self.size) * i), (HEIGHT, (WIDTH // self.size) * i))

# Areas players can't reach (walls and borders)
# Map borders
off_limits = [(HEIGHT + MARGIN, MARGIN + i * SQUARE_SIDE) for i in range(-1, 25)] + \
             [(MARGIN + i * SQUARE_SIDE, HEIGHT + MARGIN) for i in range(-1, 25)] + \
             [(MARGIN + i * SQUARE_SIDE, MARGIN - SQUARE_SIDE) for i in range(-1, 25)] + \
             [(MARGIN - SQUARE_SIDE, MARGIN + i * SQUARE_SIDE) for i in range(-1, 25)]




class ClueGame:
    def __init__(self, players):
        self.characters = ["Character1", "Character2", "Character3", "Character4", "Character5", "Character6"]
        self.weapons = ["Weapon1", "Weapon2", "Weapon3", "Weapon4", "Weapon5", "Weapon6"]
        self.rooms = ["Room1", "Room2", "Room3", "Room4", "Room5", "Room6"]
        self.players = players
        self.solution = {}
        self.knowledge_base = []

    def pick_solution(self):
        # Randomly select the solution
        self.solution["murderer"] = random.choice(self.characters)
        self.solution["weapon"] = random.choice(self.weapons)
        self.solution["room"] = random.choice(self.rooms)

    def distribute_cards(self):
        # Distribute remaining cards among players (not part of the solution)
        remaining_cards = [c for c in self.characters if c != self.solution["murderer"]]
        remaining_cards += [w for w in self.weapons if w != self.solution["weapon"]]
        remaining_cards += [r for r in self.rooms if r != self.solution["room"]]
        random.shuffle(remaining_cards)

        print("\nDistribuyendo cartas a los jugadores:")
        for i, card in enumerate(remaining_cards):
            player = self.players[i % len(self.players)]
            player.add_card(card)
            print(f"{player.name} recibe la carta: {card}")

    def is_guess_consistent(self, guess):
        # Check if a guess is consistent with the current knowledge base
        return all(rule(guess) for rule in self.knowledge_base)

    def make_informed_guess(self):
        # Make a guess that hasn't been disproven yet
        while True:
            guess = {
                "murderer": random.choice(self.characters),
                "weapon": random.choice(self.weapons),
                "room": random.choice(self.rooms)
            }
            if self.is_guess_consistent(guess):
                return guess

    def add_knowledge(self, guess):
        # Mark the entire guess as false and update the knowledge base
        print(f"\nAdivinanza: {guess} ha sido marcada como falsa.")
        self.knowledge_base.append(
            lambda model: model["murderer"] != guess["murderer"] or model["weapon"] != guess["weapon"] or model["room"] != guess["room"]
        )
        print(f"Actualizando KB: {guess} es incorrecta.")

    def is_solution_unique(self, model):
        # Check if the current model is valid according to the KB
        return all(rule(model) for rule in self.knowledge_base)

    def guess_and_update(self, index):
        # Players make guesses, and the KB is updated until the correct solution is found
        # while True:
            # for player in self.players:

                # Create an informed guess for each player
                guess = self.make_informed_guess()
                print(f"\n{self.players[index].name} adivina: {guess}")
                
                disproved = False
                for other_player in self.players:
                    if other_player != player:
                        disproved = other_player.disprove_guess(guess)
                        if disproved:
                            break

                # If any player disproves the guess, mark the entire guess as false
                if disproved:
                    self.add_knowledge(guess)
                else:
                    # If no one disproves, it means the guess is correct
                    print(f"\n¡El jugador {self.players[index].name} ha adivinado correctamente!")
                    print(f"La solución es: {guess}")
                    pygame.quit()
                    return guess

    def play(self):
        print("Iniciando Clue Game...")
        self.pick_solution()
        self.distribute_cards()

        # Keep guessing until the unique solution is found
        self.guess_and_update()

# Class for rooms
class Room:
    def __init__(self, name, wall):
        self.name = name
        self.wall = wall
        # Add room walls to off_limits
        off_limits.extend([(i[0] * SQUARE_SIDE + MARGIN, i[1] * SQUARE_SIDE + MARGIN) for i in self.wall])

    def show_room(self):
        for i in self.wall:
            pygame.draw.rect(screen, "white", pygame.Rect(i[0] * SQUARE_SIDE, i[1] * SQUARE_SIDE, SQUARE_SIDE, SQUARE_SIDE))





# Class for players
class Player:
    def __init__(self, current_pos, img, name):
        self.name = name
        self.cards = []
        self.current_pos = current_pos
        self.img = img
        self.steps_remaining = 0  # Steps remaining to move

    def disprove_guess(self, guess):
        # If the player has any card that disproves the guess, return True
        for card in self.cards:
            if card in guess.values():
                print(f"{self.name} podría contradecir la adivinanza con una de sus cartas.")
                return True
        return False

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

# Setting up pygame
pygame.init()
screen = pygame.display.set_mode((HEIGHT + SIDE, WIDTH))
run = True
smallfont = pygame.font.SysFont('Corbel', 20)

# Setting up the grid
board = Grid(SQUARES)

# Players
p1_img = pygame.image.load("./assets/basketball-player.png")
p2_img = pygame.image.load("./assets/basketball.png")
p3_img = pygame.image.load("./assets/player.png")
p4_img = pygame.image.load("./assets/tennis-player.png")
p5_img = pygame.image.load("./assets/tennis.png")
p6_img = pygame.image.load("./assets/writer (2).png")
players = [
    Player((MARGIN, MARGIN), p1_img, "Player1"),
    Player((HEIGHT - MARGIN - IMAGE_WIDTH, MARGIN), p2_img, "Player2"),
    Player((MARGIN, HEIGHT - MARGIN - IMAGE_WIDTH), p5_img, "Player3"),
    Player((HEIGHT - MARGIN - IMAGE_WIDTH, HEIGHT - MARGIN - IMAGE_WIDTH), p4_img, "Player4"),
    Player((HEIGHT - MARGIN - IMAGE_WIDTH, (HEIGHT - IMAGE_WIDTH) // 2), p3_img, "Player5"),
    Player((MARGIN, (HEIGHT - IMAGE_WIDTH) // 2), p6_img, "Player1")
]

# Rooms
study = Room('study', [(6, i) for i in range(5) if i != 2] + [(i, 4) for i in range(7)])
lounge = Room('lounge', [(i, 4) for i in range(18, 25) if i != 2] + [(18, i) for i in range(5) if i != 2])
conservatory = Room('conservatory', [(6, i) for i in range(20, 25) if i != 22] + [(i, 20) for i in range(7)])
kitchen = Room('kitchen', [(18, i) for i in range(20, 25) if i != 22] + [(i, 20) for i in range(18, 25)])
hall = Room('hall', [(8, i) for i in range(7)] + [(i, 6) for i in range(8, 17) if i != 12] + [(16, i) for i in range(7)])
dining_room = Room('dining room', [(18, i) for i in range(8, 17) if i != 12] + [(i, 8) for i in range(18, 25)] + [(i, 16) for i in range(18, 25)])
cellar = Room('cellar', [(10, i) for i in range(10, 15)] + [(i, 14) for i in range(10, 15)] + [(14, i) for i in range(10, 15)] + [(i, 10) for i in range(10, 15) if i != 12])
billard_room = Room('billard room', [(6, i) for i in range(13, 18) if i != 15] + [(i, 13) for i in range(7)] + [(i, 17) for i in range(7)])
library = Room('library', [(6, i) for i in range(7, 12) if i != 9] + [(i, 7) for i in range(7)] + [(i, 11) for i in range(7)])
ballroom = Room('ballroom', [(8, i) for i in range(18, 25)] + [(i, 18) for i in range(8, 17) if i != 12] + [(16, i) for i in range(18, 25)])

rooms = [study, lounge, kitchen, conservatory, hall, dining_room, cellar, billard_room, library, ballroom]

# Buttons
roll_button = Button((1650, 80), 'roll')
number_rolled = 0
current_player_index = 0
number_rolled_text = smallfont.render("number rolled is {}".format(number_rolled), True, (255, 255, 255))

if __name__ == "__main__":

    # players = [Player("Player1"), Player("Player2"), Player("Player3"), Player("Player4"), Player("Player5"), Player("Player6")]
    game = ClueGame(players)
    game.pick_solution()
    game.distribute_cards()
    # game.play()
    while run:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # Permitir mover solo si el jugador actual tiene pasos restantes
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN] and players[current_player_index].steps_remaining > 0:
                    players[current_player_index].move_player(event.key)
                    players[current_player_index].steps_remaining -= 1
                    if players[current_player_index].steps_remaining == 0:  # Cambia al siguiente jugador
                        current_player_index = (current_player_index + 1) % len(players)
                        game.guess_and_update(current_player_index)
                        number_rolled = 0  # Resetea el número de pasos al siguiente jugador

            # Habilitar la tirada de dados solo cuando el jugador actual no tenga pasos restantes
            if event.type == pygame.MOUSEBUTTONDOWN and roll_button.pos[0] / 2 <= mouse[0] <= roll_button.pos[0] / 2 + 140 and roll_button.pos[1] / 2 <= mouse[1] <= roll_button.pos[1] / 2 + 40 and players[current_player_index].steps_remaining == 0:
                number_rolled = random.randint(1, 6)
                players[current_player_index].steps_remaining = number_rolled  # Set steps to the number rolled

        screen.fill((0, 0, 0))
        board.set_up()
        
        for room in rooms:
            room.show_room()

        # Muestra el botón
        roll_button.show_button()
        number_rolled_text = smallfont.render("Number rolled is {}".format(number_rolled), True, (255, 255, 255))
        screen.blit(number_rolled_text, (1600, 200))

        for player in players:
            player.show_player()

        pygame.display.flip()

    pygame.quit()
