import colorama
import time
import json
import os

save_file = os.path.join("Resources", "Save.json")


def files_setup():
    # Setup required files
    dirs = ("Resources",)
    files = ("Resources/Save.json",)
    for folder in dirs:
        if not os.path.isdir(folder):
            os.makedirs(folder)
    for file in files:
        file = file.replace("/", os.path.sep)
        if not os.path.isfile(file):
            if file.endswith(".json"):
                json.dump({}, open(file, "w"))
            else:
                open(file, "w")


class GameEngine:
    class Printer:
        def __init__(self):
            self.default_color = colorama.Fore.RESET
            self.color = self.default_color
            self.delay = 0.03  # Normal delay
            self.enabled = True
            self.newline_delay = 0.5
            self.special_delays = {
                '.': 0.25,
                ',': self.delay,
                ';': self.delay,
            }

        def sleep(self, t):
            if self.enabled:
                time.sleep(t)

        def windows_init(self):
            colorama.init()

        def set_color(self, color_name):
            # Setting the text color the printer is currently printing.
            color = getattr(colorama.Fore, color_name.strip().upper())
            print(color, end="")

        def reset_color(self):
            # Resetting printer color to default
            self.color = self.default_color

        def print(self, *text, end="\n"):
            """
            Activate the printer with text to print and pre configures values.
            :param text: Text to print
            :type text: str
            :param end: end param in python's print function
            :return: None
            """
            real_text = ''
            for t in text:
                real_text += str(t)
            text = real_text
            for line in text.split("\n"):
                starting_spaces = ''
                end_spaces = ''
                for char in line:
                    if char == ' ':
                        starting_spaces += ' '
                    else:
                        break
                for char in line[::-1]:
                    if char == ' ':
                        end_spaces += ' '
                    else:
                        break
                print(starting_spaces, end="", flush=True)
                for char in line.strip():
                    print(char, end="", flush=True)
                    if char in self.special_delays:
                        self.sleep(self.special_delays[char])
                    else:
                        self.sleep(self.delay)
                print(end_spaces, end="", flush=True)
                self.sleep(self.newline_delay)
                print(end=end)

    def __init__(self):
        self.printer = self.Printer()

    def print(self, *text, end="\n"):
        self.printer.print(*text)

    def clear(self, clear=True):
        if clear:
            os.system("cls")

    def menu(self, title, options, smooth=False, custom_error='', clear=False):
        state_backup = self.printer.enabled
        self.printer.enabled = smooth
        self.print(title)
        choices = options
        if type(options) == dict:
            choices = tuple(options.keys())
        for i in range(len(choices)):
            self.print(i+1, ") ", choices[i])

        user_input = input().strip().lower()
        while True:
            try:
                choice = int(user_input)
                if 0 < choice <= len(choices):
                    self.printer.enabled = state_backup
                    self.clear(clear)
                    if type(options) == dict:
                        tuple(options.values())[choice - 1]()
                        break
                    else:
                        return options[choice - 1]
            except ValueError:
                pass
            finally:
                for i in range(len(choices)):
                    if choices[i].strip().lower() == user_input:
                        self.printer.enabled = state_backup
                        self.clear(clear)
                        if type(options) == dict:
                            tuple(options.values())[i]()
                            break
                        else:
                            return options[i]
            user_input = input("Enter a valid choice: ").strip().lower()


class SaveLoadEngine:
    @staticmethod
    def get_save_data():
        # Getting the JSON content of Save.json
        return json.load(open(save_file, "r"))

    @staticmethod
    def update_save(data):
        # Updating the JSON content in Save.json
        json.dump(data, open(save_file, "w"), indent=2)

    @staticmethod
    def get_slot_names():
        # Getting a list of all slot names in Save.json
        return tuple(SaveLoadEngine.get_save_data().keys())

    @staticmethod
    def create_save_slot(slot_name):
        # Creating a save slot in Save.json
        content = SaveLoadEngine.get_save_data()
        content[slot_name] = {}
        SaveLoadEngine.update_save(content)

    @staticmethod
    def get_save_slot(slot_name):
        # Getting slot's content from Save.json by slot name
        slots = SaveLoadEngine.get_save_data()
        if slot_name in slots:
            return slots[slot_name]

    @staticmethod
    def slot_exists(slot_name):
        # Checking if a save slot exist in Save.json by it's name
        return slot_name in SaveLoadEngine.get_slot_names()

    @staticmethod
    def update_save_slot(slot_name, content):
        # Update slot content in Save.json by slot name and content.
        save_data = SaveLoadEngine.get_save_data()
        if slot_name in save_data:
            save_data[slot_name] = content
            SaveLoadEngine.update_save(save_data)

    @staticmethod
    def delete_slot(slot_name):
        # Delete a slot from Save.json
        save_data = SaveLoadEngine.get_save_data()
        if slot_name in save_data:
            del (save_data[slot_name])
            SaveLoadEngine.update_save(save_data)
