#
# THE 'PRESENTATION LAYER' OF THE PROGRAM
#

# import logging
# logging.basicConfig(level=logging.DEBUG)

import commands


class Option:
    def __init__(self, name: str, command: commands.Command, prep_call=None):
        self.name = name
        self.command = command
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


def option_choice_is_valid(choice: str, options: dict[str, Option]):
    return choice.upper() in options


def get_option_choice(options: dict[str, Option]):
    choice = input("Choose an option: ")
    while not option_choice_is_valid(choice, options):
        print("Invalid choice")
        choice = input("Choose an option: ")
    return options[choice.upper()]


# ----- MAIN LOGIC -----
def loop():
    pass


if __name__ == "__main__":

    print("====================")
    print("| Welcome to Bark! |")
    print("====================")

    # Database initialization (creates 'bookmarks' table if needed)
    commands.CreateBookmarksTableCommand().execute()

    # Menu options definition.
    options = {
        "A": Option("Add a bookmark", commands.AddBookmarkCommand()),
        "B": Option("List bookmarks by date", commands.ListBookmarksCommand()),
        "T": Option(
            "List bookmarks by title", commands.ListBookmarksCommand(order_by="title")
        ),
        "D": Option("Delete a bookmark", commands.DeleteBookmarkCommand()),
        "Q": Option("Quit", commands.QuitCommand()),
    }

    # Iterates over menu options and prints them in the CLI-specifications format.
    print_options(options)

    # Gets a user's choice of menu option
    chosen_option = get_option_choice(options)
    chosen_option.choose()
