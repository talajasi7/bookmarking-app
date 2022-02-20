# **BARK** - A bookmarking application

## **(from 'Practices of the Python Pro' book)**

**BARK** is a bookmarking application where, using a command-line interface, a user chooses options for adding, listing, updating and deleting bookmarks stored in a database.

## Architecture design

---
BARK is based on a multitier architecture pattern to be compliant with the *separation of concerns* design principle. The high-level layers of abstraction for BARK are the following:

- **Presentation layer**: the *command-line interface* (CLI). This is a way to present options to a user and understand which options they choose.
- **Persistence layer**: the *database*. Data needs to be persisted (stored) for later use.
- **Business logic layer**: the *commands* and *actions*. Once an option is chosen, some action or business logic happens as a result. This layer acts as the glue that connects the presentation and persistence layers.

The core idea behind this kind of architecture is that each layer (tier) of the application has freedom to evolve.
