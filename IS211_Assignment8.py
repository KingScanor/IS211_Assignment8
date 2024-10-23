# Assignment 8
import argparse
import random
import time


class Player:
    """
        Represents a player in the Pig game.

        Attributes:
            name (str): The name of the player.
            score (int): The player's total score.
            is_turn (bool): Whether it's currently the player's turn.
            turn_total (int): The player's accumulated score in the current turn.
        """
    def __init__(self, name):
        self.name = name
        self.score = 0
        self. is_turn = False
        self.turn_total = 0

    def roll_die(self, die):
        roll = die.roll()
        if roll == 1:
            print(f"Turn Over! {self.name} rolled a 1.\n")
            self.reset_turn()
            return False
        else:
            self.turn_total += roll
            print (f"\n{self.name} rolled a {roll}. Turn Total: {self.turn_total}, Total Score: {self.score}\n")
            return True

    def hold(self):
        self.score += self.turn_total
        print (f"{self.name} holds. Total Score: {self.score}\n")
        self.reset_turn()

    def reset_turn(self):
        self.turn_total = 0
        self.is_turn = False

class ComputerPlayer(Player):
    """
        Represents a computer player in the Pig game. Inherits from Player.

        Attributes:
            name (str): The name of the computer player.
        """
    def __init__(self, name):
        super().__init__(name)

    def make_decision(self):
        hold_threshold = min(25, 100 - self.score)
        if self.turn_total >= hold_threshold:
            return '2'
        else:
            return '1'

class Die:
    """
        Represents a die with a specified number of sides.

        Attributes:
            sides (int): The number of sides on the die (default is 6).
        """
    def __init__(self, sides = 6):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)

class PlayerFactory:
    """
        Creates Player objects based on the specified player type.
        """
    def create_player(self, player_type, name):
        if player_type == "human":
            return Player(name)
        elif player_type == "computer":
            return ComputerPlayer(name)

        else:
            raise ValueError("Invalid player type")

class Game:
    """
        Manages the Pig game between two players.

        Attributes:
            player1 (Player): The first player.
            player2 (Player): The second player.
            current_player (Player): The player whose turn it is.
            die (Die): The die used in the game.
        """
    def __init__(self, player1_type, player2_type):
        self.factory = PlayerFactory()
        self.player1 = self.factory.create_player(player1_type, "Player 1")
        self.player2 = self.factory.create_player(player2_type, "Player 2")
        self.current_player = self.player1
        self.current_player.is_turn = True
        self.die = Die()

    def start_game(self):
        while self.player1.score < 100 and self.player2.score < 100:
            self.play_turn()

    def play_turn(self, proxy=None):
        print (f"\n{self.current_player.name}'s turn:")

        while self.current_player.is_turn:
            if proxy and proxy.check_time():
                return

            if isinstance(self.current_player, ComputerPlayer):
                decision = self.current_player.make_decision()
                print (f"{self.current_player.name} chooses to {'Roll' if decision == '1' else 'Hold'}")
            else:
                decision = input ("Roll (1) or Hold (2)?").lower()

            if decision == '1':
                if not self.current_player.roll_die(self.die):
                    self.switch_turn()
            elif decision == "2":
                self.current_player.hold()
                self.switch_turn()
            else:
                print ("Invalid input, Please Type '1' for Roll or '2' for Hold.")
            if self.player1.score >= 100 or self.player2.score >= 100:
                self.check_winner()
                return

    def switch_turn(self):
        self.current_player.is_turn = False
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1
        self.current_player.is_turn = True
        self.display_scores()
        self.display_current_player()

    def display_scores(self):
        print (f"\nScores - {self.player1.name}: {self.player1.score}, {self.player2.name}: {self.player2.score}\n")

    def display_current_player(self):
        print (f"\n{self.current_player.name}'s turn:")

    def check_winner(self):
        if self.player1.score >= 100:
            print (f"\nCongratulations to the winner, {self.player1.name}.")
        elif self.player2.score >= 100:
            print(f"\nCongratulations to the winner, {self.player2.name}.")
        else:
            if self.player1.score > self.player2.score:
                print (f"\nYou ran out of time! {self.player1.name} wins!")
            elif self.player2.score > self.player1.score:
                print(f"\nYour ran out of time! {self.player2.name} wins!")
            else:
                print ("\n Time's up! There is a tie!")

class TimedGameProxy:
    """
        A proxy class for the Game class that adds a time limit to the game.

        Attributes:
            game (Game): The Game object being proxied.
            timed (bool): Whether the game is timed or not.
            start_time (float): The time the game started.
            time_limit (int): The time limit for the game in seconds (default 60).
        """
    def __init__(self, player1_type, player2_type, timed):
        self.game = Game (player1_type, player2_type)
        self.timed = timed
        self.start_time = None
        self.time_limit = 60

    def start_game(self):
        self.start_time = time.time()

        while self.game.player1.score < 100 and self.game.player2.score < 100:
            self.game.play_turn(self)
            break

    def check_time(self):
        if self.timed and time.time() - self.start_time > self.time_limit:
            self.game.display_scores()
            self.game.check_winner()
            self.display_time_taken()
            return True
        return False

    def display_time_taken(self):
        time_taken = time.time() - self.start_time
        print(f"\nTime Taken: {time_taken: .2f} seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description= "Play the Pig dice game.")
    parser.add_argument ("--player1", choices=["human", "computer"], default="human", help="Type of player 1" )
    parser.add_argument ("--player2", choices=["human", "computer"], default="human", help="Type of player 2")
    parser.add_argument ("--timed", action="store_true", help="Enable timed game mode")
    args = parser.parse_args()

    game = TimedGameProxy(args.player1, args.player2, args.timed)
    game.start_game()






