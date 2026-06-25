import pytest
from datetime import date
from app import app
from models import db, Exercise, Workout, WorkoutExercise

# Configure app for testing with in-memory SQLite at module level
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

# Re-register SQLAlchemy for in-memory DB configuration once
if app in db._app_engines:
    del db._app_engines[app]
if "sqlalchemy" in app.extensions:
    del app.extensions["sqlalchemy"]
db.init_app(app)

@pytest.fixture
def client():
    with app.app_context():
        db.create_all()
        # Seed basic test data
        e1 = Exercise(name="Pushups", category="Strength", equipment_needed=False)
        e2 = Exercise(name="Running", category="Cardio", equipment_needed=False)
        db.session.add_all([e1, e2])
        
        w1 = Workout(date=date(2026, 6, 25), duration_minutes=30, notes="Test Workout")
        db.session.add(w1)
        db.session.commit()
        
        yield app.test_client()
        db.session.remove()
        db.drop_all()

# --- MODEL VALIDATIONS ---

def test_exercise_validation_invalid_category(client):
    with app.app_context():
        with pytest.raises(ValueError):
            e = Exercise(name="Yoga", category="InvalidCategory")
            db.session.add(e)
            db.session.commit()

def test_exercise_validation_short_name(client):
    with app.app_context():
        with pytest.raises(ValueError):
            e = Exercise(name="Yo", category="Flexibility")
            db.session.add(e)
            db.session.commit()

def test_workout_validation_negative_duration(client):
    with app.app_context():
        with pytest.raises(ValueError):
            w = Workout(date=date.today(), duration_minutes=-10)
            db.session.add(w)
            db.session.commit()

def test_workout_exercise_validation_negative_reps(client):
    with app.app_context():
        w = Workout.query.first()
        e = Exercise.query.first()
        with pytest.raises(ValueError):
            we = WorkoutExercise(workout=w, exercise=e, reps=-5, sets=3)
            db.session.add(we)
            db.session.commit()

# --- API ENDPOINTS ---

def test_get_workouts(client):
    res = client.get('/workouts')
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 1
    assert data[0]['duration_minutes'] == 30
    assert data[0]['notes'] == "Test Workout"

def test_get_workout_by_id(client):
    res = client.get('/workouts/1')
    assert res.status_code == 200
    data = res.get_json()
    assert data['id'] == 1
    assert data['notes'] == "Test Workout"

def test_get_workout_not_found(client):
    res = client.get('/workouts/999')
    assert res.status_code == 404
    data = res.get_json()
    assert "error" in data

def test_create_workout_success(client):
    res = client.post('/workouts', json={
        "date": "2026-07-01",
        "duration_minutes": 45,
        "notes": "July morning session"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data['id'] is not None
    assert data['duration_minutes'] == 45

def test_create_workout_invalid(client):
    res = client.post('/workouts', json={
        "date": "invalid-date",
        "duration_minutes": 0
    })
    assert res.status_code == 400
    data = res.get_json()
    assert "errors" in data or "error" in data

def test_delete_workout(client):
    res = client.delete('/workouts/1')
    assert res.status_code == 204
    # Ensure deleted
    res_get = client.get('/workouts/1')
    assert res_get.status_code == 404

def test_get_exercises(client):
    res = client.get('/exercises')
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 2

def test_create_exercise_success(client):
    res = client.post('/exercises', json={
        "name": "Plank",
        "category": "Balance",
        "equipment_needed": False
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data['name'] == "Plank"

def test_create_exercise_invalid(client):
    res = client.post('/exercises', json={
        "name": "Pl",
        "category": "Invalid"
    })
    assert res.status_code == 400

def test_add_exercise_to_workout(client):
    res = client.post('/workouts/1/exercises/2/workout_exercises', json={
        "reps": 12,
        "sets": 3,
        "duration_seconds": 0
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data['reps'] == 12
    assert data['sets'] == 3
    
    res_w = client.get('/workouts/1')
    w_data = res_w.get_json()
    assert len(w_data['workout_exercises']) == 1
    assert w_data['workout_exercises'][0]['exercise']['name'] == "Running"
    assert w_data['workout_exercises'][0]['reps'] == 12
