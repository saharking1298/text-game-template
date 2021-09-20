from Engine import files_setup, GameEngine, SaveLoadEngine as Saver


class Game:
    def __init__(self):
        self.selected_slot = ""

    def main_menu(self,):
        choices = {"New Game": self.new_game,
                   "Load Game": self.load_game,
                   "Creation Club": self.creation_club,
                   "Exit": self.exit}
        e.print("Welcome to the dungeon!")
        e.menu("What do you want to do now?", choices, clear=True)

    def new_game(self):
        e.print("Enter the new save slot name: ")
        slot_name = input().strip()
        while Saver.slot_exists(slot_name):
            e.print("Sorry, this slot already exist.")
            slot_name = input().strip()
        Saver.create_save_slot(slot_name)
        self.selected_slot = slot_name
        e.print(f"Slot '{slot_name}' has been selected.")

        e.print("New game...")

    def load_game(self):
        slots = Saver.get_slot_names()
        if len(slots) > 0:
            selected_slot = e.menu("Select a save to load:", slots)
            self.selected_slot = selected_slot
            e.print(f"Loading game '{selected_slot}'...")
        else:
            self.new_game()

    def creation_club(self):
        e.print("Welcome to Creation Club!")

    def exit(self):
        e.print("Sorry to see you go!")
        exit(0)


def main():
    game = Game()
    game.main_menu()


if __name__ == '__main__':
    # Files setup
    files_setup()
    # Setting up the engine
    e = GameEngine()
    e.printer.windows_init()
    e.printer.set_color("green")
    e.clear()
    # Calling main
    main()
