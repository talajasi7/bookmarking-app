# ------
# THE 'BUSINESS LOGIC LAYER' OF THE PROGRAM
# ------

import datetime
import sys
from abc import ABC, abstractmethod

# Dependencies from third-party modules.
import requests

# Dependencies from first-party modules.
from .persistence import BookmarkDatabase

# Sets up the persistence layer (this can be swapped in the future)
persistence = BookmarkDatabase()


class Command(ABC):
    @abstractmethod
    def execute(self, data):
        """Encapsulates and executes the logic of an specific action"""


class AddBookmarkCommand(Command):
    def execute(self, data: dict[str, str], timestamp=None) -> str:
        # Fallback to current time if 'timestamp' is not provided
        data["date_added"] = timestamp or datetime.datetime.now().isoformat()
        persistence.create(data)
        return True, None


class ListBookmarksCommand(Command):
    def __init__(self, order_by: str = "date_added"):
        self.order_by = order_by

    def execute(self, data=None) -> list:
        return True, persistence.list(order_by=self.order_by)


class DeleteBookmarkCommand(Command):
    def execute(self, data: dict[str, str]) -> str:
        persistence.delete(data)
        return True, None


class EditBookmarkCommand(Command):
    def execute(self, data: dict[str, str]) -> str:
        persistence.edit(data["id"], data["update"])
        return True, None


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
        return True, bookmarks_imported


class QuitCommand(Command):
    def execute(self, data=None):
        sys.exit()


if __name__ == "__main__":
    pass
