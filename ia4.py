import random

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
        # Generate a guess based on remaining options in the KB
        remaining_characters = [c for c in self.characters if not any(rule({"murderer": c, "weapon": None, "room": None}) for rule in self.knowledge_base)]
        remaining_weapons = [w for w in self.weapons if not any(rule({"murderer": None, "weapon": w, "room": None}) for rule in self.knowledge_base)]
        remaining_rooms = [r for r in self.rooms if not any(rule({"murderer": None, "weapon": None, "room": r}) for rule in self.knowledge_base)]

        if remaining_characters and remaining_weapons and remaining_rooms:
            guess = {
                "murderer": random.choice(remaining_characters),
                "weapon": random.choice(remaining_weapons),
                "room": random.choice(remaining_rooms)
            }
            return guess
        else:
            return None  # No se puede hacer una adivinanza informada

    def add_knowledge(self, guess, disproved_player):
        # Mark the entire guess as false and update the knowledge base
        print(f"\nAdivinanza: {guess} ha sido marcada como falsa por {disproved_player.name}.")
        self.knowledge_base.append(
            lambda model: model["murderer"] != guess["murderer"] and 
                          model["weapon"] != guess["weapon"] and 
                          model["room"] != guess["room"]
        )
        print(f"Actualizando KB: {guess} es incorrecta.")

    def guess_and_update(self):
        # Players make guesses, and the KB is updated until the correct solution is found
        while True:
            for player in self.players:
                # Create an informed guess for each player
                guess = self.make_informed_guess()
                if guess is None:
                    print(f"\n{player.name} no puede hacer una adivinanza informada.")
                    continue

                print(f"\n{player.name} adivina: {guess}")
                
                disproved = False
                disproving_player = None
                for other_player in self.players:
                    if other_player != player:
                        disproved = other_player.disprove_guess(guess)
                        if disproved:
                            disproving_player = other_player
                            break

                # If any player disproves the guess, mark the entire guess as false
                if disproved:
                    self.add_knowledge(guess, disproving_player)
                else:
                    # If no one disproves, it means the guess is correct
                    print(f"\n¡El jugador {player.name} ha adivinado correctamente!")
                    print(f"La solución es: {guess}")
                    return guess

    def play(self):
        print("Iniciando Clue Game...")
        self.pick_solution()
        self.distribute_cards()

        # Keep guessing until the unique solution is found
        self.guess_and_update()

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def disprove_guess(self, guess):
        # If the player has any card that disproves the guess, return True
        for card in self.cards:
            if card in guess.values():
                print(f"{self.name} podría contradecir la adivinanza con una de sus cartas.")
                return True
        return False

if __name__ == "__main__":
    players = [Player("Player1"), Player("Player2"), Player("Player3"), Player("Player4"), Player("Player5"), Player("Player6")]
    game = ClueGame(players)
    game.play()
