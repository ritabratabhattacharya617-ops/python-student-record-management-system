"""Student Record Management System with CSV/JSON persistence.

Run:
    python student_manager.py
    python student_manager.py --format json
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

FIELDS = ["student_id", "name", "age", "grade", "email"]


def clean_text(value: Any) -> str:
    """Convert a value to trimmed text."""
    return str(value).strip()


def validate_student(student: dict[str, Any]) -> dict[str, str]:
    """Validate and normalize a student record."""
    normalized = {field: clean_text(student.get(field, "")) for field in FIELDS}
    if not normalized["student_id"]:
        raise ValueError("Student ID cannot be empty.")
    if not normalized["name"]:
        raise ValueError("Name cannot be empty.")
    try:
        age = int(normalized["age"])
    except (TypeError, ValueError) as exc:
        raise ValueError("Age must be a whole number.") from exc
    if not 3 <= age <= 120:
        raise ValueError("Age must be between 3 and 120.")
    normalized["age"] = str(age)
    if not normalized["grade"]:
        raise ValueError("Grade cannot be empty.")
    if normalized["email"] and "@" not in normalized["email"]:
        raise ValueError("Email must contain '@' or be left blank.")
    return normalized


def load_records(path: str | Path, file_format: str) -> list[dict[str, str]]:
    """Load records from CSV or JSON. A missing file means an empty database."""
    path = Path(path)
    if not path.exists():
        return []
    try:
        with path.open("r", newline="", encoding="utf-8") as file:
            if file_format == "csv":
                return [
                    {field: clean_text(row.get(field, "")) for field in FIELDS}
                    for row in csv.DictReader(file)
                ]
            if file_format == "json":
                data = json.load(file)
                if not isinstance(data, list):
                    raise ValueError("JSON database must contain a list of records.")
                return [
                    {field: clean_text(row.get(field, "")) for field in FIELDS}
                    for row in data
                    if isinstance(row, dict)
                ]
            raise ValueError("Format must be 'csv' or 'json'.")
    except json.JSONDecodeError as exc:
        raise ValueError(f"Could not parse JSON database: {exc}") from exc
    except OSError as exc:
        raise OSError(f"Could not read {path}: {exc}") from exc


def save_records(path: str | Path, records: list[dict[str, str]], file_format: str) -> None:
    """Write all records to CSV or JSON."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("w", newline="", encoding="utf-8") as file:
            if file_format == "csv":
                writer = csv.DictWriter(file, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(records)
            elif file_format == "json":
                json.dump(records, file, indent=2, ensure_ascii=False)
                file.write("\n")
            else:
                raise ValueError("Format must be 'csv' or 'json'.")
    except OSError as exc:
        raise OSError(f"Could not write {path}: {exc}") from exc


def add_student(records: list[dict[str, str]], student: dict[str, Any]) -> dict[str, str]:
    """Create a record, rejecting duplicate IDs."""
    student = validate_student(student)
    if any(record["student_id"] == student["student_id"] for record in records):
        raise ValueError(f"Student ID {student['student_id']} already exists.")
    records.append(student)
    return student


def find_student(records: list[dict[str, str]], student_id: str) -> dict[str, str] | None:
    """Return the matching record, or None when absent."""
    return next((r for r in records if r["student_id"] == clean_text(student_id)), None)


def update_student(
    records: list[dict[str, str]], student_id: str, changes: dict[str, Any]
) -> dict[str, str]:
    """Update a record in place and return it."""
    current = find_student(records, student_id)
    if current is None:
        raise KeyError(f"No student with ID {student_id}.")
    candidate = {**current, **changes, "student_id": current["student_id"]}
    normalized = validate_student(candidate)
    current.update(normalized)
    return current


def delete_student(records: list[dict[str, str]], student_id: str) -> dict[str, str]:
    """Delete and return a record."""
    student = find_student(records, student_id)
    if student is None:
        raise KeyError(f"No student with ID {student_id}.")
    records.remove(student)
    return student


def sort_by_name(records: list[dict[str, str]]) -> list[dict[str, str]]:
    """Example lambda and list-comprehension usage."""
    return sorted([record for record in records], key=lambda record: record["name"].casefold())


def print_records(records: list[dict[str, str]]) -> None:
    if not records:
        print("No student records found.")
        return
    print(f'{"ID":<12} {"Name":<22} {"Age":<5} {"Grade":<10} Email')
    print("-" * 76)
    for record in records:
        print(
            f'{record["student_id"]:<12} {record["name"]:<22} '
            f'{record["age"]:<5} {record["grade"]:<10} {record["email"]}'
        )


def prompt_student(existing: dict[str, str] | None = None) -> dict[str, str]:
    existing = existing or {}
    result = {}
    for field in FIELDS:
        label = field.replace("_", " ").title()
        current = existing.get(field, "")
        suffix = f" [{current}]" if current else ""
        value = input(f"{label}{suffix}: ").strip()
        result[field] = value if value else current
    return result


def run_app(file_format: str, path: Path) -> None:
    records = load_records(path, file_format)
    actions = {
        "1": "Add student",
        "2": "List students",
        "3": "Search by ID",
        "4": "Update student",
        "5": "Delete student",
        "6": "Save and exit",
    }
    while True:
        print(f"\nStudent Record Management ({file_format.upper()})")
        for key, label in actions.items():
            print(f"{key}. {label}")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                student = add_student(records, prompt_student())
                save_records(path, records, file_format)
                print(f"Added {student['name']}.")
            elif choice == "2":
                print_records(sort_by_name(records))
            elif choice == "3":
                student = find_student(records, input("Student ID: "))
                print_records([student] if student else [])
            elif choice == "4":
                student_id = input("Student ID to update: ").strip()
                current = find_student(records, student_id)
                if current is None:
                    raise KeyError(f"No student with ID {student_id}.")
                updated = update_student(records, student_id, prompt_student(current))
                save_records(path, records, file_format)
                print(f"Updated {updated['name']}.")
            elif choice == "5":
                deleted = delete_student(records, input("Student ID to delete: "))
                save_records(path, records, file_format)
                print(f"Deleted {deleted['name']}.")
            elif choice == "6":
                save_records(path, records, file_format)
                print(f"Records saved to {path}. Goodbye!")
                break
            else:
                print("Please choose a number from 1 to 6.")
        except (ValueError, KeyError, OSError) as exc:
            print(f"Error: {exc}")
        except KeyboardInterrupt:
            print("\nAction cancelled.")
        finally:
            # This block runs after each menu action, including handled errors.
            pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage student records in CSV or JSON.")
    parser.add_argument("--format", choices=("csv", "json"), default="csv")
    parser.add_argument("--file", help="Optional database path")
    args = parser.parse_args()
    default_path = Path("data") / f"students.{args.format}"
    run_app(args.format, Path(args.file) if args.file else default_path)


if __name__ == "__main__":
    main()
