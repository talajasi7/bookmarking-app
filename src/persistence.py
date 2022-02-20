from abc import ABC, abstractmethod

# Dependencies from first-party modules.
from .database import DatabaseManager


class PersistenceLayer(ABC):
    @abstractmethod
    def create(self, bookmark_data: dict):
        raise NotImplementedError("Persistence layers must implement a create method.")

    @abstractmethod
    def list(self, order_by: str = None):
        raise NotImplementedError("Persistence layers must implement a list method.")

    @abstractmethod
    def edit(self, bookmark_id: str, bookmark_data: dict):
        raise NotImplementedError("Persistence layers must implement an edit method.")

    @abstractmethod
    def delete(self, bookmark_id: str):
        raise NotImplementedError("Persistence layers must implement a delete method.")


class BookmarkDatabase(PersistenceLayer):
    """
    A specific persistence layer implementation that uses a database.
    It provides database-specific implementation for each of the
    behaviors of the interface `PersistenceLayer`.
    """

    def __init__(self) -> None:
        # Specify the database table's name.
        self.table_name = "bookmarks"
        # Handles database creation with `DatabaseManager`.
        self.database = DatabaseManager("data/bookmarks.db")

        # Creates 'bookmarks' table (if needed) inside the database.
        self.database.create_table(
            self.table_name,
            {
                "id": "integer primary key autoincrement",
                "title": "text not null",
                "url": "text not null",
                "notes": "text",
                "date_added": "text not null",
            },
        )

    # Public methods

    def create(self, bookmark_data: dict):
        self.database.add(self.table_name, data=bookmark_data)

    def list(self, order_by: str = None):
        return self.database.select(self.table_name, order_by=order_by).fetchall()

    def edit(self, bookmark_id: str, bookmark_data: dict):
        self.database.update(
            self.table_name, criteria={"id": bookmark_id}, data=bookmark_data
        )

    def delete(self, bookmark_id: str):
        self.database.delete(self.table_name, criteria={"id": bookmark_id})
