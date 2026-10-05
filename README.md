# Overview

Your team has been hired to develop a simple web application that allows students to track their GPAs. This project serves as an initial proof of concept to demonstrate your team's capabilities before it is assigned a more complex task. Because the project's requirements are well defined and its scope is limited, the team has chosen the Waterfall process model, following its traditional phases which include:

* Communication: gathering and understanding requirements
* Planning: defining schedules, resources, and milestones
* Modeling: designing system architecture and data models
* Construction: implementing and testing the application
* Deployment: delivering the final product to users

**Team deliverable status:** all five phases complete. The `gpa_calculator` library is packaged and published to PyPI, and a `Dockerfile` is included for containerized delivery.

# Communication Phase

## Overview

The project involves developing a web application that allows students to track their GPAs. Students should be able to register for the application and, after successfully logging in, enter completed courses along with their corresponding letter grades. The application should display all previously entered courses and calculate the student's overall GPA. Students should also be able to update their letter grades if they were entered incorrectly.

## Objectives 

* Track previously completed courses for each student, including their letter grades.
* Calculate and display the student's overall GPA.

## Requirements 

1. Users must be able to authenticate themselves.
2. Students (authenticated users) must be able to view all previously completed courses.
3. Students must be able to view their current GPA.
4. Students must be able to update the letter grade for a course.
5. Students must be able to delete a previously completed course.

### Requirement coverage

| # | Requirement | Implementation |
|---|---|---|
| 1 | Authenticate | `src/app/routes.py` — `/users/signup`, `/users/login`, `/users/signout`; Flask-Login sessions, bcrypt hashing |
| 2 | View all courses | `/enrollments` → `templates/enrollments.html` |
| 3 | View current GPA | `/enrollments` renders `calculate_gpa(current_user.enrollments)` |
| 4 | Update letter grade | `/enrollments/update/<prefix>/<number>` → `templates/update_enrollment.html` |
| 5 | Delete a course | `/enrollments/delete/<prefix>/<number>` |

## Constraints 

* A working version of the web application is expected to be delivered in 3 weeks. 
* The implementation team is limited to 3 to 5 members. 
* The software must be implemented in Python, Flask, and SQLAlchemy. 

## Risks 

* The project team has limited experience with some of the technologies and tools being used.

# Planning Phase

## Schedule 

Estimate a schedule for this project by completing the table below. 

|Phase|Task|Start|End|Duration|Deliverable|
|---|---|---|---|---|---|
|Modeling|Requirements Analysis|09/16/26|09/17/26|2 days|Use Case Diagram|
|Modeling|Data Model|09/17/26|09/18/26|2 days|Class Diagram|
|Construction|Coding|09/18/26|10/01/26|14 days|Code|
|Construction|Testing|10/02/26|10/05/26|4 days|Test Report|
|Deployment|Delivery|10/06/26|10/07/26|2 days|Final Commit/Push|

## Team Roles

Assign roles to each team member by completing the table below. A member may take on more than one role.

|Name|Role(s)|
|--|--|
|Hlib Yeromin|manager (owner)|
|Richard Hall|developer|
|Riley Drenth|testing and documentation|

## Branch Model

```
feature/* ──PR──▶ dev ──PR──▶ main ──tag──▶ PyPI + Docker
```

- `main` — stable, protected, only via PR from `dev`.
- `dev` — integration branch for all feature work.
- `feature/*` — short-lived branches per task, created from `dev`.

# Modeling Phase

## Requirements Analysis 

Based on the project description, perform a requirements analysis by developing a UML use case diagram that captures the system's key functionalities and user interactions.

![Use Case Diagram](pics/pic1.png)

Source: [`uml/use_case.wsd`](uml/use_case.wsd)

## Data Model 

Based on the data model defined in [src/app/models.py](src/app/models.py), create a UML class diagram to document the system's structure. The model includes the following entities:

* User: id, name, about, and password.
* Courses: prefix, number, name, credits
* Enrollment: user_id, course_prefix, course_number, grade

Make sure that your class diagram shows the association between **User**, **Course**, and **Enrollment**. 

![Class Diagram](pics/pic3.png)

Source: [`uml/class.wsd`](uml/class.wsd)

