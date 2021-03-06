# ------
# THE 'PERSISTENCE LAYER' OF THE PROGRAM
# ------

import logging
import sqlite3


class DatabaseManager:
    def __init__(self, database_filename: str):
        self.connection = sqlite3.connect(database_filename)

    def __del__(self):
        # Close the connection to the database when the program finishes,
        # to limit the possibility of data corruption.
        self.connection.close()
        logging.debug(f"Closed connection {self.connection}")

    # Method acting as a building block
    def _execute(self, statement: str, values: list[str] = None) -> sqlite3.Cursor:
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor

    def create_table(self, table_name: str, columns: dict[str, str]) -> None:
        columns_with_types = [
            f"{column_name} {data_type}" for column_name, data_type in columns.items()
        ]
        self._execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name}
            ({', '.join(columns_with_types)});
            """
        )

    def drop_table(self, table_name: str) -> None:
        self._execute(f"DROP TABLE {table_name};")

    def add(self, table_name: str, data: dict[str, str]) -> None:
        placeholders = ", ".join("?" * len(data))
        column_names = ", ".join(data.keys())
        column_values = tuple(data.values())
        self._execute(
            f"""
            INSERT INTO {table_name}
            ({column_names})
            VALUES ({placeholders});
            """,
            column_values,
        )

    def select(
        self, table_name: str, criteria: dict[str, str] = None, order_by: str = None
    ) -> sqlite3.Cursor:
        criteria = criteria or {}

        query = f"SELECT * FROM {table_name}"

        if criteria:
            placeholders = (f"{column} = ?" for column in criteria.keys())
            select_criteria = " AND ".join(placeholders)
            query += f" WHERE {select_criteria}"

        if order_by:
            query += f" ORDER BY {order_by}"

        return self._execute(query, tuple(criteria.values()))

    def update(
        self,
        table_name: str,
        criteria: dict[str, str],
        data: dict[str, str],
    ) -> None:
        data_placeholders = ", ".join(f"{key} = ?" for key in data.keys())
        update_placeholders = (f"{column} = ?" for column in criteria.keys())
        update_criteria = " AND ".join(update_placeholders)
        values = tuple(data.values()) + tuple(criteria.values())
        self._execute(
            f"""
            UPDATE {table_name}
            SET {data_placeholders}
            WHERE {update_criteria};
            """,
            values,
        )

    def delete(self, table_name: str, criteria: dict[str, str]) -> None:
        placeholders = (f"{column} = ?" for column in criteria.keys())
        delete_criteria = " AND ".join(placeholders)
        self._execute(
            f"""
            DELETE FROM {table_name}
            WHERE {delete_criteria};
            """,
            tuple(criteria.values()),
        )


if __name__ == "__main__":

    db_manager = DatabaseManager("data/bookmarks.db")

    db_manager.create_table(
        "bookmarks",
        {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "title": "TEXT NOT NULL",
            "url": "TEXT NOT NULL",
            "notes": "TEXT",
            "date_added": "TEXT NOT NULL",
        },
    )

    db_manager.add(
        "bookmarks",
        {
            "title": "GitHub",
            "url": "https://github.com",
            "notes": "A place to store repositories of code",
            "date_added": "2022-01-06T18:22:36",
        },
    )

    results_cursor = db_manager.select(
        "bookmarks",
        # criteria={"title": "GitHub"}
    )
    print(results_cursor.fetchall())

    db_manager.delete("bookmarks", criteria={"title": "GitHub"})

    del db_manager
