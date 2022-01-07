#
# THE 'BUSINESS LOGIC LAYER' OF THE PROGRAM
#

import sys
from abc import ABC, abstractmethod
from datetime import datetime

from database import DatabaseManager

# Specify the database's location.
DB_PATH = "data/bookmarks.db"

# Specify database table's name.
TABLE_NAME = "bookmarks"

# Create an instance of DatabaseManager to be used throughout the commands.
db = DatabaseManager(DB_PATH)


class Command(ABC):
    @abstractmethod
    def execute(self):
        """Encapsulates and executes the logic of an specific action"""


class CreateBookmarksTableCommand:
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


class AddBookmarkCommand:
    def execute(self, data: dict[str, str]) -> str:
        data["date_added"] = datetime.now().isoformat()
        db.add_record(TABLE_NAME, data)
        return "Bookmark added!"


class ListBookmarksCommand:
    def __init__(self, order_by: str = "date_added"):
        self.order_by = order_by

    def execute(self) -> list:
        return db.select_records(TABLE_NAME, order_by=self.order_by).fetchall()


class DeleteBookmarkCommand:
    def execute(self, data: dict[str, str]) -> str:
        db.delete_records(TABLE_NAME, criteria={"id": data})
        return "Bookmark deleted!"


class QuitCommand:
    def execute(self):
        sys.exit()
