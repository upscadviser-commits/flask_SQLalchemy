# Workout Tracker API

A professional Flask-SQLAlchemy backend API for personal trainers to track workouts and reusable exercises. Built with Flask, SQLAlchemy, Marshmallow, and Flask-Migrate.

## Project Description

This API handles storing and retrieving information about workouts and exercises. It uses a many-to-many relationship via a join table (`WorkoutExercise`) containing sets, reps, and duration for each specific exercise included in a workout.

### Key Features
*   **Table Constraints**: SQLite unique constraints on exercise names and positive check constraints on duration, reps, sets, and duration seconds.
*   **Model Validations**: Custom `@validates` validations verifying name length, category (restricted to strength/cardio/flexibility/balance), and ISO date formatting.
*   **Schema Validations & Serialization**: Marshmallow schemas for validating request bodies (handling range validations) and serializing complex nested relationship structures.
*   **Cascade Deletions**: Deleting a workout or exercise cascadingly cleans up all referencing association rows in the join table.

---

## Installation & Setup

1.  **Create and Activate Virtual Environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize Database and Migrations**:
    ```bash
    export FLASK_APP=server/app.py
    flask db init
    flask db migrate -m "initial migration"
    flask db upgrade
    ```

4.  **Seed Database**:
    ```bash
    PYTHONPATH=server python server/seed.py
    ```

5.  **Run the Test Suite**:
    ```bash
    PYTHONPATH=server pytest server/test_app.py
    ```

---

## Running the Application

Start the Flask server locally:
```bash
export FLASK_APP=server/app.py
flask run --port=5555
```
The server will be available at `http://localhost:5555`.

---

## API Endpoints

### Workouts

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/workouts` | Retrieve a list of all workouts |
| `GET` | `/workouts/<id>` | Retrieve a single workout, including associated exercises with reps/sets/duration details |
| `POST` | `/workouts` | Create a new workout. Requires `date` and `duration_minutes` |
| `DELETE` | `/workouts/<id>` | Delete a workout (and cascade-delete associated workout exercises) |

### Exercises

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/exercises` | Retrieve a list of all exercises |
| `GET` | `/exercises/<id>` | Retrieve a single exercise and all workouts it is associated with |
| `POST` | `/exercises` | Create a new exercise. Requires `name` and `category` |
| `DELETE` | `/exercises/<id>` | Delete an exercise (and cascade-delete associated workout exercises) |

### Associations

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout, specifying `reps`, `sets`, or `duration_seconds` in the request body |
