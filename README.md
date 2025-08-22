# NiceGUI Kanban Board

A simple Kanban board application built with Python, NiceGUI, and SQLite.

## Features

- Create, view, and move tasks between columns.
- Drag-and-drop interface for moving tasks.
- Data is persisted in a local SQLite database (`kanban.db`).

## Setup and Installation

1.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To start the Kanban board application, run:

```bash
python main.py
```

The application will be available at `http://127.0.0.1:8080`.