# ------
# THE 'PRESENTATION LAYER' OF THE PROGRAM
# ------

import time

# import logging
# logging.basicConfig(level=logging.DEBUG)

import commands
from utilities import clear_screen


def print_bookmarks(bookmarks: list, field_max_chars: int = None) -> None:
    def format_field(field):
        field = str(field)
        if field_max_chars and len(field) > field_max_chars:
            field = f"{field[:field_max_chars]}..."
        return field

    for bookmark in bookmarks:
        print("\t".join(format_field(field) if field else "" for field in bookmark))


class Option:
    """Class for connecting menu text to business logic commands"""

    def __init__(self, name: str, command: commands.Command, prep_call=None):
        # Action's name displayed in the CLI menu
        self.name = name
        # Instance of the command to execute
        self.command = command
        # Optional preparation step to call before executing a command
        self.prep_call = prep_call

    def _handle_message(self, message) -> None:
        if isinstance(message, list):
            print_bookmarks(message, field_max_chars=35)
        else:
            print(message)

    def trigger(self):
        data = self.prep_call() if self.prep_call else None
        message = self.command.execute(data) if data else self.command.execute()
        self._handle_message(message)

    def __str__(self) -> str:
        return self.name


def print_options(options: dict[str, Option]):
    for shortcut, option in options.items():
        print(f"({shortcut}) {option}")
    print()


# Functions for managing user's CLI menu option choice.
# ------
def option_choice_is_valid(choice: str, options: dict[str, Option]):
    return choice.upper() in options


def get_option_choice(options: dict[str, Option]):
    choice = input("Choose an option: ")
    while not option_choice_is_valid(choice, options):
        print("Invalid choice")
        choice = input("Choose an option: ")
    return options[choice.upper()]


# Functions for interaction with the user.
# ------
# A general function for prompting users for input
def get_user_input(label: str, required: bool = True):
    value = input(f"{label}: ") or None
    while required and not value:
        value = input(f"{label}: ") or None
    return value


# A function to get the necessary information for adding a new bookmark
def get_new_bookmark_info():
    return {
        "title": get_user_input("Title"),
        "url": get_user_input("URL"),
        "notes": get_user_input("Notes", required=False),
    }


# A function to get the necessary information for deleting a bookmark
def get_bookmark_id_for_deletion():
    return get_user_input("Enter a bookmark ID to delete")


# A function to get the necessary information for editing/updating a bookmark
def get_new_bookmark_info():
    bookmark_id = get_user_input("Enter a bookmark ID to edit")
    field = get_user_input("Choose a value to edit (title, URL, notes)")
    new_value = get_user_input(f"Enter the new value for {field}")
    return {"id": bookmark_id, "update": {field: new_value}}


# A function to get the Github username to import stars from
def get_github_import_options():
    return {
        "github_username": get_user_input("GitHub username"),
        "preserve_timestamps": get_user_input(
            "Preserve timestamps? [Y/n]", required=False
        )  # whether or not to retain the time when the star was originally created
        in {
            "Y",
            "y",
            None,
        },  # Accepts "Y", "y", or just pressing Enter as the user saying "yes"
    }


# App loop
def loop(options: dict):

    # Iterates over menu options and prints them in the CLI-specifications format.
    clear_screen()
    print_options(options)

    # Gets a user's choice of menu option
    chosen_option = get_option_choice(options)
    clear_screen()
    chosen_option.trigger()

    # Allows to pause and wait for the user to press 'Enter' before proceeding,
    # in order to let the user review the result.
    _ = input("\nPress ENTER to return to menu")


if __name__ == "__main__":

    clear_screen()

    print("====================================================")
    print("                 Welcome to Bark!                   ")
    print("====================================================")

    time.sleep(1)

    # CLI menu options definition
    menu_options = {
        "A": Option(
            "Add a bookmark",
            commands.AddBookmarkCommand(),
            prep_call=get_new_bookmark_info,
        ),
        "B": Option("List bookmarks by date", commands.ListBookmarksCommand()),
        "T": Option(
            "List bookmarks by title", commands.ListBookmarksCommand(order_by="title")
        ),
        "E": Option(
            "Edit a bookmark",
            commands.EditBookmarkCommand(),
            prep_call=get_new_bookmark_info,
        ),
        "D": Option(
            "Delete a bookmark",
            commands.DeleteBookmarkCommand(),
            prep_call=get_bookmark_id_for_deletion,
        ),
        ""
        "G": Option(
            "Import GitHub stars",
            commands.ImportGitHubStarsCommand(),
            prep_call=get_github_import_options,
        ),
        "Q": Option("Quit", commands.QuitCommand()),
    }

    # Database initialization (creates 'bookmarks' table if needed)
    commands.CreateBookmarksTableCommand().execute()

    # Loops forever (until the user chooses the option corresponding to 'QuitCommand')
    # Now BARK will give the user a way to return to the menu after each interaction,
    # and the menu gives them an option to exit.
    while True:
        loop(menu_options)