`Enrollment` is an association object resolving the many-to-many between `User` and `Course`, carrying the `grade`. Both sides expose an `association_proxy` (`user.courses` / `course.students`). The composite primary key on `Enrollment` (`user_id`, `course_prefix`, `course_number`) means a student cannot enroll in the same course twice, which is what makes the grade update in requirement 4 unambiguous.

## Baseline Implementation

A baseline for the web app is given in **Flask**. The project should be structured like the following: 

```
.venv
pics
src
|__app
|____ __init__.py
|____ models.py
|____ routes.py
|____ forms.py
|__ gpa_calculator
|____ __init__.py
|__ init_db.py
|__ pyproject.toml
|__ README.md
|__ LICENSE
instance
|__ prj1.db
static
|__ style.css
templates
|__ base.html
|__ index.html
|__ login.html
|__ signup.html
|__ error.html
|__ create_enrollment.html
|__ update_enrollment.html
|__ enrollments.html
uml
|__ class.wsd
|__ use_case.wsd
README.md
requirements.txt
Dockerfile
.dockerignore
.gitignore
```

[.venv](.venv) should not be pushed to the remote repository. Be sure to add it to your [.gitignore](.gitignore) file to exclude it from version control.

# Implementation Phase

Create a public GitHub repository for your project. Add all team members as collaborators. Share the URL of your repo with your instructor:  

```
Project's GitHub Repository: https://github.com/msu-denver/26FCS3250-002-prj-1
```

Following software development collaboration best practices, create a **dev** branch to manage beta versions of your project. Additionally, each team member should create local temporary branches for individual development and testing tasks. Once the **dev** branch reaches a stable state, merge it into the **main** branch. The **main** branch should be protected. 

To run an initial course load, modify [src/init_db.py](src/init_db.py) to insert at least 5 courses of your choice. 

As part of the project requirements, you must create your own **gpa_calculator** library according to the provided model. The library must be packaged and published to PyPI so that it can be installed using pip. 

Before beginning implementation, a team representative must meet with the instructor for a **mandatory** checkpoint. This can be done eiter in person or online. Either way, it needs to be scheduled. Be prepared to present the following:

* Use case and class diagrams
* A working baseline implementation of the app
* The **main** branch is protected
* A draft project schedule
* Team role assignments

## The gpa_calculator library

`src/gpa_calculator` is a standalone, dependency-free module. `calculate_gpa(enrollments)`
returns the credit-weighted GPA, rounded to 3 decimals. Enrollments with no grade, an
unrecognised grade, or non-positive credits are skipped; with no graded credits it returns `0`.

The grade scale includes `A+` at 4.3, so a GPA can exceed 4.0.

```python
from gpa_calculator import calculate_gpa

class Course:
    def __init__(self, credits): self.credits = credits

class Enrollment:
    def __init__(self, grade, credits):
        self.grade = grade
        self.course = Course(credits)

calculate_gpa([Enrollment('A', 4), Enrollment('B+', 3), Enrollment('A-', 4)])  # 3.7
```

### Build and publish

The package lives in `src/` and builds with `hatchling`:

```bash
cd src
uv build                                  # or: python -m build
uv publish                                # or: twine upload dist/*
```

Published at **https://pypi.org/project/gpa-calculator-hlib-yeromin/** — install with:

```bash
pip install gpa_calculator_hlib_yeromin
```

Note that `src/pyproject.toml` must declare which directory to ship, since the distribution
name (`gpa_calculator_hlib_yeromin`) differs from the package directory (`gpa_calculator`):

```toml
[tool.hatch.build.targets.wheel]
packages = ["gpa_calculator"]
```

Only `gpa_calculator` is distributed. The Flask app is not part of the wheel.

## Tech Stack

