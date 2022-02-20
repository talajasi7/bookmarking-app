# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2022-02-20

---

### Added

- ...

### Changed

- Now each `Command` returns a tuple representing both the status and the result of the operation.
- Decoupling commands from database specifics (`DatabaseManager`) with an interface `PersistenceLayer`.
- Create a `BookmarkDatabase` implementation for the interface to handle common database operations.
- Creating the table `bookmarks`, when needed, now takes place in the `__init__` method of `BookmarkDatabase`.

### Fixed

- ...

### Removed

- Delete `CreateBookmarksTableCommand` command, and the code of all modules where it is called.
