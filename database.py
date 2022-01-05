import sqlite3


class DatabaseManager:
    def __init__(self, database_filename: str) -> None:
        self.connection = sqlite3.connect(database_filename)

    def __del__(self):
        # Close the connection to the database when the program finishes,
        # to limit the possibility of data corruption.
        self.connection.close()
        print(f"Closed connection {self.connection}")


if __name__ == "__main__":
    db_manager = DatabaseManager("mock.db")
    del db_manager
