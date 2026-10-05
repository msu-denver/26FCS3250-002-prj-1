# gpa_calculator_hlib_yeromin

Credit-weighted GPA calculation for letter-graded courses. Pure standard library,
no runtime dependencies.

Part of the CS3250 *Software Development Methods and Tools* (Project 1) GPA
Calculator at MSU Denver.

## Install

```bash
pip install gpa_calculator_hlib_yeromin
```

## Usage

`calculate_gpa` takes a list of enrollment-like objects. Each needs a `grade`
attribute and a `course` with a `credits` attribute — anything duck-typed works,
so you can pass the project's SQLAlchemy `Enrollment` objects directly or your
own dataclasses.

```python
from gpa_calculator import calculate_gpa, GRADE_POINTS

class Course:
    def __init__(self, credits):
        self.credits = credits

class Enrollment:
    def __init__(self, grade, credits):
        self.grade = grade
        self.course = Course(credits)

enrollments = [
    Enrollment('A', 4),
    Enrollment('B+', 3),
    Enrollment('A-', 4),
]

print(calculate_gpa(enrollments))  # 3.7
```

### Grade scale

`GRADE_POINTS` uses the traditional college letter scale. `A+` is included and
worth 4.3, so a GPA can exceed 4.0.

| Grade | Points | | Grade | Points | | Grade | Points |
|-------|--------|-|-------|--------|-|-------|--------|
| A+    | 4.3    | | C+    | 2.3    | | D-    | 0.7    |
| A     | 4.0    | | C     | 2.0    | | F     | 0.0    |
| A-    | 3.7    | | C-    | 1.7    | |       |        |
| B+    | 3.3    | | D+    | 1.3    | |       |        |
| B     | 3.0    | | D     | 1.0    | |       |        |
| B-    | 2.7    | |       |        | |       |        |

## Behaviour

- Enrollments with no grade yet, an unrecognised grade, or non-positive credits
  are skipped rather than raising.
- Returns `0` when there are no graded credits to average.
- Otherwise returns the credit-weighted mean, rounded to 3 decimals.

## License

MIT — see [LICENSE](LICENSE).
