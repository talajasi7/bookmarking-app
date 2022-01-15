# ------
# THE 'BUSINESS LOGIC LAYER' OF THE PROGRAM
# ------

import datetime
import sys
from abc import ABC, abstractmethod

import requests

from database import DatabaseManager


# Specify the database's location.
DB_PATH = "data/bookmarks.db"

# Specify the database table's name.
TABLE_NAME = "bookmarks"

# Create an instance of DatabaseManager to be used throughout the commands.
db = DatabaseManager(DB_PATH)


class Command(ABC):
    @abstractmethod
    def execute(self):
        """Encapsulates and executes the logic of an specific action"""


class CreateBookmarksTableCommand(Command):
    def execute(self):
        db.create_table(
            TABLE_NAME,
            {
                "id": "integer primary key autoincrement",
                "title": "text not null",
                "url": "text not null",
                "notes": "text",
                "date_added": "text not null",
            },
        )


class AddBookmarkCommand(Command):
    def execute(self, data: dict[str, str], timestamp=None) -> str:
        # Fallback to current time if 'timestamp' is not provided
        data["date_added"] = timestamp or datetime.datetime.now().isoformat()
        db.add_record(TABLE_NAME, data)
        return "Bookmark added!"


class ListBookmarksCommand(Command):
    def __init__(self, order_by: str = "date_added"):
        self.order_by = order_by

    def execute(self) -> list:
        return db.select_records(TABLE_NAME, order_by=self.order_by).fetchall()


class DeleteBookmarkCommand(Command):
    # Given a repository directory, extract the needed pieces to create a bookmark
    def execute(self, data: dict[str, str]) -> str:
        db.delete_records(TABLE_NAME, criteria={"id": data})
        return "Bookmark deleted!"


class EditBookmarkCommand(Command):
    def execute(self, data: dict[str, str]) -> str:
        db.update_records(TABLE_NAME, data=data["update"], criteria={"id": data["id"]})
        return "Bookmark updated!"


class ImportGitHubStarsCommand(Command):
    def _extract_bookmark_info(self, repo: dict):
        return {
            "title": repo["name"],
            "url": repo["html_url"],
            "notes": repo["description"],
        }

    def execute(self, data: dict):

        bookmarks_imported = 0

        github_username = data["github_username"]

        # The URL for the first page of star results
        next_page_of_results = f"https://api.github.com/users/{github_username}/starred"

        while next_page_of_results:
            # Gets the next page of results, using the right header to tell the API
            # to return timestamps
            stars_response = requests.get(
                url=next_page_of_results,
                headers={"Accept": "application/vnd.github.v3.star+json"},
            )
            # The Link header contains the link to the next page, if available
            next_page_of_results = stars_response.links.get("next", {}).get("url")

            for repo_info in stars_response.json():
                repo = repo_info["repo"]
                if data["preserve_timestamps"]:
                    timestamp = datetime.datetime.strptime(
                        repo_info["starred_at"],
                        "%Y-%m-%dT%H:%M:%SZ",  # the timestamp when the star was created
                    )
                else:
                    timestamp = None

                bookmarks_imported += 1

                # Executes an 'AddBookmarkCommand', populating with the repository data
                AddBookmarkCommand().execute(
                    self._extract_bookmark_info(repo), timestamp=timestamp
                )

        # Returns a message indicating how many stars were imported
        return f"Imported {bookmarks_imported} bookmarks from starred repos!"


class QuitCommand(Command):
    def execute(self):
        sys.exit()


if __name__ == "__main__":
    pass
