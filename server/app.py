from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    ExerciseSchema,
    WorkoutSchema,
    WorkoutExerciseSchema,
    ExerciseWithWorkoutsSchema
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# Schemas
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()
exercise_with_workouts_schema = ExerciseWithWorkoutsSchema()

# Routes

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(jsonify(workouts_schema.dump(workouts)), 200)

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    return make_response(jsonify(workout_schema.dump(workout)), 200)

@app.route('/workouts', methods=['POST'])
def create_workout():
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({"error": "No input data provided"}), 400)
    try:
        data = workout_schema.load(json_data)
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 400)

    try:
        new_workout = Workout(
            date=data['date'],
            duration_minutes=data['duration_minutes'],
            notes=data.get('notes')
        )
        db.session.add(new_workout)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 400)

    return make_response(jsonify(workout_schema.dump(new_workout)), 201)

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    
    try:
        db.session.delete(workout)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 400)

    return make_response(jsonify({}), 204)

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(jsonify(exercises_schema.dump(exercises)), 200)

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)
    return make_response(jsonify(exercise_with_workouts_schema.dump(exercise)), 200)

@app.route('/exercises', methods=['POST'])
def create_exercise():
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({"error": "No input data provided"}), 400)
    try:
        data = exercise_schema.load(json_data)
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 400)

    try:
        new_exercise = Exercise(
            name=data['name'],
            category=data['category'],
            equipment_needed=data.get('equipment_needed', False)
        )
        db.session.add(new_exercise)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 400)

    return make_response(jsonify(exercise_schema.dump(new_exercise)), 201)

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)
    
    try:
        db.session.delete(exercise)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 400)

    return make_response(jsonify({}), 204)

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)
    
    json_data = request.get_json() or {}
    json_data['workout_id'] = workout_id
    json_data['exercise_id'] = exercise_id

    try:
        data = workout_exercise_schema.load(json_data)
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 400)

    try:
        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )
        db.session.add(workout_exercise)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e)}), 400)

    return make_response(jsonify(workout_exercise_schema.dump(workout_exercise)), 201)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
