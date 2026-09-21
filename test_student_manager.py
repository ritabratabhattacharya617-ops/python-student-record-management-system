import tempfile
import unittest
from pathlib import Path

from student_manager import (
    add_student, delete_student, find_student, load_records, save_records,
    update_student, validate_student,
)


class StudentManagerTests(unittest.TestCase):
    def setUp(self):
        self.records = []
        self.student = {
            "student_id": "S10", "name": "Mina Roy", "age": "15",
            "grade": "9", "email": "mina@example.com",
        }

    def test_create_and_find(self):
        add_student(self.records, self.student)
        self.assertEqual(find_student(self.records, "S10")["name"], "Mina Roy")

    def test_duplicate_id_rejected(self):
        add_student(self.records, self.student)
        with self.assertRaises(ValueError):
            add_student(self.records, self.student)

    def test_update(self):
        add_student(self.records, self.student)
        updated = update_student(self.records, "S10", {"name": "Mina Das"})
        self.assertEqual(updated["name"], "Mina Das")

    def test_delete(self):
        add_student(self.records, self.student)
        delete_student(self.records, "S10")
        self.assertIsNone(find_student(self.records, "S10"))

    def test_invalid_age(self):
        bad = {**self.student, "age": "old"}
        with self.assertRaises(ValueError):
            validate_student(bad)

    def test_csv_and_json_round_trip(self):
        add_student(self.records, self.student)
        with tempfile.TemporaryDirectory() as tmp:
            for fmt in ("csv", "json"):
                path = Path(tmp) / f"students.{fmt}"
                save_records(path, self.records, fmt)
                self.assertEqual(load_records(path, fmt), self.records)


if __name__ == "__main__":
    unittest.main()
