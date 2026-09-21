# Student Record Management System

A beginner-friendly command-line CRUD application demonstrating Python functions, file I/O, CSV/JSON, validation, exceptions, lambda functions, and list comprehensions.

## Requirements

- Python 3.10 or newer
- No third-party packages are required.

## Setup

### Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Run

From this project directory:

```bash
python student_manager.py
```

CSV is the default format. To use JSON:

```bash
python student_manager.py --format json
```

To choose a custom file path:

```bash
python student_manager.py --format csv --file data/classroom.csv
```

## Menu

1. Add student
2. List students
3. Search by ID
4. Update student
5. Delete student
6. Save and exit

Each student record has `student_id`, `name`, `age`, `grade`, and `email`. Student IDs must be unique. Age must be an integer from 3 through 120. Email can be blank; if supplied, it must contain `@`.

## Data files

- `data/students.csv` — created when the CSV app saves.
- `data/students.json` — created when the JSON app saves.
- `data/sample_students.csv` and `data/sample_students.json` — small examples.

The program uses UTF-8 and Python's built-in `csv` and `json` modules. It treats a missing database as an empty list and reports common input/file errors.

## Concepts demonstrated

- **Functions:** `add_student`, `find_student`, `update_student`, `delete_student`, and persistence helpers.
- **Parameters and return values:** functions accept records/IDs and return normalized records, a match, or deleted record.
- **Lambda:** `sort_by_name` uses `key=lambda record: record["name"].casefold()`.
- **List comprehension:** record loading and sorting examples.
- **File handling:** `with path.open(...)` safely closes files.
- **Exceptions:** validation raises `ValueError`; missing records raise `KeyError`; file problems raise `OSError`; JSON parsing errors are translated into a clear message.
- **try/except/finally:** menu actions catch expected errors; a `finally` block demonstrates guaranteed cleanup flow.
- **Debugging:** use print statements, breakpoints, and the Python debugger (`python -m pdb student_manager.py`).

## Tests

Run the automated tests with:

```bash
python -m unittest discover -s tests -v
```

## Suggested practice

1. Add a search-by-name feature.
2. Add sorting by grade or age.
3. Add a confirmation prompt before deletion.
4. Add a CSV-to-JSON export option.
5. Add a unit test for invalid email and duplicate IDs.
6. Replace the `finally: pass` with a useful cleanup/logging action.
