# Practice Exercises

Try these after running the application.

1. **Functions:** Write `count_students(records)` that returns the number of records.
2. **Parameters/defaults:** Add a function that filters by grade, with an optional grade parameter.
3. **Lambda:** Sort students by age, then by name.
4. **List comprehension:** Create a list of names for students whose age is at least 16.
5. **CSV:** Add a feature to export only students in a chosen grade to a separate CSV file.
6. **JSON:** Make the JSON loader reject any top-level value that is not a list.
7. **Exceptions:** Handle an invalid menu choice without terminating the program.
8. **Debugging:** Set a breakpoint inside `update_student`; inspect `current`, `changes`, and `candidate`.
9. **Testing:** Write tests for blank names, out-of-range ages, missing IDs, and invalid email.
10. **Extension:** Add a new field such as `phone`, updating `FIELDS`, sample files, and tests.

## Reflection

- Why is `with open(...)` preferable to manually calling `close()`?
- What is the difference between `return` and `print`?
- When should an exception be raised versus handled?
- Why should a CRUD application validate data before saving?
