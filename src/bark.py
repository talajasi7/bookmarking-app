# ------
# THE 'PRESENTATION LAYER' OF THE PROGRAM
# ------

import time
from collections.abc import Callable

# import logging
# logging.basicConfig(level=logging.DEBUG)

# Dependencies from first-party modules.
from . import commands as commands
from .utilities import clear_screen


def format_bookmark(bookmark, field_max_chars: int = None):
    def format_field(field):
        field = str(field)
        if field_max_chars and len(field) > field_max_chars:
            field = f"{field[:field_max_chars]}..."
        return field

    return "\t".join(format_field(field) if field else "" for field in bookmark)


class Option:
    """Class for connecting menu text to business logic commands"""

    def __init__(
        self,
        name: str,
        command: commands.Command,
        prep_call: Callable = None,
        success_message: str = "{result}",
    ):
        # Action's name displayed in the CLI menu
        self.name = name
        # Instance of the command to execute
        self.command = command
        # Optional preparation step to call before executing a command
        self.prep_call = prep_call
        # Stores the configured success message for this option for later use
        self.success_message = success_message

    # Dunder methods

    def __str__(self) -> str:
        return self.name

    # Public methods

    def trigger(self):
        data = self.prep_call() if self.prep_call else None
        success, result = self.command.execute(data)

        formatted_result = ""

        if isinstance(result, list):
            for bookmark in result:
                formatted_result += "\n" + format_bookmark(bookmark, field_max_chars=35)
        else:
            formatted_result = result

        if success:
            print(self.success_message.format(result=formatted_result))

    # Getters & Setters
    # ...


def print_options(options: dict[str, Option]):
    for shortcut, option in options.items():
        print(f"({shortcut}) {option}")
    print()


# Functions for managing user's CLI menu option choice.
# ------
def is_option_choice_valid(choice: str, options: dict[str, Option]):
    return choice.upper() in options


def get_option_choice(options: dict[str, Option]):
    choice = input("Choose an option: ")
    while not is_option_choice_valid(choice, options):
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


# A more specific function to limit the user's choices
def get_restricted_user_input(label: str, valid_inputs: tuple[str] = (None,)):
    value = input(f"{label}: ") or None
    while value not in valid_inputs:
        print(
            f"Please, choose between {', '.join(valid_inputs[:-1])} or {valid_inputs[-1]}"
        )
        value = input(f"{label}: ") or None
    return value


# A function to get the necessary information for adding a new bookmark
def get_new_bookmark_info():
    return {
        "title": get_user_input("Title"),
        "url": get_user_input("URL"),
        "notes": get_user_input("Notes", required=False),
    }


# A function to get the necessary information for editing/updating a bookmark
def get_edit_bookmark_info():
    bookmark_id = get_user_input("Enter a bookmark ID to edit")
    field = get_restricted_user_input(
        "Choose a value to edit (title, URL, notes)",
        valid_inputs=("title", "URL", "notes"),
    )
    new_value = get_user_input(f"Enter the new value for {field}")
    return {"id": bookmark_id, "update": {field: new_value}}


# A function to get the necessary information for deleting a bookmark
def get_bookmark_id_for_deletion():
    return get_user_input("Enter a bookmark ID to delete")


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
    _ = input("\nPress ENTER to return to menu ")


# App launcher
def run_bark():
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
            success_message="Bookmark added!",
        ),
        "B": Option(
            "List bookmarks by date",
            commands.ListBookmarksCommand(),
        ),
        "T": Option(
            "List bookmarks by title",
            commands.ListBookmarksCommand(order_by="title"),
        ),
        "E": Option(
            "Edit a bookmark",
            commands.EditBookmarkCommand(),
            prep_call=get_edit_bookmark_info,
            success_message="Bookmark updated!",
        ),
        "D": Option(
            "Delete a bookmark",
            commands.DeleteBookmarkCommand(),
            prep_call=get_bookmark_id_for_deletion,
            success_message="Bookmark deleted!",
        ),
        ""
        "G": Option(
            "Import GitHub stars",
            commands.ImportGitHubStarsCommand(),
            prep_call=get_github_import_options,
            success_message="Imported {result} bookmarks from starred repos!",
        ),
        "Q": Option("Quit", commands.QuitCommand()),
    }

    # Loops forever (until the user chooses the option corresponding to 'QuitCommand')
    # Now BARK will give the user a way to return to the menu after each interaction,
    # and the menu gives them an option to exit.
    while True:
        loop(menu_options)


if __name__ == "__main__":

    run_bark()
