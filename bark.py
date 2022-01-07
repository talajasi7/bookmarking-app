#
# THE 'PRESENTATION LAYER' OF THE PROGRAM
#

import os

# import logging
# logging.basicConfig(level=logging.DEBUG)

import commands


class Option:
    """Class for connecting menu text to business logic commands"""

    def __init__(self, name: str, command: commands.Command, prep_call=None):
        # action's name displayed in the CLI menu
        self.name = name
        # instance of the command to execute
        self.command = command
        # optional preparation step to call before executing a command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        message = self.command.execute(data) if data else self.command.execute()
        print(message)

    def __str__(self) -> str:
        return self.name


def print_options(options: dict[str, Option]):
    for shortcut, option in options.items():
        print(f"({shortcut}) {option}")
    print()


# Functions for managing user choice for the CLI menu options.
# ---


def option_choice_is_valid(choice: str, options: dict[str, Option]):
    return choice.upper() in options


def get_option_choice(options: dict[str, Option]):
    choice = input("Choose an option: ")
    while not option_choice_is_valid(choice, options):
        print("Invalid choice")
        choice = input("Choose an option: ")
    return options[choice.upper()]


# Functions for gathering bookmark information from the user.
# ---
# A general function for prompting users for input
def get_user_input(label: str, required: bool = True):
    value = input(f"{label}: ") or None
    while required and not value:
        value = input(f"{label}: ") or None
    return value


# A function to get the necessary data for adding a new bookmark
def get_new_bookmark_data():
    return {
        "title": get_user_input("Title"),
        "url": get_user_input("URL"),
        "notes": get_user_input("Notes", required=False),
    }


# A function to get the necessary information for deleting a bookmark
def get_bookmark_id_for_deletion():
    return get_user_input("Enter a bookmark ID to delete:")


# A function for clearing the screen (OS-agnostic).
def clear_screen():
    clear = "cls" if os.name == "nt" else "clear"
    os.system(clear)


# Application loop
def loop():
    # Menu options definition.
    options = {
        "A": Option(
            "Add a bookmark",
            commands.AddBookmarkCommand(),
            prep_call=get_new_bookmark_data,
        ),
        "B": Option("List bookmarks by date", commands.ListBookmarksCommand()),
        "T": Option(
            "List bookmarks by title", commands.ListBookmarksCommand(order_by="title")
        ),
        "D": Option(
            "Delete a bookmark",
            commands.DeleteBookmarkCommand(),
            prep_call=get_bookmark_id_for_deletion,
        ),
        "Q": Option("Quit", commands.QuitCommand()),
    }

    # Iterates over menu options and prints them in the CLI-specifications format.
    clear_screen()
    print("====================")
    print("| Welcome to Bark! |")
    print("====================")
    print_options(options)

    # Gets a user's choice of menu option
    chosen_option = get_option_choice(options)
    clear_screen()
    chosen_option.choose()

    # Allows to pause and wait for the user to press 'Enter' before proceeding,
    # in order to let the user review the result.
    _ = input("Press ENTER to return to menu")


if __name__ == "__main__":

    # Database initialization (creates 'bookmarks' table if needed)
    commands.CreateBookmarksTableCommand().execute()

    # Loops forever (until the user chooses the option corresponding to 'QuitCommand')
    # Now BARK will give the user a way to return to the menu after each interaction,
    # and the menu gives them an option to exit.
    while True:
        loop()