|Layer|Technology|Purpose|
|---|---|---|
|Framework|[Flask](https://flask.palletsprojects.com/)|Web application framework|
|ORM|[Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)|Database ORM for models (`User`, `Course`, `Enrollment`)|
|Forms|[Flask-WTF](https://flask-wtf.readthedocs.io/) / [WTForms](https://wtforms.readthedocs.io/)|Form handling and CSRF protection|
|Auth|[Flask-Login](https://flask-login.readthedocs.io/)|User session management|
|Hashing|[bcrypt](https://pypi.org/project/bcrypt/)|Secure password hashing|
|Database|[SQLite](https://www.sqlite.org/)|Local development database (`instance/prj1.db`)|
|GPA Library|[gpa_calculator](./src/gpa_calculator)|Credit-weighted GPA calculation module|
|Packaging|[hatchling](https://hatch.pypa.io/)|Build backend for PyPI distribution|

## Getting Started

### Prerequisites

- Python 3.9+
- macOS/Linux/Windows

### Installation

```bash
git clone https://github.com/msu-denver/26FCS3250-002-prj-1.git
cd 26FCS3250-002-prj-1

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### Running the Application

```bash
cd src

# seed the course catalog (idempotent; also runs automatically on first boot)
python init_db.py

export FLASK_APP=app  # On Windows (CMD): set FLASK_APP=app
                      # On Windows (PowerShell): $env:FLASK_APP="app"

flask run --host 127.0.0.1 --port 5000
```

Open your browser and navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

> The app must be started from `src/`. `Flask` is instantiated with a display name rather than
> an import name, so `root_path` resolves to the current working directory — that is what places
> the SQLite file in `src/instance/` and makes `../templates` and `../static` resolve correctly.

## Usage

1. **Sign Up** — create an account with ID, name, password, and confirmation
2. **Log In** — authenticate with your credentials
3. **Grade Entry** — click "Grade Entry" to add a course with its letter grade
4. **View Enrollments** — see all enrolled courses with credits, grades, and calculated GPA
5. **Update Grade** — click "Edit" on a row to correct a letter grade; GPA recalculates
6. **Delete Enrollment** — remove a course (GPA automatically recalculates)
7. **Sign Out** — end your session

# Testing Phase

At this stage, you are NOT expected to write automated tests. Instead, you should perform manual testing, documenting your test results using the table provided below.

|Functionality Tested|Date|Time|Result|
|--|--|--|--|
|Sign Up|10/01/26|14:30|passed|
|Login / Signout|10/01/26|14:30|passed|
|List Enrollments|10/01/26|14:31|passed|
|Create Enrollment|10/01/26|14:31|passed|
|Delete Enrollment|10/01/26|14:32|passed|
|Update Grade / GPA|10/01/26|14:32|passed|

GPA display was additionally checked against hand-computed credit-weighted values:
`A`(4cr) = 4.00, `B+`(4cr) = 3.30, `A`(4cr) `+` `F`(4cr) = 2.00, and the mixed set
`B+`(4cr) `+` `A`(4cr) = 3.65. Access to `/enrollments` without a session was confirmed to
redirect to login.

# Deployment Phase

Create a Docker image to allow the instructor to run your project in a containerized environment. To meet this requirement, include a **Dockerfile** in your repository that enables the instructor to build the image and run the application as a container.

```bash
docker build -t gpa-calculator .
docker run --rm -p 5000:5000 gpa-calculator
```

Then open [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

The image mirrors the local checkout layout (`/srv/src/app`, `/srv/templates`, `/srv/static`)
and starts the app from `/srv/src` so the working-directory-dependent paths described above
resolve identically to a local run. Courses are seeded at build time; the container runs as an
unprivileged user.

# Team Evaluation 

Students should use this [form](https://forms.cloud.microsoft/r/RiQbbB9VhD) to evaluate your team members and complete a self-evaluation. This is a mandatory requirement, and the team's grade will be placed on hold until all members have submitted their evaluations.

# Rubric 

```
+5 Planning: Schedule
+5 Planning: Team Roles 
+5 Modeling: Use Case Diagram 
+5 Modeling: Class Diagram
+5 Check-point
+10 Courses data load
+5 Authentication
+10 List of Enrollments
+10 Create Enrollment
+10 Delete Enrollment
+10 GPA Calculation and Display
+10 GPA PyPI build and deployment
+5 Testing 
+5 Deployment
-25 Team/Self Evaluation
-5 main branch not protected
```

# User Interface Suggestions

![pic1](pics/pic1.png)

![pic2](pics/pic2.png)

![pic3](pics/pic3.png)

![pic4](pics/pic4.png)

![pic5](pics/pic5.png)

![pic6](pics/pic6.png)

![pic7](pics/pic7.png)
